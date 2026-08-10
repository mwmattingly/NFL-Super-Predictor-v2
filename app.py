import streamlit as st
from pyspark.sql import SparkSession

# Page configuration
st.set_page_config(
    page_title="NFL Week 10 Predictions",
    page_icon="🏈",
    layout="wide"
)

# Title
st.title("🏈 NFL Week 10 Predictions")

# Get Spark session
@st.cache_resource
def get_spark():
    return SparkSession.builder.getOrCreate()

# Load Week 10 predictions
@st.cache_data(ttl=300)
def load_week10_predictions():
    spark = get_spark()
    spark_df = spark.sql("""
        SELECT 
            HomeTeam,
            AwayTeam,
            HomeScore_Simulated,
            AwayScore_Simulated,
            Winner_Simulated
        FROM nfl.analytics.simulation_accuracy
        WHERE Week = 10
        ORDER BY Day
    """)
    return spark_df.toPandas()

try:
    df = load_week10_predictions()
    
    st.subheader(f"Total Games: {len(df)}")
    st.markdown("---")
    
    # Display predictions table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Please ensure the nfl.analytics.simulation_accuracy table exists and contains Week 10 data.")
