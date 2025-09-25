import streamlit as st
import json
import requests
import logging

from BD_Publisher_OData_Func import BD_Publisher_OData_Func
from BD_Publisher_Swagger_Func import BD_Publisher_Swagger_Func

st.title("🔍 BD Publisher Functions")

# Collect Authentication Inputs Once in the sidebar
st.sidebar.header("🔐 Authentication")
api_key = st.sidebar.text_input("api_key", type="password")
tenant = st.sidebar.text_input("Tenant")

# Session parameter for Tenant and api_key
if "Tenant" not in st.session_state:
    st.session_state["Tenant"] = st.sidebar.text_input("Tenant")
if "API_Key" not in st.session_state:
    st.session_state["API_Key"] = st.sidebar.text_input("API_Key", type="password")

tenant = st.session_state["Tenant"]
api_key = st.session_state["API_Key"]

# Selection to call either function
option = st.radio("Select function to run:", ["OData", "Swagger"])

if st.button("Run Selected Function"):
    if option == "OData":
        BD_Publisher_OData_Func(tenant,api_key)
    elif option == "Swagger":
        BD_Publisher_Swagger_Func(tenant,api_key)
