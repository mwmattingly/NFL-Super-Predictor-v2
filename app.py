import os
import pandas as pd
import streamlit as st
from databricks import sql
from databricks.sdk.core import Config, oauth_service_principal

st.set_page_config(
    page_title="NFL Simulation Accuracy",
    page_icon="🏈",
    layout="wide"
)

st.title("🏈 NFL Simulation Accuracy")

server_hostname = os.getenv("DATABRICKS_HOST")
http_path = os.getenv("DATABRICKS_HTTP_PATH")
client_id = os.getenv("DATABRICKS_CLIENT_ID")
client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")

if server_hostname:
    server_hostname = (
        server_hostname
        .replace("https://", "")
        .replace("http://", "")
        .rstrip("/")
    )

def credential_provider():
    config = Config(
        host=f"https://{server_hostname}",
        client_id=client_id,
        client_secret=client_secret
    )
    return oauth_service_principal(config)

try:
    if not server_hostname:
        st.error("Missing DATABRICKS_HOST")
        st.stop()

    if not http_path:
        st.error("Missing DATABRICKS_HTTP_PATH")
        st.stop()

    if not client_id or not client_secret:
        st.error("Missing Databricks app credentials")
        st.stop()

    with sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        credentials_provider=credential_provider
    ) as conn:

    query = """
    SELECT
        week,
        COUNT(*) AS games,
        SUM(moneylinecorrect) AS correct_picks,
        ROUND(100.0 * AVG(moneylinecorrect), 2) AS pct_correct
    FROM nfl.analytics.simulation_accuracy
    GROUP BY week
    ORDER BY week
    """
    
    df = pd.read_sql(query, conn)
    
    st.subheader("Moneyline Prediction Accuracy by Week")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {e}")
