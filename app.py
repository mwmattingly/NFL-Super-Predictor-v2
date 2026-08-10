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

st.write("Reached query section")

try:
    st.write("Step 1 - importing SQL connector")

    from databricks import sql

    st.write("Step 2 - connector imported")

    conn = sql.connect(
        server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        auth_type="oauth-m2m",
        client_id=os.getenv("DATABRICKS_CLIENT_ID"),
        client_secret=os.getenv("DATABRICKS_CLIENT_SECRET")
    )

    st.write("Step 3 - connected")

    cursor = conn.cursor()

    st.write("Step 4 - cursor created")

    cursor.execute("SELECT COUNT(*) FROM nfl.analytics.simulation_accuracy")

    st.write("Step 5 - query executed")

    result = cursor.fetchall()

    st.write("Step 6 - results fetched")

    st.write(result)

except Exception as e:
    st.error(f"ERROR: {e}")
