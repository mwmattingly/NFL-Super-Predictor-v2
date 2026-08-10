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

host = os.getenv("DATABRICKS_HOST")
http_path = os.getenv("DATABRICKS_HTTP_PATH")
client_id = os.getenv("DATABRICKS_CLIENT_ID")
client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")

try:
    if not host:
        st.error("Missing DATABRICKS_HOST")
        st.stop()

    if not http_path:
        st.error("Missing DATABRICKS_HTTP_PATH")
        st.stop()

    if not client_id or not client_secret:
        st.error("Missing Databricks app service principal credentials")
        st.stop()

    server_hostname = host.replace("https://", "").replace("http://", "").rstrip("/")

    cfg = Config(
        host=host if host.startswith("http") else f"https://{host}",
        client_id=client_id,
        client_secret=client_secret
    )

    with sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        credentials_provider=oauth_service_principal(cfg)
    ) as conn:
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
