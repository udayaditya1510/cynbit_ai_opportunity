import json
import pandas as pd
import streamlit as st

from src.lead_intelligence import analyze_lead, build_response_draft, SAMPLE_CATEGORIES

st.set_page_config(page_title="Cynbit | AI Lead Intelligence", page_icon="⚡", layout="wide")

st.title("⚡ Cynbit AI Lead Intelligence Copilot")
st.caption("Proof of concept • Explainable lead routing • Human-approved response drafting")

with st.sidebar:
    st.header("Demo controls")
    st.markdown("This PoC uses a transparent, deterministic baseline and synthetic examples.")
    mode = st.radio("Input mode", ["Load sample enquiry", "Enter enquiry"])
    st.divider()
    st.markdown("**Safety controls**")
    st.write("• No email is sent")
    st.write("• No CRM is modified")
    st.write("• Human review is required")
    st.write("• Do not enter sensitive data")

samples = pd.read_csv("data/sample_leads.csv")
if mode == "Load sample enquiry":
    sample_index = st.selectbox(
        "Choose a sample",
        range(len(samples)),
        format_func=lambda i: f"{samples.iloc[i]['company']} — {samples.iloc[i]['channel']}",
    )
    selected = samples.iloc[sample_index]
    company = str(selected["company"])
    channel = str(selected["channel"])
    message = str(selected["message"])
else:
    company = st.text_input("Company / contact", "Prospective client")
    channel = st.selectbox("Enquiry channel", ["Website", "Email", "Referral", "LinkedIn", "Other"])
    message = st.text_area(
        "Customer enquiry",
        "We need an AI assistant to qualify incoming leads and connect with our CRM.",
        height=150,
    )

analyze = st.button("Analyze enquiry", type="primary", disabled=not message.strip())

if analyze:
    result = analyze_lead(message, company=company, channel=channel)
    draft = build_response_draft(company, result)

    st.subheader("Analysis")
    c1, c2, c3 = st.columns(3)
    c1.metric("Suggested service", result["category"])
    c2.metric("Suggested priority", result["priority"])
    c3.metric("Heuristic confidence", f'{result["confidence"]:.0%}')

    st.info(
        "Prototype limitation: confidence is a transparent heuristic based on keyword evidence, "
        "not a calibrated ML probability. Confirm the recommendation before acting."
    )

    left, right = st.columns(2)
    with left:
        st.markdown("#### Why this recommendation?")
        st.write(result["explanation"] or "No strong keyword evidence; manual review recommended.")
        st.markdown("#### Extracted requirement signals")
        if result["signals"]:
            for signal in result["signals"]:
                st.write(f"• {signal}")
        else:
            st.write("No predefined requirement signals detected.")
        st.markdown("#### Recommended discovery questions")
        for question in result["discovery_questions"]:
            st.write(f"• {question}")

    with right:
        st.markdown("#### Suggested next step")
        st.write(result["next_action"])
        st.markdown("#### Human-reviewed response draft")
        edited_draft = st.text_area("Edit before use", draft, height=260)

    export = dict(result)
    export.update({
        "company": company,
        "channel": channel,
        "original_message": message,
        "response_draft": edited_draft,
        "status": "Needs human review",
    })
    st.download_button(
        "Download analysis as JSON",
        data=json.dumps(export, indent=2),
        file_name="cynbit_lead_analysis.json",
        mime="application/json",
    )

    with st.expander("Technical details"):
        st.json({
            "category_scores": result["category_scores"],
            "matched_terms": result["matched_terms"],
            "priority_reasons": result["priority_reasons"],
            "model": "explainable-keyword-baseline-v1",
        })

st.divider()
st.markdown("**Future production path:** labelled classifier → approved-content retrieval (RAG) → structured LLM extraction/drafting → policy checks → human approval → CRM integration.")
st.caption("Independent prototype for an AI opportunity challenge. Not an official Cynbit system.")
