from src.lead_intelligence import analyze_lead, build_response_draft, classify_enquiry

def test_ai_automation_classification():
    category, scores, matched = classify_enquiry(
        "We need an AI agent and LLM automation for invoice processing"
    )
    assert category == "AI Automation"
    assert "ai agent" in matched

def test_seo_classification():
    result = analyze_lead("Our SEO is weak and organic traffic has declined.")
    assert result["category"] == "Digital Marketing & SEO"

def test_urgent_cloud_issue_is_high_priority():
    result = analyze_lead("Urgent: our AWS production server outage needs monitoring.")
    assert result["category"] == "Cloud & Infrastructure"
    assert result["priority"] == "High"

def test_ambiguous_or_unknown_enquiry_goes_to_review():
    result = analyze_lead("Hello, I want to know more.")
    assert result["category"] == "Needs Human Review"
    assert result["requires_human_review"] is True

def test_response_draft_is_generated_without_claims():
    result = analyze_lead("We need a mobile app and backend API.")
    draft = build_response_draft("Example Ltd", result)
    assert "Example Ltd" in draft
    assert "discovery call" in draft.lower()
    assert result["requires_human_review"] is True
