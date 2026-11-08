import streamlit as st
from streamlit_folium import st_folium
import folium

# 1. Page Configuration
st.set_page_config(
    page_title="FloodWatch AI - Enterprise Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Modern 3D Glassmorphism & Weather Layout CSS Injection
st.markdown("""
<style>
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .stApp { animation: fadeIn 0.8s ease-out; }

    /* Premium 3D Slate Cards */
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

    /* Weather Timeline Styling */
    .weather-container {
        display: flex; gap: 12px; overflow-x: auto; padding: 10px 0;
    }
    .weather-day-card {
        background: #1E293B; border: 1px solid #475569; border-radius: 12px;
        min-width: 130px; padding: 16px; text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);
    }
    .weather-date { font-size: 12px; color: #94A3B8; font-weight: 600; }
    .weather-icon { font-size: 28px; margin: 8px 0; }
    .weather-temp { font-size: 18px; font-weight: 700; color: #64FFDA; }
    .weather-cond { font-size: 11px; color: #CBD5E1; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Configuration & Fixed Logo Asset
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

# 4. Master Headers
st.title("🌊 FloodWatch AI Platform")
st.markdown(f"##### *Geospatial Risk Management Hub & Meteorological Tracking* &nbsp;|&nbsp; **Active Node: {selected_city}**")
st.write("---")

# 5. Core Operational Risk Metric Blocks
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="premium-card">
        <div class="card-title">🚨 Current Risk Assessment</div>
        <div class="card-value">HIGH SURGE</div>
        <p class="card-desc">Hydrological monitoring registers threshold variances. Early telemetry warnings active.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="premium-card">
        <div class="card-title">🛰️ Active SAR Radar Layer</div>
        <div class="card-value">SENTINEL-1</div>
        <p class="card-desc">Cloud-penetrating radar processing operational. Fetching baseline spatial metrics.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="premium-card">
        <div class="card-title">🏢 Infrastructure Threat Score</div>
        <div class="card-value">84.2 / 100</div>
        <p class="card-desc">AI damage forecasting mapping node active across vulnerable settlement zones.</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 6. NEW FEATURE: Meteorological Forecast Center
# ==========================================
st.markdown("### 🌤️ Live Local Meteorology & 7-Day Resiliency Outlook")

# Local Mock Database Engine mapped to actual geographical weather patterns
weather_db = {
    "Islamabad": {"temp": "17°C", "humidity": "64%", "wind": "4 mph", "forecast": [
        {"day": "Mon Nov 9", "icon": "☁️", "temp": "24°C / 16°C", "cond": "Cloudy"},
        {"day": "Tue Nov 10", "icon": "⛅", "temp": "23°C / 15°C", "cond": "Partly Cloudy"},
        {"day": "Wed Nov 11", "icon": "☀️", "temp": "23°C / 16°C", "cond": "Mostly Sunny"},
        {"day": "Thu Nov 12", "icon": "🌧️", "temp": "19°C / 13°C", "cond": "Heavy Rain/Showers"},
        {"day": "Fri Nov 13", "icon": "🌦️", "temp": "19°C / 12°C", "cond": "Passing Showers"},
        {"day": "Sat Nov 14", "icon": "☀️", "temp": "21°C / 12°C", "cond": "Clear & Sunny"},
        {"day": "Sun Nov 15", "icon": "☁️", "temp": "22°C / 12°C", "cond": "Decreasing Clouds"}
    ]},
    "Nowshera": {"temp": "19°C", "humidity": "58%", "wind": "6 mph", "forecast": [
        {"day": "Mon Nov 9", "icon": "☀️", "temp": "26°C / 15°C", "cond": "Sunny"},
        {"day": "Tue Nov 10", "icon": "☀️", "temp": "25°C / 14°C", "cond": "Sunny"},
        {"day": "Wed Nov 11", "icon": "⛅", "temp": "24°C / 13°C", "cond": "Partly Cloudy"},
        {"day": "Thu Nov 12", "icon": "🌧️", "temp": "20°C / 12°C", "cond": "Moderate Rain"},
        {"day": "Fri Nov 13", "icon": "☁️", "temp": "21°C / 11°C", "cond": "Overcast"},
        {"day": "Sat Nov 14", "icon": "☀️", "temp": "23°C / 11°C", "cond": "Clear"},
        {"day": "Sun Nov 15", "icon": "☀️", "temp": "24°C / 12°C", "cond": "Clear"}
    ]},
    "Sukkur": {"temp": "26°C", "humidity": "42%", "wind": "5 mph", "forecast": [
        {"day": "Mon Nov 9", "icon": "☀️", "temp": "32°C / 20°C", "cond": "Clear & Hot"},
        {"day": "Tue Nov 10", "icon": "☀️", "temp": "31°C / 19°C", "cond": "Clear"},
        {"day": "Wed Nov 11", "icon": "☀️", "temp": "31°C / 19°C", "cond": "Clear"},
        {"day": "Thu Nov 12", "icon": "☀️", "temp": "30°C / 18°C", "cond": "Clear"},
        {"day": "Fri Nov 13", "icon": "☀️", "temp": "30°C / 17°C", "cond": "Sunny"},
        {"day": "Sat Nov 14", "icon": "☀️", "temp": "29°C / 17°C", "cond": "Sunny"},
        {"day": "Sun Nov 15", "icon": "☀️", "temp": "29°C / 18°C", "cond": "Sunny"}
    ]},
    "Rajanpur": {"temp": "23°C", "humidity": "48%", "wind": "3 mph", "forecast": [
        {"day": "Mon Nov 9", "icon": "☀️", "temp": "30°C / 17°C", "cond": "Sunny"},
        {"day": "Tue Nov 10", "icon": "☀️", "temp": "29°C / 16°C", "cond": "Sunny"},
        {"day": "Wed Nov 11", "icon": "☀️", "temp": "29°C / 16°C", "cond": "Sunny"},
        {"day": "Thu Nov 12", "icon": "⛅", "temp": "27°C / 15°C", "cond": "Partly Cloudy"},
        {"day": "Fri Nov 13", "icon": "☁️", "temp": "26°C / 14°C", "cond": "Overcast"},
        {"day": "Sat Nov 14", "icon": "☀️", "temp": "27°C / 14°C", "cond": "Clear"},
        {"day": "Sun Nov 15", "icon": "☀️", "temp": "28°C / 15°C", "cond": "Clear"}
    ]}
}

city_data = weather_db.get(selected_city, weather_db["Islamabad"])

# Render Current Weather Card metrics block
w_col1, w_col2, w_col3 = st.columns(3)
with w_col1:
    st.metric(label="🌡️ Current Temperature", value=city_data["temp"])
with w_col2:
    st.metric(label="💧 Relative Humidity", value=city_data["humidity"])
with w_col3:
    st.metric(label="💨 Wind Speed Metrics", value=city_data["wind"])

# Build the custom HTML 7-day chronological slider layout timeline
timeline_html = '<div class="weather-container">'
for day_f in city_data["forecast"]:
    timeline_html += f"""
    <div class="weather-day-card">
        <div class="weather-date">{day_f["day"]}</div>
        <div class="weather-icon">{day_f["icon"]}</div>
        <div class="weather-temp">{day_f["temp"]}</div>
        <div class="weather-cond">{day_f["cond"]}</div>
    </div>
    """
timeline_html += '</div>'
st.markdown(timeline_html, unsafe_allow_html=True)
st.write("---")

# 7. Open-Source Map Canvas
st.markdown("### 🗺️ Operational Geospatial Framework Map")
m = folium.Map(location=[34.0105, 71.9866], zoom_start=11, tiles="OpenStreetMap")
folium.CircleMarker(
    location=[34.0105, 71.9866], radius=14, popup=f"{selected_city} Node Visual Baseline Area",
    color="#0D9488", fill=True, fill_color="#00FFFF", fill_opacity=0.7
).add_to(m)
st_folium(m, width=1300, height=500)
