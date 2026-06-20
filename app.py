import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Parking Impact Intelligence System",
    layout="wide"
)

epi = pd.read_csv("epi_hotspots.csv")
forecast = pd.read_csv("tomorrow_hotspots.csv")
repeat = pd.read_csv("repeat_offenders.csv")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Overview",
        "Heatmap",
        "Risk Map",
        "EPI Hotspots",
        "Forecast",
        "Enforcement Planner",
        "Repeat Offenders"
    ]
)
# =========================
# CREATE ENFORCEMENT TABLE
# =========================

planner = forecast.copy()

epi_lookup = (
    epi[
        [
            "junction_name",
            "EPI"
        ]
    ]
)

planner = planner.merge(
    epi_lookup,
    on="junction_name",
    how="left"
)

def get_risk(v):

    if v >= 100:
        return "HIGH"

    elif v >= 50:
        return "MEDIUM"

    else:
        return "LOW"

planner["risk"] = (
    planner["expected_violations"]
    .apply(get_risk)
)

def get_recommendation(row):

    if row["risk"] == "HIGH":

        return (
            "Deploy 3 officers + "
            "continuous monitoring"
        )

    elif row["risk"] == "MEDIUM":

        return (
            "Deploy 2 officers "
            "during peak hours"
        )

    else:

        return (
            "Routine patrol"
        )

planner["recommendation"] = (
    planner.apply(
        get_recommendation,
        axis=1
    )
)

def get_reason(row):

    if row["risk"] == "HIGH":

        return (
            "High predicted violations "
            "and hotspot activity"
        )

    elif row["risk"] == "MEDIUM":

        return (
            "Moderate congestion risk"
        )

    else:

        return (
            "Low expected activity"
        )

planner["reason"] = (
    planner.apply(
        get_reason,
        axis=1
    )
)

planner = planner.sort_values(
    "expected_violations",
    ascending=False
)
if page == "Overview":

    st.title("🚓 Parking Impact Intelligence System")
    st.markdown("""
    ### AI-driven Parking Impact Intelligence System

    This system analyzes parking violation patterns,
    predicts future congestion hotspots,
    identifies repeat offenders,
    and recommends enforcement deployment
    using machine learning and geospatial analytics.
    """)
    c1,c2,c3 = st.columns(3)

    c1.metric("Violations","298,450")
    c2.metric("Police Stations","54")
    c3.metric("Junctions","169")

elif page == "Heatmap":

    st.title("🔥 Parking Violation Heatmap")

    st.markdown("""
    Historical parking violation density across Bangalore.
    Areas with higher concentration of violations appear as hotspots.
    """)

    with open("parking_heatmap.html", "r", encoding="utf-8") as f:
        html = f.read()

    st.components.v1.html(
        html,
        height=700,
        scrolling=True
    )
elif page == "Risk Map":

    st.title("🗺️ Bangalore Risk Map")

    with open("risk_map.html", "r", encoding="utf-8") as f:
        html = f.read()

    st.components.v1.html(
        html,
        height=700,
        scrolling=True
    )
elif page == "EPI Hotspots":

    st.title("🔥 Enforcement Priority Index")

    fig = px.bar(
        epi.head(10),
        x="junction_name",
        y="EPI",
        color="EPI"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        epi.head(20)
    )

elif page == "Forecast":

    st.title("📈 Tomorrow Risk Forecast")

    fig = px.bar(
        forecast.head(15),
        x="junction_name",
        y="expected_violations",
        color="expected_violations"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        forecast.head(20)
    )
elif page == "Enforcement Planner":

    st.title(
        "🚓 Enforcement Planner"
    )

    st.markdown("""
    AI-generated enforcement deployment
    recommendations based on forecasted
    parking violations and hotspot risk.
    """)

    st.dataframe(
        planner[
            [
                "junction_name",
                "expected_violations",
                "EPI",
                "risk",
                "recommendation",
                "reason"
            ]
        ].head(20),
        use_container_width=True
    )
elif page == "Repeat Offenders":

    st.title("🚨 Repeat Offenders")

    fig = px.bar(
        repeat.head(20),
        x="vehicle_number",
        y="violations",
        color="violations"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        repeat.head(20)
    )