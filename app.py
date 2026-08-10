import os
import streamlit as st

st.set_page_config(
    page_title="NFL Simulation Accuracy",
    page_icon="🏈",
    layout="wide"
)

st.title("🏈 NFL Simulation Accuracy")

for key in sorted(os.environ.keys()):
    if "DATABRICKS" in key.upper():
        st.write(key)
