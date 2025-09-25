import streamlit as st

st.title("Run OData or Swagger")
st.write(st.__version__)

# Track the selected file in session state
if "selected_file" not in st.session_state:
    st.session_state.selected_file = "bd_publisher_odata.py"

selected = st.radio("Select file to run:", ["bd_publisher_odata.py", "bd_publisher_swagger.py"], index=["bd_publisher_odata.py", "bd_publisher_swagger.py"].index(st.session_state.selected_file))

if selected != st.session_state.selected_file:
    st.session_state.selected_file = selected
    st.experimental_rerun()

st.write(f"Currently running: {st.session_state.selected_file}")

if st.session_state.selected_file == "bd_publisher_odata.py":
    import bd_publisher_odata
elif st.session_state.selected_file == "bd_publisher_swagger.py":
    import bd_publisher_swagger
