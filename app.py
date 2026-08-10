import os
import pandas as pd
import streamlit as st
from databricks import sql

st.set_page_config(
    page_title="NFL Simulation Accuracy",
    page_icon="🏈",
    layout="wide"
)

st.title("🏈 NFL Simulation Accuracy")

st.write("HOST =", os.getenv("DATABRICKS_HOST"))
st.write("CLIENT ID exists =", os.getenv("DATABRICKS_CLIENT_ID") is not None)
st.write("CLIENT SECRET exists =", os.getenv("DATABRICKS_CLIENT_SECRET") is not None)

conn = sql.connect(
    server_hostname=os.getenv("DATABRICKS_HOST").replace("https://", ""),
    http_path=os.getenv("DATABRICKS_HTTP_PATH"),
    auth_type="oauth-m2m",
    client_id=os.getenv("DATABRICKS_CLIENT_ID"),
    client_secret=os.getenv("DATABRICKS_CLIENT_SECRET")
)

import socket
socket.setdefaulttimeout(30)
