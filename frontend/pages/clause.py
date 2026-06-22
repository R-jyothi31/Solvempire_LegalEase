import streamlit as st

st.title("Clause View")

# Get analysis result from session state
result = st.session_state.get("analysis_result", None)

# If no analysis result exists
if result is None:
    st.warning("Please upload and analyze a document first.")
    st.stop()

# Get clause analysis list
clauses = result.get("analysis", [])

# If no clauses found
if not clauses:
    st.info("No clauses found in the analyzed document.")
    st.stop()

# Show clause selector
clause_options = [f"Clause {i+1}" for i in range(len(clauses))]
selected_clause = st.selectbox("Select a Clause", clause_options)

# Get selected clause index
selected_index = clause_options.index(selected_clause)
clause_data = clauses[selected_index]

# Display selected clause details
st.subheader(selected_clause)

st.write("**Clause Text**")
st.write(clause_data.get("clause", "No clause text available."))

st.write("**Relevant Laws**")
laws = clause_data.get("laws", [])

if isinstance(laws, list) and laws:
    for law in laws:
        if isinstance(law, dict):
            st.write(f"- {law.get('law_name', 'Law')}: {law.get('description', '')}")
        else:
            st.write(f"- {law}")
else:
    st.write("No relevant laws found.")

st.write("**Explanation**")
st.write(clause_data.get("explanation", "No explanation available."))

st.write("**Risks**")
risks = clause_data.get("risks", [])

if isinstance(risks, list):
    if risks:
        for risk in risks:
            st.write(f"- {risk}")
    else:
        st.write("No major risks found.")
else:
    st.write(risks)

st.write("**Next Steps**")
next_steps = clause_data.get("next_steps", [])

if isinstance(next_steps, list):
    if next_steps:
        for step in next_steps:
            st.write(f"- {step}")
    else:
        st.write("No next steps available.")
else:
    st.write(next_steps)