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

[data-testid="stMetric"]{
background:#16213E;
border:1px solid #2E4F7A;
border-radius:18px;
padding:20px;
box-shadow:0px 4px 15px rgba(0,0,0,0.3);
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
        "Traffic Intelligence Maps",
        "Enforcement Intelligence",
        "Live Risk Monitor",
        "Impact Simulator",
        "Model Health Monitor"  
    ]
)
st.markdown("""
<style>

/* Sidebar navigation cards */

div[role="radiogroup"] > label {

    width: 100% !important;
    min-height: 70px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    padding: 10px !important;
    margin-bottom: 10px !important;

    border-radius: 12px !important;

    text-align: center !important;

    white-space: normal !important;
    word-wrap: break-word !important;

    background: #1E293B;
    border: 1px solid #334155;
}

/* Hover */

div[role="radiogroup"] > label:hover {

    background: #2563EB;
    border-color: #60A5FA;
}

/* Selected */

div[role="radiogroup"] > label:has(input:checked) {

    background: #2563EB;
    border-color: #60A5FA;
}

</style>
""", unsafe_allow_html=True)
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
elif page == "Traffic Intelligence Maps":

    st.title("🗺️ Traffic Intelligence Center")

    st.markdown("""
    Unified visualization platform for parking violation analytics,
    hotspot detection and congestion forecasting.
    """)

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([
        "🔥 Violation Heatmap",
        "🚨 Risk Hotspots",
        "📈 Forecast Intelligence"
    ])

    # ==================================
    # HEATMAP
    # ==================================

    with tab1:

        c1, c2, c3 = st.columns(3)

        c1.metric("Records", "298K+")
        c2.metric("Coverage", "Bengaluru")
        c3.metric("Type", "Historical")

        st.info(
            "Historical parking violation density across Bengaluru."
        )

        with st.expander(
            "🔥 Click to View Heatmap",
            expanded=False
        ):

            with open(
                "maps/parking_heatmap.html",
                "r",
                encoding="utf-8"
            ) as f:

                html = f.read()

            st.components.v1.html(
                html,
                height=850,
                scrolling=True
            )

    # ==================================
    # RISK MAP
    # ==================================

    with tab2:

        c1, c2, c3 = st.columns(3)

        c1.metric("Critical Hotspots", "10")
        c2.metric("High Risk Zones", "20")
        c3.metric("Ranking", "EPI")

        st.warning(
            "Hotspots ranked using Enforcement Priority Index."
        )

        with st.expander(
            "🚨 Click to View Risk Map",
            expanded=False
        ):

            with open(
                "maps/risk_map.html",
                "r",
                encoding="utf-8"
            ) as f:

                html = f.read()

            st.components.v1.html(
                html,
                height=850,
                scrolling=True
            )

    # ==================================
    # FORECAST
    # ==================================

    with tab3:

        st.success(
            "Tomorrow's forecasted parking congestion hotspots."
        )

        top_forecast = (
            forecast
            .sort_values(
                "expected_violations",
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            top_forecast,
            x="junction_name",
            y="expected_violations",
            color="expected_violations",
            title="Forecasted Hotspots"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            top_forecast,
            use_container_width=True
        )
        st.markdown("""
<style>

button[data-baseweb="tab"] {
    width: 100%;
    font-size: 18px;
    font-weight: 600;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
}

.stTabs [data-baseweb="tab"] {
    height: 60px;
}

</style>
""", unsafe_allow_html=True)
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
elif page == "Enforcement Intelligence":

    st.title("🚓 Enforcement Intelligence Center")

    st.markdown("""
    Unified enforcement analytics including deployment planning
    and repeat offender identification.
    """)

    st.markdown("---")

    tab1, tab2 = st.tabs([
        "🚓 Deployment Planner",
        "🚨 Repeat Offenders"
    ])
    st.markdown("""
<style>

/* Make tabs occupy full width */

.stTabs [data-baseweb="tab-list"] {
    display: flex;
    width: 100%;
}

.stTabs [data-baseweb="tab"] {
    flex-grow: 1;
    text-align: center;
    justify-content: center;
    font-size: 18px;
    font-weight: 600;
    height: 60px;
}

/* Selected tab */

.stTabs [aria-selected="true"] {
    background-color: #1E293B;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

    # ==================================
    # DEPLOYMENT PLANNER
    # ==================================

    with tab1:

        st.info(
            "AI-generated enforcement deployment recommendations."
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "High Risk Locations",
            len(
                planner[
                    planner["risk"] == "HIGH"
                ]
            )
        )

        c2.metric(
            "Medium Risk Locations",
            len(
                planner[
                    planner["risk"] == "MEDIUM"
                ]
            )
        )

        c3.metric(
            "Recommendations",
            len(planner)
        )

        st.dataframe(
            planner[
                [
                    "junction_name",
                    "expected_violations",
                    "EPI",
                    "risk",
                    "recommendation"
                ]
            ].head(20),
            use_container_width=True
        )

    # ==================================
    # REPEAT OFFENDERS
    # ==================================

    with tab2:

        st.warning(
            "Vehicles with repeated parking violations."
        )

        fig = px.bar(
            repeat.head(15),
            x="vehicle_number",
            y="violations",
            color="violations",
            title="Top Repeat Offenders"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            repeat.head(20),
            use_container_width=True
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
elif page == "Impact Simulator":

    st.title("🎯 Enforcement Impact Simulator")

    st.markdown("""
    Simulate the impact of deploying enforcement resources
    at high-risk parking hotspots.
    """)

    hotspot = st.selectbox(
        "Select Hotspot",
        sorted(
            forecast["junction_name"].unique()
        )
    )

    violations = st.slider(
        "Expected Violations",
        0,
        200,
        100
    )

    officers = st.slider(
        "Additional Officers Deployed",
        0,
        5,
        2
    )

    if st.button(
        "Run Simulation",
        use_container_width=True
    ):

        reduction = officers * 0.10

        reduction = min(
            reduction,
            0.50
        )

        reduced_violations = int(
            violations *
            (1 - reduction)
        )

        saved = (
            violations -
            reduced_violations
        )

        st.markdown("---")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Current Violations",
            violations
        )

        c2.metric(
            "Projected Violations",
            reduced_violations,
            delta=f"-{saved}"
        )

        c3.metric(
            "Reduction",
            f"{round(reduction*100)}%"
        )

        st.success(
            f"""
            Deploying {officers} additional officers at
            {hotspot} could reduce parking violations
            from {violations} to {reduced_violations}.
            """
        )

        st.info(
            "This simulation demonstrates how targeted enforcement can improve traffic conditions."
        )
elif page == "Model Health Monitor":

    st.title("🧠 Model Health Monitor")

    st.markdown("""
    Monitor model performance and detect changes in parking
    violation patterns that may require retraining.
    """)

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Model Version",
        "v1.0"
    )

    c2.metric(
        "Last Training",
        "Apr 2024"
    )

    c3.metric(
        "Training Records",
        "298K"
    )

    c4.metric(
        "Current Status",
        "Active"
    )

    st.markdown("---")

    st.subheader("Incoming Weekly Data")

    new_records = st.slider(
        "New Violation Records Received",
        0,
        50000,
        12000
    )

    pattern_change = st.slider(
        "Change in Violation Pattern (%)",
        0,
        100,
        15
    )

    st.markdown("---")

    if pattern_change >= 30:

        st.error("""
        ⚠ Significant Data Drift Detected

        Parking behaviour has changed substantially.
        Model retraining is recommended.
        """)

        st.subheader("Recommended Actions")

        st.markdown("""
        - Retrain Forecasting Model
        - Refresh Hotspot Rankings
        - Recalculate EPI Scores
        - Update Enforcement Recommendations
        """)

    elif pattern_change >= 15:

        st.warning("""
        Moderate pattern shift detected.

        Continue monitoring incoming data.
        """)

    else:

        st.success("""
        Model performance is stable.

        No retraining required.
        """)

    st.markdown("---")

    st.subheader("Continuous Learning Framework")

    st.markdown("""
    New Violation Data  
    ↓  
    Data Validation  
    ↓  
    Drift Detection  
    ↓  
    Model Retraining  
    ↓  
    Forecast Update  
    ↓  
    EPI Recalculation  
    ↓  
    Dashboard Refresh
    """)