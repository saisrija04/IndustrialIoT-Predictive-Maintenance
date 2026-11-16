from src.maintenance_logger import log_maintenance
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

from streamlit_autorefresh import st_autorefresh
from src.sensor_simulator import generate_sensor_reading

# Page configuration
st.set_page_config(
    page_title="Industrial IoT Predictive Maintenance",
    page_icon="🏭",
    layout="wide"
)

# Load model and dataset
model = joblib.load("models/predictive_maintenance_model.pkl")
df = pd.read_csv("data/machine_data.csv")

# Automatic refresh every 5 seconds
refresh_count = st_autorefresh(
    interval=5000,
    key="sensor_refresh"
)

# Store sensor history
if "sensor_history" not in st.session_state:
    st.session_state.sensor_history = []

# Generate new sensor reading
reading = generate_sensor_reading()

st.session_state.sensor_history.append(reading)

# Keep the latest 50 readings
st.session_state.sensor_history = (
    st.session_state.sensor_history[-50:]
)

# Prepare sensor data for prediction
machine_data = pd.DataFrame([{
    "temperature": reading["temperature"],
    "vibration": reading["vibration"],
    "rpm": reading["rpm"],
    "operating_hours": reading["operating_hours"]
}])

prediction = model.predict(machine_data)[0]
probability = model.predict_proba(machine_data)[0][1]

# Dashboard heading
st.title("🏭 Industrial IoT Predictive Maintenance")
st.subheader("Real-Time Machine Health Monitoring")
st.caption("Simulated industrial sensor monitoring | Refresh every 5 seconds")

st.divider()

# Historical dataset metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Training Readings", len(df))
col2.metric("Normal Training Readings", int((df["failure"] == 0).sum()))
col3.metric("Failure Training Readings", int((df["failure"] == 1).sum()))

st.divider()

# Live sensor readings
st.subheader("⚙️ Live Machine Sensor Monitoring")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Temperature", f'{reading["temperature"]} °C')
c2.metric("Vibration", f'{reading["vibration"]}')
c3.metric("Motor Speed", f'{reading["rpm"]} RPM')
c4.metric("Operating Hours", reading["operating_hours"])

st.caption(f'Last updated: {reading["timestamp"]}')

st.divider()

# Predictive maintenance result

# Predictive maintenance result
st.subheader("🔍 Predictive Maintenance Result")

col1, col2 = st.columns(2)

col1.metric(
    "Failure Probability",
    f"{probability * 100:.2f}%"
)

# Determine machine health status
if prediction == 1:
    health_status = "CRITICAL"
    recommendation = "Stop and inspect the machine before further operation."
elif (
    reading["temperature"] > 80
    or reading["vibration"] > 5.5
    or reading["rpm"] > 1800
):
    health_status = "WARNING"
    recommendation = "Schedule a maintenance inspection."
else:
    health_status = "NORMAL"
    recommendation = "Continue routine machine monitoring."

# Display status
if health_status == "CRITICAL":
    col2.error("🔴 CRITICAL MACHINE CONDITION")
    st.error("High failure risk detected!")

elif health_status == "WARNING":
    col2.warning("🟡 MACHINE WARNING")
    st.warning("Abnormal sensor readings detected.")

else:
    col2.success("🟢 MACHINE CONDITION NORMAL")
    st.success("Machine readings are within the monitoring limits.")

st.write("**Maintenance Recommendation:**")
st.info(recommendation)

st.progress(float(probability))
# Save warning and critical maintenance events
if health_status in ["WARNING", "CRITICAL"]:

    last_logged = st.session_state.get("last_logged")

    current_event = (
        health_status,
        reading["timestamp"]
    )

    if last_logged != current_event:
        log_maintenance(
            reading,
            health_status,
            probability,
            recommendation
        )

        st.session_state.last_logged = current_event


st.divider()

# Historical sensor charts
st.subheader("📊 Real-Time Sensor Trends")

history_df = pd.DataFrame(st.session_state.sensor_history)

fig1 = px.line(
    history_df,
    x="timestamp",
    y="temperature",
    title="Temperature Trend (°C)",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(
    history_df,
    x="timestamp",
    y="vibration",
    title="Vibration Trend",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

fig3 = px.line(
    history_df,
    x="timestamp",
    y="rpm",
    title="Motor Speed Trend (RPM)",
    markers=True
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

st.subheader("📋 Latest Sensor Readings")
st.dataframe(
    history_df.tail(10).iloc[::-1],
    use_container_width=True
)

st.caption(
    "Industrial IoT Predictive Maintenance | "
    "Machine Learning | Simulated Sensor Data"
)
# Maintenance History
st.divider()
st.subheader("🛠️ Maintenance History")

import os

if os.path.exists("data/maintenance_history.csv"):

    maintenance_df = pd.read_csv(
        "data/maintenance_history.csv"
    )

    st.dataframe(
        maintenance_df.tail(20).iloc[::-1],
        use_container_width=True
    )

    st.metric(
        "Total Maintenance Events",
        len(maintenance_df)
    )
    
    # Download Maintenance Report
    st.subheader("📥 Download Maintenance Report")

    csv_data = maintenance_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Maintenance Report (CSV)",
        data=csv_data,
        file_name="industrial_maintenance_report.csv",
        mime="text/csv"
    )


    # Maintenance Analytics
    st.divider()
    st.subheader("📊 Maintenance Analytics")

    status_counts = (
        maintenance_df["health_status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = ["Health Status", "Count"]

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            status_counts,
            names="Health Status",
            values="Count",
            title="Maintenance Events by Status",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            status_counts,
            x="Health Status",
            y="Count",
            title="Maintenance Event Summary",
            text="Count"
        )
        st.plotly_chart(fig, use_container_width=True)
    

else:
    st.info("No maintenance events recorded yet.")
