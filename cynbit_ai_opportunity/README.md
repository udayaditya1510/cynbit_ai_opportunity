# Cynbit AI Opportunity Challenge
### AI Lead Intelligence & Sales Copilot — Research, working PoC, and technical plan

> **Submission-ready GitHub repository.** This project proposes and demonstrates an AI-assisted workflow for triaging inbound business enquiries, matching them to Cynbit service lines, preparing discovery questions, and drafting a human-reviewed response.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

## 1. Executive summary

Cynbit publicly presents itself as a technology services and product business spanning AI automation, custom software, cloud/infrastructure, digital growth and CRM-related workflows. The opportunity portfolio in [`docs/AI_OPPORTUNITY_REPORT.md`](docs/AI_OPPORTUNITY_REPORT.md) identifies eight AI/ML opportunities. The recommended first pilot is an **AI Lead Intelligence Copilot**.

The PoC accepts an enquiry, predicts a service category using an explainable baseline, suggests a priority, extracts simple requirement signals, recommends discovery questions, and drafts an acknowledgement for human review. It is deliberately safe-by-default: it does not send messages or write to a CRM.

## 2. Deliverables

| Required deliverable | Included file |
|---|---|
| AI Opportunity Report | [`docs/AI_OPPORTUNITY_REPORT.md`](docs/AI_OPPORTUNITY_REPORT.md) |
| Functional AI/ML Proof of Concept | [`app.py`](app.py), [`src/lead_intelligence.py`](src/lead_intelligence.py) |
| Technical Approach Report | [`docs/TECHNICAL_APPROACH.md`](docs/TECHNICAL_APPROACH.md) |
| Public research sources and assumptions | [`docs/SOURCES_AND_ASSUMPTIONS.md`](docs/SOURCES_AND_ASSUMPTIONS.md) |
| Sample data | [`data/sample_leads.csv`](data/sample_leads.csv) |
| Tests | [`tests/test_lead_intelligence.py`](tests/test_lead_intelligence.py) |

## 3. Run locally

### Requirements
- Python 3.10 or later
- pip

### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit (normally `http://localhost:8501`).

### Run tests
```bash
pip install -r requirements-dev.txt
pytest -q
```

## 4. Demo walkthrough

1. Select **Load sample enquiry** or enter a new enquiry.
2. Click **Analyze enquiry**.
3. Review the predicted service line, priority, confidence, extracted needs, and explanation.
4. Review the discovery questions and editable email draft.
5. Use the export button to download the analysis as JSON.

Try:
- "We need an AI agent to qualify inbound leads and integrate with HubSpot."
- "Our ecommerce website has poor Core Web Vitals and organic traffic is declining."
- "We need a secure mobile application and backend APIs hosted on AWS."
- "We need to extract invoice data from PDF files and route approvals."

## 5. What is genuinely implemented vs. proposed

**Implemented now**
- Streamlit user interface
- Transparent rule-based service classification
- Heuristic priority recommendation
- Keyword-based requirement extraction
- Suggested discovery questions
- Editable acknowledgement draft
- JSON export
- Synthetic sample dataset
- Unit tests

**Proposed production enhancements**
- Train and evaluate a supervised classifier using consented, labelled historical enquiries.
- Add an LLM behind a provider abstraction for robust structured extraction and response drafting.
- Add retrieval-augmented generation (RAG) over approved service descriptions and case studies.
- Add CRM/email integrations only after authentication, authorization, audit logging and human approval are implemented.

The displayed confidence is a **heuristic score**, not a calibrated model probability. The current app is a working baseline PoC, not a production AI agent and not a trained ML model.

## 6. Suggested GitHub repository description

`AI opportunity assessment and a Streamlit proof of concept for AI-assisted lead qualification, service routing, and sales response drafting for Cynbit Technologies.`

Suggested topics: `python`, `streamlit`, `machine-learning`, `nlp`, `lead-scoring`, `ai-automation`, `business-analysis`, `proof-of-concept`.

## 7. Repository structure

```text
cynbit-ai-opportunity-challenge/
├── app.py
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── LICENSE
├── README.md
├── src/
│   ├── __init__.py
│   └── lead_intelligence.py
├── data/
│   └── sample_leads.csv
├── docs/
│   ├── AI_OPPORTUNITY_REPORT.md
│   ├── TECHNICAL_APPROACH.md
│   └── SOURCES_AND_ASSUMPTIONS.md
└── tests/
    └── test_lead_intelligence.py
```

## 8. Responsible use

- Use only enquiries that Cynbit is authorized to process.
- Minimize and redact personal or confidential information.
- Treat customer-submitted content as untrusted input.
- Never allow an AI-generated claim about pricing, delivery, guarantees or customer references without approved evidence.
- Require human review before external communication or CRM updates.
- Define retention, access controls, audit trails and deletion procedures before production deployment.

## 9. Disclaimer

This is an independent challenge project based on publicly available company information and synthetic demonstration data. It is not an official Cynbit product, and no access to Cynbit's internal systems, customer data, CRM, analytics or operational metrics was available. Business benefits in the report are hypotheses to validate in a pilot.
