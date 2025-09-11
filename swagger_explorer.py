import streamlit as st
import json
import requests

st.title("🔍 Swagger GET Endpoint Explorer")

# Collect Authentication Inputs Once in the sidebar
st.sidebar.header("🔐 Authentication")
api_key = st.sidebar.text_input("API Key", type="password")
tenant = st.sidebar.text_input("Tenant")

# Initialize Session State for params
if "params" not in st.session_state:
    st.session_state.params = {}

# Store Headers in a Reusable Dictionary
def get_auth_headers(api_key, tenant):
    return {
        "x-api-key": api_key,
        "tenant": tenant,
        "Content-Type": "application/json"
    }


# Step 1: Upload Swagger JSON file
uploaded_file = st.file_uploader("Upload Swagger JSON", type="json")

if uploaded_file is not None:
    swagger_data = json.load(uploaded_file)

    # Step 2: Extract GET endpoints
    def extract_get_endpoints(swagger_data):
        paths = swagger_data.get("paths", {})
        get_endpoints = []
        for path, methods in paths.items():
            if "get" in methods:
                get_endpoints.append(f"GET {path}")
        return sorted(get_endpoints)

    get_endpoints = extract_get_endpoints(swagger_data)

    # Step 3: Dropdown to select endpoint
    selected_endpoint = st.selectbox("Select a GET Endpoint", get_endpoints)

    # Step 4: Extract parameters for selected endpoint
    def get_parameters(swagger_data, selected_endpoint):
        method, path = selected_endpoint.split(" ", 1)
        endpoint_data = swagger_data["paths"].get(path, {}).get(method.lower(), {})
        return endpoint_data.get("parameters", [])

    parameters = get_parameters(swagger_data, selected_endpoint)

    # Step 5: Render input fields dynamically
    st.subheader("Enter Parameters")
    user_inputs = {}
    for param in parameters:
        name = param.get("name")
        location = param.get("in")
        required = param.get("required", False)
        param_type = param.get("type", param.get("schema", {}).get("type", "string"))

        label = f"{name} ({location})"
        if param_type == "string":
            user_inputs[name] = st.text_input(label, value=st.session_state.params.get(name, ""))
        elif param_type == "integer":
            user_inputs[name] = st.number_input(label, value=st.session_state.params.get(name, 0))
        elif param_type == "boolean":
            user_inputs[name] = st.checkbox(label, value=st.session_state.params.get(name, False))

    # Save inputs to session state
    st.session_state.params.update(user_inputs)

    # Step 6: Call the endpoint when button is pressed
    if st.button("Call Endpoint"):
        method, path = selected_endpoint.split(" ", 1)
        base_url = "https://public-api.eu.bluedolphin.app"
        url = f"{base_url}{path}"

        # Replace path parameters
        for param in parameters:
            if param.get("in") == "path":
                name = param.get("name")
                value = user_inputs.get(name)
                if value:
                    url = url.replace(f"{{{name}}}", str(value))

        # Build query parameters
        query_params = {}
        for param in parameters:
            if param.get("in") == "query":
                name = param.get("name")
                value = user_inputs.get(name)
                if value != "":
                    query_params[name] = value

        # Build headers
        # headers = {}
        # for param in parameters:
            # if param.get("in") == "header":
                # name = param.get("name")
                # value = user_inputs.get(name)
                # if value != "":
                    # headers[name] = value

        try:
            # Use Headers in Every API Call
            headers = get_auth_headers(api_key, tenant)
            response = requests.get(url, headers=headers, params=query_params)
            response.raise_for_status()
            st.subheader("Response")
            st.json(response.json())
        except Exception as e:
            st.error(f"API call failed: {e}")

'Tenant selected: #', tenant, '#'
# 'Workspace_id selected: #', workspace_id, '#'
