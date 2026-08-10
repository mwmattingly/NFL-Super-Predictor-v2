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
st.caption("Moneyline prediction accuracy from Unity Catalog")


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
            CAST(week AS INT) AS week,
            COUNT(*) AS games,
            SUM(moneylinecorrect) AS correct_picks,
            ROUND(100.0 * AVG(moneylinecorrect), 2) AS pct_correct
        FROM nfl.analytics.simulation_accuracy
        GROUP BY CAST(week AS INT)
        ORDER BY CAST(week AS INT)
        """

        df = pd.read_sql(query, conn)

    if df.empty:
        st.warning("No simulation accuracy records were returned.")
        st.stop()

    total_games = int(df["games"].sum())
    total_correct = int(df["correct_picks"].sum())
    overall_accuracy = (total_correct / total_games) * 100 if total_games else 0

    best_week_row = df.loc[df["pct_correct"].idxmax()]
    best_week = int(best_week_row["week"])
    best_week_accuracy = float(best_week_row["pct_correct"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Overall Moneyline Accuracy",
            value=f"{overall_accuracy:.1f}%"
        )

    with col2:
        st.metric(
            label="Correct Picks",
            value=f"{total_correct:,} of {total_games:,}"
        )

    with col3:
        st.metric(
            label="Best Week",
            value=f"Week {best_week}",
            delta=f"{best_week_accuracy:.1f}%"
        )

    st.divider()

    st.subheader("Weekly Accuracy Trend")

    chart_df = df.rename(
        columns={
            "week": "Week",
            "pct_correct": "Accuracy %"
        }
    ).set_index("Week")

    st.bar_chart(
        chart_df["Accuracy %"],
        use_container_width=True
    )

    st.subheader("Weekly Results")

    display_df = df.copy()
    display_df = display_df.rename(
        columns={
            "week": "Week",
            "games": "Games",
            "correct_picks": "Correct Picks",
            "pct_correct": "Accuracy %"
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Week": st.column_config.NumberColumn("Week", format="%d"),
            "Games": st.column_config.NumberColumn("Games", format="%d"),
            "Correct Picks": st.column_config.NumberColumn("Correct Picks", format="%d"),
            "Accuracy %": st.column_config.ProgressColumn(
                "Accuracy %",
                format="%.2f%%",
                min_value=0,
                max_value=100
            )
        }
    )

except Exception as e:
    st.error(f"Error loading data: {e}")
