import os
import streamlit as st
import pandas as pd
from databricks import sql

st.set_page_config(
    page_title="NFL Simulation Accuracy",
    page_icon="🏈",
    layout="wide"
)

st.title("🏈 NFL Simulation Accuracy")

try:
    conn = sql.connect(
        server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_TOKEN")
    )

    query = """
    SELECT *
    FROM nfl.analytics.simulation_accuracy
    """

    df = pd.read_sql(query, conn)

    st.success(f"Retrieved {len(df):,} rows")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
