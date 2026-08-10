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
