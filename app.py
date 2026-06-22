import streamlit as st
import pandas as pd
import plotly.express as px
from catboost import CatBoostRegressor

st.set_page_config(
    page_title="Parking Impact Intelligence System",
    layout="wide"
)
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

[data-testid="stMetric"] {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 15px;
    padding: 15px;
    text-align: center;
}

h1 {
    color: #F8FAFC;
}

h2, h3 {
    color: #E2E8F0;
}

</style>
""", unsafe_allow_html=True)

epi = pd.read_csv("data/epi_hotspots.csv")
forecast = pd.read_csv("data/tomorrow_hotspots.csv")
repeat = pd.read_csv("data/repeat_offenders.csv")

model = CatBoostRegressor()

model.load_model(
    "models/parking_forecast_model.cbm"
)
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Home",
        "Heatmap",
        "Risk Map",
        "EPI Hotspots",
        "Forecast",
        "Enforcement Planner",
        "Repeat Offenders",
        "Live Risk Monitor"
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

if page == "Home":

    st.title("🚓 Parking Impact Intelligence System")

    st.caption(
        "AI-Driven Detection, Forecasting and Enforcement Planning for Parking-Induced Congestion"
    )

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Violations", "298,450")
    c2.metric("Police Stations", "54")
    c3.metric("Junctions", "169")
    c4.metric("Hotspots", len(epi))

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success("Hotspot Detection")

    with col2:
        st.warning("📈 Violation Forecasting")

    with col3:
        st.info("🚓 Enforcement Planning")

    st.markdown("---")

    st.subheader("System Workflow")

    st.markdown("""
    Parking Violations → Hotspot Detection → Risk Analysis → Forecasting → EPI Scoring → Enforcement Recommendations
    """)
elif page == "Heatmap":

    st.title("Parking Violation Density Analysis")

    st.info(
        "This heatmap visualizes historical parking violation concentration across Bengaluru."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Records", "298K+")
    c2.metric("Locations", "10,942")
    c3.metric("Junctions", "169")

    st.markdown("---")
    with open("maps/parking_heatmap.html", "r", encoding="utf-8") as f:
        html = f.read()

    st.components.v1.html(
        html,
        height=700,
        scrolling=True
    )
elif page == "Risk Map":

    st.title("🗺️ High Risk Congestion Hotspots")

    st.warning(
        "Locations ranked using Enforcement Priority Index (EPI)."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Critical Hotspots", "10")
    c2.metric("High Risk Zones", "20")
    c3.metric("Forecast Enabled", "Yes")

    st.markdown("---")

    with open("maps/risk_map.html", "r", encoding="utf-8") as f:
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
    st.info(
    "Predicted parking violation intensity for upcoming high-risk locations."
)
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
    st.warning(
    "Vehicles with repeated parking violations requiring targeted enforcement."
)

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
elif page == "Live Risk Monitor":

    st.title("🚨 Live Risk Monitor")

    st.markdown("""
    ### AI-Powered Parking Risk Assessment

    Simulate future parking violation risk using the trained forecasting model.
    Select a location and time to generate real-time enforcement recommendations.
    """)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        police_station = st.selectbox(
            "🏢 Police Station",
            sorted(epi["police_station"].dropna().unique())
        )

        day = st.selectbox(
            "📅 Day",
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
            ]
        )

    with col2:

        junction = st.selectbox(
            "📍 Junction",
            sorted(epi["junction_name"].dropna().unique())
        )

        hour = st.slider(
            "🕒 Hour",
            0,
            23,
            18
        )

    st.markdown("")

    if st.button(
        "🚀 Generate Risk Assessment",
        use_container_width=True
    ):

        sample = pd.DataFrame({
            "police_station": [police_station],
            "junction_name": [junction],
            "day_of_week": [day],
            "hour": [hour]
        })

        pred = max(
            0,
            round(model.predict(sample)[0])
        )

        if pred >= 100:

            risk = "HIGH"

            recommendation = (
                "Deploy 3 officers and continuous monitoring"
            )

            color = "🔴"

        elif pred >= 50:

            risk = "MEDIUM"

            recommendation = (
                "Deploy 2 officers during peak hours"
            )

            color = "🟡"

        else:

            risk = "LOW"

            recommendation = (
                "Routine patrol"
            )

            color = "🟢"

        st.markdown("---")

        st.subheader("Risk Assessment Results")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Expected Violations",
            pred
        )

        c2.metric(
            "Risk Category",
            risk
        )

        c3.metric(
            "Selected Hour",
            hour
        )

        st.markdown("")

        if risk == "HIGH":

            st.error(
                f"{color} HIGH RISK LOCATION DETECTED"
            )

        elif risk == "MEDIUM":

            st.warning(
                f"{color} MODERATE RISK LOCATION"
            )

        else:

            st.success(
                f"{color} LOW RISK LOCATION"
            )

        st.markdown("### Recommended Action")

        st.info(
            recommendation
        )

        st.markdown("### Operational Summary")

        st.markdown(
            f"""
            - **Police Station:** {police_station}
            - **Junction:** {junction}
            - **Predicted Violations:** {round(pred)}
            - **Risk Level:** {risk}
            - **Recommended Action:** {recommendation}
            """
        )