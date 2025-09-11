# Here is the complete Streamlit app script that allows you to:

# 1. Upload a Swagger JSON file.
# 2. Select an API endpoint from a dropdown.
# 3. View detailed information about the selected endpoint.
# [Download `swagger_explorer.py`]
import streamlit as st
import json

# 2. Extract Endpoint Details
def extract_endpoint_details(swagger_data):
    paths = swagger_data.get("paths", {})
    endpoint_info = {}
    for path, methods in paths.items():
        for method, details in methods.items():
            key = f"{method.upper()} {path}"
            endpoint_info[key] = {
                "summary": details.get("summary", ""),
                "description": details.get("description", ""),
                "parameters": details.get("parameters", []),
                "responses": details.get("responses", {})
            }
    return endpoint_info


# 1. Upload the Swagger JSON File
uploaded_file = st.file_uploader("Upload Swagger JSON", type="json")

if uploaded_file is not None:
    swagger_data = json.load(uploaded_file)

    # 3. Create Dropdown and Show Details
    endpoint_info = extract_endpoint_details(swagger_data)
    selected = st.selectbox("Select an API Endpoint", list(endpoint_info.keys()))

    if selected:
        details = endpoint_info[selected]
        st.markdown(f"### `{selected}`")
        st.write(f"**Summary:** {details['summary']}")
        st.write(f"**Description:** {details['description']}")

        st.write("**Parameters:**")
        if details["parameters"]:
            for param in details["parameters"]:
                name = param.get("name", "")
                location = param.get("in", "")
                required = param.get("required", False)
                param_type = param.get("type", param.get("schema", {}).get("type", ""))
                st.write(f"- `{name}` ({location}) - Required: {required}, Type: {param_type}")
        else:
            st.write("No parameters.")

        st.write("**Responses:**")
        for code, response in details["responses"].items():
            st.write(f"- `{code}`: {response.get('description', '')}")
