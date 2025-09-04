import streamlit as st
import numpy as np
import pandas as pd

st.title("🎈 BlueDolphin Publisher")
st.write(
    "Showing BlueDolphin information! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# Add a selectbox to the sidebar:
conn_region = st.sidebar.selectbox(
    'Region',
    ('EU', 'US')
)

# Add a text input to the sidebar:
conn_tenant = st.sidebar.text_input("Tenant", key="tenant")

# Add a text input to the sidebar:
conn_api_key = st.sidebar.text_input("x-api-key", key="api_key")

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

'Region selected: ', conn_region
'Tenant selected: #', conn_tenant, '#'
'x-api-key selected: #', conn_api_key, '#'
