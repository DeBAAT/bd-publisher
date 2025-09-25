import streamlit as st
import json
import requests
import logging

from BD_Publisher_OData_Func import BD_Publisher_OData_Func
from BD_Publisher_Swagger_Func import BD_Publisher_Swagger_Func

st.title("🔍 BD Publisher Functions")

# Session parameter for tenant and api_key
if "previous_option" not in st.session_state:
    st.session_state["previous_option"] = ""
if "tenant" not in st.session_state:
    st.session_state["tenant"] = ""
if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""

# Initialize Session State for params
if "params" not in st.session_state:
    st.session_state.params = {}

# Initialize Session State for swagger_data
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None
if "swagger_data" not in st.session_state:
    st.session_state.swagger_data = {}
if "uploaded_file_name" not in st.session_state:
    st.session_state["uploaded_file_name"] = "NONE2"

# Collect Authentication Inputs Once in the sidebar
st.sidebar.header("🔐 Authentication")
tenant = st.sidebar.text_input("tenant", value=st.session_state.get("tenant", ""))
api_key = st.sidebar.text_input("api_key", value=st.session_state.get("api_key", ""))

st.session_state["tenant"] = tenant
# tenant = st.session_state["tenant"]
# api_key = st.session_state["api_key"]

# Selection to call a function
options = ["Stop Processing", "OData", "Swagger"]
chosen_option = st.selectbox("Choose an option:", options)

# Initialize previous_option in session_state if not present
if "previous_option" not in st.session_state:
    st.session_state["previous_option"] = chosen_option

# Compare chosen_option to previous_option
if chosen_option == st.session_state["previous_option"]:
    st.write("You selected the same option as before.")
    if chosen_option == "Stop Processing":
        st.write("Processing stopped by user.")
    elif chosen_option == "OData":
        BD_Publisher_OData_Func(tenant,api_key)
    elif chosen_option == "Swagger":
        BD_Publisher_Swagger_Func(tenant,api_key)
else:
    st.write("You selected a different option.")
    st.session_state["previous_option"] = chosen_option

    # Call the selected function when button is pressed
    if st.button("Run Selected Function"):
        if chosen_option == "Stop Processing":
            st.write("Processing stopped by user.")
        elif chosen_option == "OData":
            BD_Publisher_OData_Func(tenant,api_key)
        elif chosen_option == "Swagger":
            BD_Publisher_Swagger_Func(tenant,api_key)
