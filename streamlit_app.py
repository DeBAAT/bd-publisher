import streamlit as st
import requests
import numpy as np
import pandas as pd
from collections import Counter

swagger_url = "https://public-api.eu.bluedolphin.app/swagger/v1/swagger.json"

st.title("🎈 BlueDolphin Publisher")
st.markdown("Welcome to the BlueDolphin Publisher app. Use the sidebar to configure your API connection and filter data.")

# Add a selectbox to the sidebar:
conn_region = st.sidebar.selectbox( 'Region', ('EU', 'US') )

# Add some text inputs to the sidebar:
conn_tenant = st.sidebar.text_input("Tenant", key="tenant")
conn_api_key = st.sidebar.text_input("x-api-key", key="api_key")
conn_workspace_id = st.sidebar.text_input("workspace_id", key="workspace_id")
conn_take = st.sidebar.number_input("take", key="take", format="%d", min_value=1, max_value=10000, value=5, step=1)
conn_show = st.sidebar.number_input("show", key="show", format="%d", min_value=1, max_value=10000, value=5, step=1)

# Add a slider to the sidebar:
range_values = st.sidebar.slider( 'Select a range of values:', 0.0, 100.0, (25.0, 70.0) )

# Function to fetch data from API
def fetch_data(region, tenant, api_key, workspace_id, take):
    url = f"https://public-api.{region.lower()}.bluedolphin.app/v1/objects?workspace_id={workspace_id.lower()}&take={take}"
    headers = {
        "tenant": tenant,
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

# Function to fetch endpoints from API swagger_url
def get_api_endpoints(swagger_url):
    response = requests.get(swagger_url)
    response.raise_for_status()
    swagger_data = response.json()

    paths = swagger_data.get("paths", {})
    endpoint_list = list(paths.keys())
    return sorted(endpoint_list)

# Fetch and display data
if st.button("Fetch Data"):
    data = fetch_data(conn_region, conn_tenant, conn_api_key, conn_workspace_id, conn_take)
    if data:
        st.subheader("Raw API Data")
        st.json(data)

        # Convert to DataFrame
        df = pd.DataFrame(data)

        st.subheader("All Items Table")
        st.dataframe(df.head(conn_show))  # Interactive table with sorting and filtering

        # Filter based on slider
        # if "type.name" in df.columns:
            # filtered_df = df[(df["type.name"] >= range_values[0]) & (df["type.name"] <= range_values[1])]
            # st.subheader("Filtered Data")
            # st.dataframe(filtered_df)

            # # Visualization
            # if "name" in filtered_df.columns:
                # st.subheader("Data Visualization")
                # chart = alt.Chart(filtered_df).mark_bar().encode(
                    # x='name:N',
                    # y='type name:Q'
                # )
                # st.altair_chart(chart, use_container_width=True)

        # Flatten the items
        df = pd.json_normalize(data["items"])

        st.subheader("All Items Normalized")
        st.dataframe(df.head(conn_show))  # Interactive table with sorting and filtering

        # Count items by type.name
        if "type.name" in df.columns:
            type_counts = Counter(df["type.name"])
            st.subheader("Item Counts by Type Name")
            st.write(type_counts)

            # type_df = pd.DataFrame(type_counts.items(), columns=["Type Name", "Count"])
            # type_chart = alt.Chart(type_df).mark_bar().encode(
                # x='Type Name:N',
                # y='Count:Q'
            # )
            # st.altair_chart(type_chart, use_container_width=True)
        else:
            st.warning("The API response does not contain a 'type.name' field for counting.")
    else:
        st.warning("No items found in the API response.")

'Region selected: ', conn_region
'Tenant selected: #', conn_tenant, '#'
'x-api-key selected: #', conn_api_key, '#'
'Workspace_id selected: #', conn_workspace_id, '#'
'Take selected: #', conn_take, '#'
'Show selected: #', conn_show, '#'
'Swagger_url used: #', swagger_url, '#'

# Add Dropdown to select an endpoint from the list found
try:
    endpoints = get_api_endpoints(swagger_url)
    selected_endpoint = st.selectbox("Select an API Endpoint", endpoints)
    st.write(f"You selected: `{selected_endpoint}`")
except Exception as e:
    st.error(f"Failed to load endpoints: {e}")

