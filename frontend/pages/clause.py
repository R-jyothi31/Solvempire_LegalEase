import streamlit as st

st.title("Clause View")

result = st.session_state.get("analysis_result", None)

if result is None:
    st.warning("Please upload and analyze a document first.")
    st.stop()

for idx, item in enumerate(result["analysis"], start=1):
    with st.expander(f"Clause {idx}"):
        st.write("### Clause")
        st.write(item["clause"])

        st.write("### Explanation")
        st.write(item["explanation"])

        st.write("### Risks")
        for risk in item["risks"]:
            st.write(f"- {risk}")

        st.write("### Next Steps")
        for step in item["next_steps"]:
            st.write(f"- {step}")