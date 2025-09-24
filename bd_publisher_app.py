import streamlit as st
import json
import requests
import logging

st.title("🔍 OData GET Endpoint Explorer")

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

'Tenant selected: #', tenant, '#'
# 'Workspace_id selected: #', workspace_id, '#'

