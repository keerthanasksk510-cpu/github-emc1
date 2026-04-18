import streamlit as st
import pandas as pd
import numpy as np
import time
from streamlit_autorefresh import st_autorefresh

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="AI Motor Dashboard", layout="wide")

st.title("🚀 AI-Based Predictive Maintenance & Energy Dashboard")

# ==============================
# AUTO REFRESH (every 2 sec)
# ==============================
st_autorefresh(interval=2000, key="datarefresh")

# ==============================
# LOAD DATA (SIMULATION FILE)
# ==============================
df_stream = pd.read_csv("esp32_simulated_stream_dataset.csv")

# Simulate real-time index
if "index" not in st.session_state:
    st.session_state.index = 0

row = df_stream.iloc[st.session_state.index % len(df_stream)]
st.session_state.index += 1

# ==============================
# EXTRACT VALUES
# ==============================
vib = row['vibration']
temp = row['temperature']
curr = row['current']
power = row['power']
CO = row['CO']
traffic = row['traffic']

# ==============================
# TOP METRICS
# ==============================
st.subheader("🔧 Motor Parameters")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Vibration", f"{vib:.2f}")
col2.metric("Temperature (°C)", f"{temp:.2f}")
col3.metric("Current (A)", f"{curr:.2f}")
col4.metric("Power (W)", f"{power:.2f}")

# ==============================
# ENVIRONMENT DATA
# ==============================
st.subheader("🌍 Environmental Parameters")
col5, col6 = st.columns(2)

col5.metric("CO Level", f"{CO:.2f}")
col6.metric("Traffic Density", f"{traffic}")

# ==============================
# PREDICTIVE MAINTENANCE LOGIC
# ==============================
if temp > 80 or vib > 5:
    status = "🔴 Critical"
elif temp > 60:
    status = "🟠 Warning"
else:
    status = "🟢 Healthy"

st.subheader("🧠 Predictive Maintenance")
st.write(f"System Status: {status}")

if status == "🔴 Critical":
    st.error("Immediate maintenance required! Possible overheating or vibration issue.")
elif status == "🟠 Warning":
    st.warning("Schedule maintenance soon.")
else:
    st.success("System operating normally.")

# ==============================
# ENERGY OPTIMIZATION LOGIC
# ==============================
fan_speed = min(max((CO + traffic) / 2, 20), 100)
power_estimate = 230 * 0.85 * (fan_speed / 100) ** 3 * 10

st.subheader("⚡ Energy Optimization")
st.write(f"Recommended Fan Speed: {fan_speed:.2f}%")
st.write(f"Estimated Power Consumption: {power_estimate:.2f} W")

# ==============================
# LIVE CHART
# ==============================
st.subheader("📊 Live Sensor Trends")

history_size = 20

if "history" not in st.session_state:
    st.session_state.history = []

st.session_state.history.append({
    "vibration": vib,
    "temperature": temp,
    "current": curr,
    "power": power
})

if len(st.session_state.history) > history_size:
    st.session_state.history.pop(0)

hist_df = pd.DataFrame(st.session_state.history)
st.line_chart(hist_df)

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("Real-time AI Dashboard | Predictive Maintenance + Energy Optimization")
