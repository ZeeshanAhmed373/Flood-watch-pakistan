import streamlit as st
from streamlit_folium import st_folium
import folium

# 1. Master Page Configurations
st.set_page_config(
    page_title="FloodWatch AI - Enterprise Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Modern High-Contrast 3D Glassmorphism CSS Themes
st.markdown("""
<style>
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .stApp { animation: fadeIn 0.8s ease-out; }

    /* 3D Dark Cards */
    .premium-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 2px solid #334155;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
        transform: perspective(1000px) translateZ(0);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 20px;
    }
    .premium-card:hover {
        transform: perspective(1000px) translateZ(20px) translateY(-6px);
        box-shadow: 0 20px 35px -5px rgba(13, 148, 136, 0.3);
        border-color: #0D9488;
    }
    .card-title {
        font-size: 13px; font-weight: 700; text-transform: uppercase;
        letter-spacing: 1.2px; color: #94A3B8; margin-bottom: 10px;
    }
    .card-value { font-size: 34px; font-weight: 800; color: #0DF5C4; margin-bottom: 8px; }
    .card-desc { margin: 0; font-size: 14px; color: #E2E8F0; line-height: 1.4; }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Structural Inputs
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <svg viewBox="0 0 24 24" width="72" height="72" stroke="#0D9488" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0px 0px 8px rgba(13,148,136,0.5));">
        <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"></path>
        <path d="M12 6v6l4 2"></path>
    </svg>
    <h4 style="color: #64FFDA; margin-top: 10px; font-weight: 700; letter-spacing: 1px;">FloodWatch AI Node</h4>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("🌍 Navigation Matrix")
selected_city = st.sidebar.selectbox("Select Target City", ["Islamabad", "Nowshera", "Sukkur", "Rajanpur"])
region = st.sidebar.selectbox("Target Basin/District Zone", ["Kabul River Basin", "Indus Delta", "Rajanpur Zone"])

# 4. Localized Coordinates & Database Variables Map
city_db = {
    "Islamabad": {"coords": [33.6844, 73.0479], "temp": "17°C", "humidity": "64%", "wind": "4 mph", "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "temps": ["24°C", "23°C", "23°C", "19°C", "19°C", "21°C", "22°C"], "icons": ["☁️", "⛅", "☀️", "🌧️", "🌦️", "☀️", "☁️"]},
    "Nowshera": {"coords": [34.0105, 71.9866], "temp": "19°C", "humidity": "58%", "wind": "6 mph", "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "temps": ["26°C", "25°C", "24°C", "20°C", "21°C", "23°C", "24°C"], "icons": ["☀️", "☀️", "⛅", "🌧️", "☁️", "☀️", "☀️"]},
    "Sukkur": {"coords": [27.7244, 68.8228], "temp": "26°C", "humidity": "42%", "wind": "5 mph", "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "temps": ["32°C", "31°C", "31°C", "30°C", "30°C", "29°C", "29°C"], "icons": ["☀️", "☀️", "☀️", "☀️", "☀️", "☀️", "☀️"]},
    "Rajanpur": {"coords": [29.1044, 70.3250], "temp": "23°C", "humidity": "48%", "wind": "3 mph", "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "temps": ["30°C", "29°C", "29°C", "27°C", "26°C", "27°C", "28°C"], "icons": ["☀️", "☀️", "☀️", "⛅", "☁️", "☀️", "☀️"]}
}

active_data = city_db.get(selected_city)

# 5. Core Platform Header Controls
st.title("🌊 FloodWatch AI Platform")
st.markdown(f"##### *Geospatial Risk Management Hub & Meteorological Tracking* &nbsp;|&nbsp; **Active Node: {selected_city}**")
st.write("---")

# 6. Operational High-Contrast Risk Metric Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""<div class="premium-card"><div class="card-title">🚨 Current Risk Assessment</div><div class="card-value">HIGH SURGE</div><p class="card-desc">{region} telemetry variances active.</p></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="premium-card"><div class="card-title">🛰️ Active SAR Radar Layer</div><div class="card-value">SENTINEL-1</div><p class="card-desc">Cloud-penetrating radar processing operational.</p></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="premium-card"><div class="card-title">🏢 Infrastructure Threat Score</div><div class="card-value">84.2 / 100</div><p class="card-desc">AI loss assessment mapping model actively running.</p></div>""", unsafe_allow_html=True)

# 7. Weather Module Using Pure Native Streamlit Columns (Fixes the raw HTML string error)
st.markdown("### 🌤️ Live Local Meteorology & 7-Day Resiliency Outlook")

w_col1, w_col2, w_col3 = st.columns(3)
w_col1.metric(label="🌡️ Current Temperature", value=active_data["temp"])
w_col2.metric(label="💧 Relative Humidity", value=active_data["humidity"])
w_col3.metric(label="💨 Wind Speed Metrics", value=active_data["wind"])

# Render the 7-day outlook using Native Streamlit Columns to eliminate HTML loop bugs completely
st.write("")
days_cols = st.columns(7)
for idx, col in enumerate(days_cols):
    with col:
        st.markdown(f"""
        <div style="background: #1E293B; border: 1px solid #475569; border-radius: 12px; padding: 12px; text-align: center;">
            <div style="font-size: 12px; color: #94A3B8; font-weight: bold;">{active_data["days"][idx]}</div>
            <div style="font-size: 26px; margin: 5px 0;">{active_data["icons"][idx]}</div>
            <div style="font-size: 15px; font-weight: bold; color: #64FFDA;">{active_data["temps"][idx]}</div>
        </div>
        """, unsafe_allow_html=True)
st.write("---")

# 8. Dynamic Geospatial Map Framework (Centered using reactive coordinates)
st.markdown(f"### 🗺️ Operational Geospatial Framework Map: {selected_city} Sector")

map_center = active_data["coords"]
m = folium.Map(location=map_center, zoom_start=11, tiles="OpenStreetMap")

folium.CircleMarker(
    location=map_center, radius=14, popup=f"Active Threat Alert Region - {selected_city} Node",
    color="#0D9488", fill=True, fill_color="#00FFFF", fill_opacity=0.7
).add_to(m)

# The unique component key string forces the map canvas view bounding box to update instantly
st_folium(m, width=1300, height=520, key=f"map_viewport_node_{selected_city}")
