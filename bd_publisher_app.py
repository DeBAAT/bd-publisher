import streamlit as st
import json
import requests
import logging

st.title("🔍 OData Endpoint Explorer")

# Collect Authentication Inputs Once in the sidebar
st.sidebar.header("🔐 Authentication")
api_key = st.sidebar.text_input("Authorization", type="password")
tenant = st.sidebar.text_input("Tenant")

# Add sidebar inputs for OData parameters
top = st.sidebar.number_input("Top", min_value=1, value=st.session_state.get("top", 10))
filter = st.sidebar.text_input("Filter", value=st.session_state.get("filter", ""), help="Enter OData filter string in single quotes, e.g. 'Name eq \'Test\''")

# Store param values in session_state
st.session_state["top"] = top
st.session_state["filter"] = filter

# Function to construct OData Headers using api_key
def get_auth_headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

# Function to construct OData URL using tenant
def get_odata_url(tenant, path=""):
    """
    Construct the OData URL using the tenant parameter.
    Default path is ''.
    """
    base_url = f"https://{tenant}.odata.bluedolphin.app/"
    return f"{base_url}{path}"

# Initialize Session State for params
if "params" not in st.session_state:
    st.session_state.params = {}

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

# Create headers and odata_url
headers = get_auth_headers(api_key)
odata_url = get_odata_url(tenant, "Objects")

# Build OData query parameters
params = {"$top": top}
if filter:
    params["$filter"] = filter

# Get the response from the odata_url
try:

    # Call the endpoint when button is pressed
    if st.button("Call Endpoint"):
        # response = requests.get(odata_url, headers=headers)
        response = requests.get(odata_url, auth=(tenant, api_key), params=params)
        response.raise_for_status()
        data = response.json()

        # Show the object_title of the main object
        show_label_element(data, "Object Title", "object_title")

        # Show full JSON response in a collapsible section
        with st.expander("Show Full JSON Response"):
            st.json(data)

except Exception as e:
    st.error(f"API call failed: {e}")

'Tenant selected: #', tenant, '#'
'odata_url created: #', odata_url, '#'
'headers created: #', headers, '#'
# 'Workspace_id selected: #', workspace_id, '#'

