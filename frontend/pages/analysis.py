import streamlit as st

st.title("Document Analysis")

# Get stored analysis result
result = st.session_state.get("analysis_result", None)

# If no result found
if result is None:
    st.warning("Please upload and analyze a document first.")
    st.stop()

# If result exists, show overview
st.subheader("Document Overview")
st.write(f"**Document Type:** {result.get('document_type', 'Unknown')}")
st.write(f"**Total Clauses Processed:** {len(result.get('analysis', []))}")

st.markdown("---")

# Show clause-wise analysis
analysis_items = result.get("analysis", [])

if not analysis_items:
    st.info("No clauses were found in the analyzed document.")
else:
    for i, item in enumerate(analysis_items, start=1):
        st.subheader(f"Clause {i}")

        st.write("**Clause Text**")
        st.write(item.get("clause", "No clause text available."))

        st.write("**Relevant Laws**")
        laws = item.get("laws", [])
        if isinstance(laws, list) and laws:
            for law in laws:
                if isinstance(law, dict):
                    st.write(f"- {law.get('law_name', 'Law')}: {law.get('description', '')}")
                else:
                    st.write(f"- {law}")
        else:
            st.write("No relevant laws found.")

        st.write("**Explanation**")
        st.write(item.get("explanation", "No explanation available."))

        st.write("**Risks**")
        risks = item.get("risks", [])
        if isinstance(risks, list):
            if risks:
                for risk in risks:
                    st.write(f"- {risk}")
            else:
                st.write("No major risks found.")
        else:
            st.write(risks)

        st.write("**Next Steps**")
        next_steps = item.get("next_steps", [])
        if isinstance(next_steps, list):
            if next_steps:
                for step in next_steps:
                    st.write(f"- {step}")
            else:
                st.write("No next steps available.")
        else:
            st.write(next_steps)

        st.markdown("---")