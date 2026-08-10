import streamlit as st
from pyspark.sql import SparkSession

# Page configuration
st.set_page_config(
    page_title="NFL Week 10 Predictions",
    page_icon="🏈",
    layout="wide"
)

# Create Spark session
spark = SparkSession.builder.getOrCreate()

# Title
st.title("🏈 NFL Week 10 Predictions")
