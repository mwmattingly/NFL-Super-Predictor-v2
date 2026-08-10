import os
import streamlit as st

st.set_page_config(
    page_title="NFL Simulation Accuracy",
    page_icon="🏈",
    layout="wide"
)

st.title("🏈 NFL Simulation Accuracy")

st.write("HOST =", os.getenv("DATABRICKS_HOST"))
st.write("CLIENT_ID exists =", os.getenv("DATABRICKS_CLIENT_ID") is not None)
st.write("CLIENT_SECRET exists =", os.getenv("DATABRICKS_CLIENT_SECRET") is not None)
st.write("HTTP_PATH =", os.getenv("DATABRICKS_HTTP_PATH"))

# Show a small portion of the values so we know they're populated
host = os.getenv("DATABRICKS_HOST")
client_id = os.getenv("DATABRICKS_CLIENT_ID")

if host:
    st.write("Host starts with:", host[:20])

if client_id:
    st.write("Client ID starts with:", client_id[:8])
