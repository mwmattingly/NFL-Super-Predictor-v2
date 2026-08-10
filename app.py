import streamlit as st
import pandas as pd
from pyspark.sql import SparkSession

# Page configuration
st.set_page_config(
    page_title="NFL Simulation Dashboard",
    page_icon="🏈",
    layout="wide"
)

# Title
st.title("🏈 NFL 2025 Season Simulation Dashboard")
st.markdown("---")

# Get Spark session
@st.cache_resource
def get_spark():
    """Get or create Spark session"""
    return SparkSession.builder.getOrCreate()

# Load data from Unity Catalog
@st.cache_data(ttl=300)
def load_simulation_data():
    """Load simulation accuracy data from Unity Catalog"""
    spark = get_spark()
    spark_df = spark.sql("""
        SELECT 
            Week,
            Day,
            HomeTeam,
            AwayTeam,
            HomeScore_Simulated,
            HomeScore_Actual,
            AwayScore_Simulated,
            AwayScore_Actual,
            HomeTO_Simulated,
            HomeTO_Actual,
            AwayTO_Simulated,
            AwayTO_Actual,
            HomeYds_Simulated,
            HomeYds_Actual,
            AwayYds_Simulated,
            AwayYds_Actual,
            Winner_Simulated,
            Winner_Actual,
            Correct_Winner,
            TravelDistance_Hours,
            EarlyGame_WestToEast,
            LateGame_EastToWest,
            GameTime_Local_Away,
            GameTime_Local_Home
        FROM nfl.analytics.simulation_accuracy
        ORDER BY Week, Day
    """)
    df = spark_df.toPandas()
    return df

try:
    df = load_simulation_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    weeks = sorted(df['Week'].unique())
    selected_weeks = st.sidebar.multiselect(
        "Select Week(s)",
        options=weeks,
        default=weeks
    )
    
    all_teams = sorted(set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique()))
    selected_teams = st.sidebar.multiselect(
        "Select Team(s)",
        options=all_teams,
        default=[]
    )
    
    travel_threshold = st.sidebar.slider(
        "Min Travel Distance (hours)",
        min_value=0.0,
        max_value=float(df['TravelDistance_Hours'].max()),
        value=0.0,
        step=0.5
    )
    
    # Filter data
    filtered_df = df[df['Week'].isin(selected_weeks)].copy()
    
    if selected_teams:
        filtered_df = filtered_df[
            filtered_df['HomeTeam'].isin(selected_teams) | 
            filtered_df['AwayTeam'].isin(selected_teams)
        ]
    
    if travel_threshold > 0:
        filtered_df = filtered_df[filtered_df['TravelDistance_Hours'] >= travel_threshold]
    
    # Key Metrics
    st.header("Model Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        accuracy = (filtered_df['Correct_Winner'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("Winner Prediction Accuracy", f"{accuracy:.2f}%")
    
    with col2:
        score_error = abs(filtered_df['HomeScore_Simulated'] - filtered_df['HomeScore_Actual']).mean()
        st.metric("Avg Score Error (Home)", f"{score_error:.2f} pts")
    
    with col3:
        yards_error = abs(filtered_df['HomeYds_Simulated'] - filtered_df['HomeYds_Actual']).mean()
        st.metric("Avg Yards Error (Home)", f"{yards_error:.2f} yds")
    
    with col4:
        to_error = abs(filtered_df['HomeTO_Simulated'] - filtered_df['HomeTO_Actual']).mean()
        st.metric("Avg Turnover Error (Home)", f"{to_error:.2f}")
    
    st.markdown("---")
    
    # Travel Fatigue Analysis
    st.header("Travel Fatigue Impact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        west_to_east = filtered_df[filtered_df['EarlyGame_WestToEast'] == True]
        if len(west_to_east) > 0:
            wte_accuracy = (west_to_east['Correct_Winner'].sum() / len(west_to_east) * 100)
            st.metric(
                "Early West→East Games Accuracy",
                f"{wte_accuracy:.1f}%",
                f"{len(west_to_east)} games"
            )
        else:
            st.info("No early West→East games in selection")
    
    with col2:
        east_to_west = filtered_df[filtered_df['LateGame_EastToWest'] == True]
        if len(east_to_west) > 0:
            etw_accuracy = (east_to_west['Correct_Winner'].sum() / len(east_to_west) * 100)
            st.metric(
                "Late East→West Games Accuracy",
                f"{etw_accuracy:.1f}%",
                f"{len(east_to_west)} games"
            )
        else:
            st.info("No late East→West games in selection")
    
    # Travel distance breakdown
    st.subheader("Prediction Accuracy by Travel Distance")
    travel_bins = pd.cut(filtered_df['TravelDistance_Hours'], bins=5)
    travel_accuracy = filtered_df.groupby(travel_bins, observed=True).agg({
        'Correct_Winner': ['sum', 'count']
    })
    travel_accuracy.columns = ['Correct', 'Total']
    travel_accuracy['Accuracy'] = (travel_accuracy['Correct'] / travel_accuracy['Total'] * 100).round(1)
    st.bar_chart(travel_accuracy['Accuracy'])
    
    st.markdown("---")
    
    # Detailed Results Table
    st.header("Detailed Simulation Results")
    st.caption(f"Showing {len(filtered_df)} games")
    
    # Format display dataframe
    display_df = filtered_df[[
        'Week', 'HomeTeam', 'AwayTeam',
        'HomeScore_Simulated', 'HomeScore_Actual',
        'AwayScore_Simulated', 'AwayScore_Actual',
        'Winner_Simulated', 'Winner_Actual', 'Correct_Winner',
        'HomeTO_Simulated', 'HomeTO_Actual',
        'HomeYds_Simulated', 'HomeYds_Actual',
        'TravelDistance_Hours', 'EarlyGame_WestToEast', 'LateGame_EastToWest'
    ]].copy()
    
    # Highlight correct predictions
    def highlight_correct(row):
        if row['Correct_Winner']:
            return ['background-color: lightgreen'] * len(row)
        else:
            return ['background-color: lightcoral'] * len(row)
    
    styled_df = display_df.style.apply(highlight_correct, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Export option
    st.download_button(
        label="Download Results as CSV",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name='nfl_simulation_results.csv',
        mime='text/csv'
    )
    
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Please ensure the nfl.analytics.simulation_accuracy table exists and is accessible.")
