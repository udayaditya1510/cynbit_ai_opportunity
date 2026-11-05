"""Explainable baseline for inbound lead triage.

This module intentionally avoids external model/API dependencies. It is a runnable
proof of concept, not a trained classifier. Replace or augment this baseline with
a validated supervised model when labelled enquiry data is available.
"""
from __future__ import annotations

import re
from typing import Dict, List, Tuple

CATEGORY_TERMS: Dict[str, List[str]] = {
    "AI Automation": [
        "ai agent", "ai automation", "llm", "chatbot", "voice agent",
        "document extraction", "invoice extraction", "automate", "automation",
        "large language model", "rag",
    ],
    "Software Development": [
        "mobile app", "web app", "website development", "backend", "api",
        "application", "software", "full stack", "full-stack", "frontend",
    ],
    "Cloud & Infrastructure": [
        "aws", "azure", "cloud migration", "cloud infrastructure", "devops",
        "ci/cd", "deployment", "kubernetes", "docker", "server outage",
        "monitoring", "scaling",
    ],
    "Digital Marketing & SEO": [
        "seo", "organic traffic", "google ads", "meta ads", "paid ads",
        "conversion rate", "keyword research", "digital marketing",
    ],
    "CRM & Growth": [
        "crm", "hubspot", "salesforce", "lead qualification", "lead generation",
        "sales pipeline", "follow-up", "customer relationship",
    ],
    "Careers & Training": [
        "internship", "intern", "job opening", "career", "training",
        "placement", "bit elevate", "bitev​levate",
    ],
}

SIGNAL_TERMS = {
    "AI / automation requirement": ["ai", "agent", "llm", "automation", "chatbot"],
    "CRM / sales integration": ["crm", "hubspot", "salesforce", "lead", "pipeline"],
    "Cloud / deployment requirement": ["aws", "azure", "cloud", "deployment", "hosting"],
    "Document processing requirement": ["pdf", "invoice", "document", "extract", "ocr"],
    "Marketing / SEO requirement": ["seo", "traffic", "ads", "marketing", "conversion"],
    "Application development requirement": ["app", "website", "backend", "api", "software"],
}

URGENT_TERMS = ["urgent", "asap", "immediately", "production down", "server outage", "critical"]
TIMELINE_TERMS = ["this week", "today", "tomorrow", "asap", "urgent", "immediately"]

DISCOVERY_QUESTIONS = {
    "AI Automation": [
        "Which business process should the AI automate, and what does success look like?",
        "Which systems or data sources must the solution integrate with?",
        "What should the AI do when confidence is low or a human decision is required?",
    ],
    "Software Development": [
        "Who are the primary users and what are the essential user journeys?",
        "Are there existing applications, APIs or design assets to integrate?",
        "What are the security, performance and launch requirements?",
    ],
    "Cloud & Infrastructure": [
        "Which cloud provider and current architecture are in use?",
        "What availability, security, backup and compliance requirements apply?",
        "Are there current infrastructure diagrams, logs or cost baselines?",
    ],
    "Digital Marketing & SEO": [
        "Which audience, geography and business outcome are you targeting?",
        "Which analytics and advertising accounts can be used for measurement?",
        "What baseline traffic, conversion and ranking data is available?",
    ],
    "CRM & Growth": [
        "Which CRM and sales tools are currently in use?",
        "How are leads captured, qualified, assigned and followed up today?",
        "Which conversion or response-time metrics should improve?",
    ],
    "Careers & Training": [
        "Which role, programme or training opportunity are you enquiring about?",
        "What are your skills, experience level and availability?",
        "Which location or working arrangement are you considering?",
    ],
    "Needs Human Review": [
        "Could you describe the business problem and desired outcome?",
        "Are there existing tools or systems involved?",
        "What timeline and constraints should we consider?",
    ],
}

def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").lower()).strip()

def _term_matches(text: str, terms: List[str]) -> List[str]:
    return [term for term in terms if term in text]

def classify_enquiry(message: str) -> Tuple[str, Dict[str, int], List[str]]:
    """Return best category, keyword counts, and matched terms."""
    text = _normalise(message)
    scores = {category: len(_term_matches(text, terms)) for category, terms in CATEGORY_TERMS.items()}
    best_score = max(scores.values(), default=0)
    if best_score == 0:
        return "Needs Human Review", scores, []
    winners = [category for category, score in scores.items() if score == best_score]
    # Ambiguous ties should not be silently forced into a single category.
    if len(winners) > 1:
        return "Needs Human Review", scores, []
    category = winners[0]
    return category, scores, _term_matches(text, CATEGORY_TERMS[category])

def _priority(message: str, category: str) -> Tuple[str, List[str]]:
    text = _normalise(message)
    reasons = _term_matches(text, URGENT_TERMS)
    if reasons:
        return "High", [f"Urgency signal: {term}" for term in reasons]
    if category in {"AI Automation", "Software Development", "Cloud & Infrastructure", "CRM & Growth"}:
        return "Medium", ["Commercial service enquiry; confirm urgency and fit during discovery."]
    return "Low", ["No explicit urgency signal detected."]

def _extract_signals(message: str) -> List[str]:
    text = _normalise(message)
    return [
        label for label, terms in SIGNAL_TERMS.items()
        if any(term in text for term in terms)
    ]

def analyze_lead(message: str, company: str = "", channel: str = "Website") -> dict:
    """Analyze an enquiry and return a JSON-serializable result."""
    category, scores, matched = classify_enquiry(message)
    priority, priority_reasons = _priority(message, category)
    if category == "Needs Human Review":
        confidence = 0.25 if not any(scores.values()) else 0.40
        next_action = "Manual review: clarify the requirement before assigning a service team."
        questions = DISCOVERY_QUESTIONS["Needs Human Review"]
    else:
        # This is deliberately labelled heuristic; not a probability.
        winning = scores[category]
        total = sum(scores.values())
        confidence = min(0.95, 0.55 + 0.10 * winning + (0.05 if total == winning else 0))
        next_action = "Offer a discovery call and confirm scope, timeline, stakeholders and success metrics."
        questions = DISCOVERY_QUESTIONS[category]
    signals = _extract_signals(message)
    return {
        "category": category,
        "priority": priority,
        "confidence": round(confidence, 2),
        "category_scores": scores,
        "matched_terms": matched,
        "explanation": (
            f"Matched {', '.join(matched)} for {category}."
            if matched else "No unique category match; human review prevents unreliable auto-routing."
        ),
        "priority_reasons": priority_reasons,
        "signals": signals,
        "discovery_questions": questions,
        "next_action": next_action,
        "company": company,
        "channel": channel,
        "requires_human_review": True,
    }

def build_response_draft(company: str, result: dict) -> str:
    """Create a neutral draft. It must be reviewed before sending."""
    recipient = company.strip() or "there"
    category = result["category"]
    return (
        f"Hi {recipient},\n\n"
        "Thank you for reaching out to Cynbit. From your message, it sounds like "
        f"your enquiry may relate to {category.lower()}. "
        "We would be happy to understand the problem, your current workflow and the outcome "
        "you are looking to achieve.\n\n"
        "Would you be available for a brief discovery call? We can then discuss the scope, "
        "relevant integrations, timeline and a suitable next step.\n\n"
        "Best regards,\nCynbit Team"
    )

SAMPLE_CATEGORIES = list(CATEGORY_TERMS.keys())
