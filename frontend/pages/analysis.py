import streamlit as st

st.title("Document Analysis")

result = st.session_state.get("analysis_result", None)

if result is None:
    st.warning("Please upload and analyze a document first.")
    st.stop()

st.subheader("Document Overview")
st.write(f"**Document Type:** {result['document_type']}")
st.write(f"**Total Clauses Processed:** {len(result['analysis'])}")

st.markdown("---")

for idx, item in enumerate(result["analysis"], start=1):
    st.markdown(f"## Clause {idx}")

    st.markdown("### Clause Text")
    st.write(item["clause"])

    st.markdown("### Relevant Laws")
    for law in item["laws"]:
        st.write(f"**Source:** {law['source']}")
        st.write(law["law_text"])
        st.markdown("---")

    st.markdown("### Explanation")
    st.write(item["explanation"])

    st.markdown("### Risks")
    for risk in item["risks"]:
        st.error(risk)

    st.markdown("### Next Steps")
    for step in item["next_steps"]:
        st.write(f"- {step}")

    st.markdown("----")