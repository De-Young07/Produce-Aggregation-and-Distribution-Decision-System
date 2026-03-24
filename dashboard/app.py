import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Get absolute path to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Force add to Python path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print("DEBUG PATH:", PROJECT_ROOT)
print("SYS PATH:", sys.path)

from src.utils.database import get_db_connection

st.set_page_config(layout="wide")

st.title("Agricultural Forecasting Dashboard")


@st.cache_data
def load_data():

    conn = get_db_connection()

    query = """
    SELECT * FROM forecasts
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


df = load_data()

# Sidebar filters
crop = st.sidebar.selectbox("Select Crop", df["crop"].unique())
market = st.sidebar.selectbox("Select Market", df["market"].unique())

filtered = df[
    (df["crop"] == crop) &
    (df["market"] == market)
]

st.subheader(f"{crop} in {market}")

# Forecast Plot
fig = px.line(
    filtered,
    x="date",
    y="forecast_value",
    title="Forecast Trend"
)

st.plotly_chart(fig, width=True)

# Metrics
st.metric("Average Forecast", round(filtered["forecast_value"].mean(), 2))
st.metric("Max Forecast", round(filtered["forecast_value"].max(), 2))

# Table
st.dataframe(filtered)


@st.cache_data
def load_optimization_data():

    conn = get_db_connection()

    query = "SELECT * FROM optimization_results"

    df = pd.read_sql(query, conn)

    conn.close()

    return df

opt_df= load_optimization_data()

st.subheader("Optimal Distribution")

st.dataframe(opt_df)

fig2 = px.bar(
    opt_df,
    x="market",
    y="optimal_quantity",
    color="crop",
    title="Optimal Supply Allocation"
)

st.plotly_chart(fig2, width=True)