import streamlit as st
from BD_Publisher_OData_Func import BD_Publisher_OData_Func
from BD_Publisher_Swagger_Func import BD_Publisher_Swagger_Func

st.title("BD Publisher Functions")

# Session parameter for Tenant
if "Tenant" not in st.session_state:
    st.session_state["Tenant"] = st.sidebar.text_input("Tenant")

tenant = st.session_state["Tenant"]

# Selection to call either function
option = st.radio("Select function to run:", ["OData", "Swagger"])

if st.button("Run Selected Function"):
    if option == "OData":
        BD_Publisher_OData_Func(tenant)
    elif option == "Swagger":
        BD_Publisher_Swagger_Func(tenant)
