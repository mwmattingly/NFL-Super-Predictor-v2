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
    conn = sql.connect(
        server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        auth_type="oauth-m2m",
        client_id=os.getenv("DATABRICKS_CLIENT_ID"),
        client_secret=os.getenv("DATABRICKS_CLIENT_SECRET")
    )

    query = """
    SELECT *
    FROM nfl.analytics.simulation_accuracy
    LIMIT 1000
    """

    df = pd.read_sql(query, conn)

    st.success(f"Retrieved {len(df):,} rows")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {e}")
