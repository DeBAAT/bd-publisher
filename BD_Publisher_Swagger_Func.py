import streamlit as st
import json
import requests
import logging

# Store Headers in a Reusable Dictionary
def get_auth_headers(api_key, tenant):
    return {
        "x-api-key": api_key,
        "tenant": tenant,
        "Content-Type": "application/json"
    }

# Show the label and value of a data element
def show_label_element(data, element_label, element_key):
    """
    Display a header and the element title from the data dictionary.

    Parameters:
    - data: dict, the data containing the element information
    - element_label: str, the header to display
    - element_key: str, the key to use for retrieving the element from data
    """
    try:
        element_value = data.get(element_key, "Unknown Title")
        st.write(f"### {element_label}: {element_value}")
    except Exception as e:
        import logging
        logging.error(f"Error displaying element with key '{element_key}': {e}")
        st.error("Failed to display element_label.")

# Show table with information of related objects
def show_related_objects(data):
    try:
        related_objects = data.get("related_objects", [])
        if related_objects:
            st.write("### Related Objects")
            table_data = [
                {
                    "Relationship": obj.get("relationship", {}).get("name", "N/A"),
                    "Type Name": obj.get("type", {}).get("name", "N/A"),
                    "Object Title": obj.get("object_title", "N/A"),
                    "Object ID": obj.get("object_id", "N/A"),
                    "Relationship ID": obj.get("relationship_id", "N/A")
                }
                for obj in related_objects
            ]
            st.table(table_data)
        else:
            st.info("No related objects found.")
    except Exception as e:
        logging.error(f"Error displaying related objects: {e}")
        st.error("Failed to display related objects.")

# Upload and cache swagger data
def Get_Swagger_Data():
    # Upload Swagger JSON file
    uploaded_file = st.file_uploader("Upload Swagger JSON", type="json")

    if uploaded_file is not None:
        st.session_state["swagger_data"] = json.load(uploaded_file)
    # Retrieve from session_state if available
    return st.session_state.get("swagger_data", None)

# Extract GET endpoints from swagger data
def Extract_Endpoints(swagger_data):
    paths = swagger_data.get("paths", {})
    get_endpoints = []
    for path, methods in paths.items():
        if "get" in methods:
            get_endpoints.append(f"GET {path}")
    return sorted(get_endpoints)

# Extract parameters for selected endpoint
def Get_Endpoint_Parameters(swagger_data, selected_endpoint):
    method, path = selected_endpoint.split(" ", 1)
    endpoint_data = swagger_data["paths"].get(path, {}).get(method.lower(), {})
    return endpoint_data.get("parameters", [])

def BD_Publisher_Swagger_Func(tenant,api_key):
    st.write(f"Swagger Function called for tenant: {tenant}")
    session_tenant = st.session_state["tenant"]
    st.write(f"Swagger Function called for session value tenant: {session_tenant}")
    # Add Swagger logic here
    st.title("🔍 Swagger Endpoint Explorer")

    # Get and process swagger data from uploaded file
    # swagger_data = Get_Swagger_Data()
    # Upload Swagger JSON file
    # uploaded_file = st.file_uploader("Upload Swagger JSON", type="json")
    # Upload file if not already in session_state
    uploaded_file = st.file_uploader("Upload Swagger JSON", type="json")
#    if "uploaded_file" not in st.session_state or st.session_state["uploaded_file"] is None:
#        st.info("No file uploaded yet.")
#        uploaded_file = st.file_uploader("Upload Swagger JSON", type="json")
    if uploaded_file is not None:
        st.success("File is uploaded: {}".format(uploaded_file.name))
        swagger_data = json.load(uploaded_file)
        st.session_state["swagger_data"] = swagger_data
        # st.session_state["swagger_data"] = json.load(uploaded_file)
        # swagger_data =  st.session_state.get("swagger_data", None)
        st.session_state["uploaded_file_name"] = uploaded_file.name
        st.session_state["uploaded_file"] = uploaded_file
        uploaded_file_name2 = uploaded_file.name
        st.success(f"File2 is available: {uploaded_file_name2}")
    else:
        st.success("File is available!")
        #uploaded_file = st.session_state["uploaded_file"]
        uploaded_file_name = st.session_state["uploaded_file_name"]
        st.success(f"File is available: {uploaded_file_name}")
        # st.success("File is available: {}".format(uploaded_file.name))

    # Test if swagger_data is empty
    if not st.session_state["swagger_data"]:
        st.info("JSON swagger_data is empty.")
    else:
        st.success("JSON swagger_data is present!")

        # if uploaded_file is not None:
        # st.write(f"Swagger Function called for uploaded_file: {uploaded_file.name}")
        # st.session_state["swagger_data"] = json.load(uploaded_file)
        # swagger_data =  st.session_state.get("swagger_data", None)
        # if swagger_data is not None:
        # swagger_data = json.load(uploaded_file)
        get_endpoints = Extract_Endpoints(swagger_data)
        # Dropdown to select endpoint
        selected_endpoint = st.selectbox("Select a GET Endpoint", get_endpoints)
        parameters = Get_Endpoint_Parameters(swagger_data, selected_endpoint)
        st.write("Parameters for selected endpoint:", parameters)

        # Render input fields dynamically
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

        # Call the endpoint when button is pressed
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

            try:
                # Use Headers in Every API Call
                headers = get_auth_headers(api_key, tenant)
                response = requests.get(url, headers=headers, params=query_params)
                response.raise_for_status()

                # Step 7: Show the Related Objects when button is pressed
                data = response.json()

                # Show the object_title of the main object
                show_label_element(data, "Object Title", "object_title")

                # Show full JSON response in a collapsible section
                with st.expander("Show Full JSON Response"):
                    st.json(data)

                # Show related objects if available
                show_related_objects(data)

            except Exception as e:
                st.error(f"API call failed: {e}")

#     else:
#        st.info("Please upload a Swagger JSON file.")

    # Call the endpoint when button is pressed
    if st.button("Stop processing..."):
        st.write("Processing stopped by user.")
