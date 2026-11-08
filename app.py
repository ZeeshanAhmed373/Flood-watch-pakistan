import streamlit as st
from streamlit_folium import st_folium
import folium

# 1. Master Page Configuration (Forced Dark Theme Baseline)
st.set_page_config(
    page_title="FloodWatch AI - Enterprise Hub",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Advanced CSS: Proportional Metric Cards & Dynamic 3D Matrix Rain Effects
st.markdown("""
<style>
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .stApp { animation: fadeIn 0.6s ease-out; background-color: #0B0F19; }

    /* Downsized Compact 3D Slate Cards */
    .premium-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1.5px solid #334155;
        border-radius: 12px;
        padding: 16px; /* Reduced from 24px */
        box-shadow: 0 4px 15px -3px rgba(0,0,0,0.4);
        transform: perspective(1000px) translateZ(0);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 15px;
    }
    .premium-card:hover {
        transform: perspective(1000px) translateZ(12px) translateY(-4px);
        box-shadow: 0 12px 24px -5px rgba(13, 148, 136, 0.25);
        border-color: #0D9488;
    }
    .card-title { 
        font-size: 11px; /* Downsized */
        font-weight: 700; 
        text-transform: uppercase; 
        letter-spacing: 1px; 
        color: #94A3B8; 
        margin-bottom: 6px; 
    }
    .card-value { 
        font-size: 24px; /* Downsized from 34px */
        font-weight: 800; 
        margin-bottom: 4px; 
        line-height: 1.1; 
    }
    .card-desc { 
        margin: 0; 
        font-size: 12.5px; /* Downsized */
        color: #CBD5E1; 
        line-height: 1.3; 
    }

    /* CSS-Driven 3D Rain Drop Grid Overlay System */
    .rain-canvas {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 9999; overflow: hidden;
    }
    .drop {
        position: absolute; bottom: 100%; width: 1.5px; height: 35px;
        background: linear-gradient(transparent, rgba(100, 255, 218, 0.4));
        animation: fall 0.9s linear infinite;
    }
    @keyframes fall {
        0% { transform: translateY(-50px) rotate(15deg); }
        100% { transform: translateY(110vh) rotate(15deg); }
    }
    /* Generates semi-random spatial distributions for the 3D drops */
    .d1 { left: 10%; animation-delay: 0s; animation-duration: 0.8s; }
    .d2 { left: 25%; animation-delay: 0.2s; animation-duration: 0.95s; }
    .d3 { left: 40%; animation-delay: 0.1s; animation-duration: 0.75s; }
    .d4 { left: 55%; animation-delay: 0.35s; animation-duration: 0.9s; }
    .d5 { left: 70%; animation-delay: 0.05s; animation-duration: 0.85s; }
    .d6 { left: 85%; animation-delay: 0.25s; animation-duration: 1s; }
    .d7 { left: 95%; animation-delay: 0.15s; animation-duration: 0.7s; }
</style>
""", unsafe_allow_html=True)

# 3. Secure Vector Sidebar Navigation Layout Banner
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <svg viewBox="0 0 24 24" width="64" height="64" stroke="#0D9488" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0px 0px 6px rgba(13,148,136,0.5));">
        <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"></path>
        <path d="M12 6v6l4 2"></path>
    </svg>
    <h4 style="color: #64FFDA; margin-top: 10px; font-weight: 700; letter-spacing: 1px; font-size: 15px;">FloodWatch AI Node</h4>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("🌍 National Matrix")
# 4. Comprehensive Internal Pakistan Regional Database Matrix
pakistan_cities_db = {
    "Islamabad Capital Territory": {
        "coords": [33.6844, 73.0479], "risk": "MODERATE", "risk_color": "#F59E0B", "sar": "STANDBY", 
        "threat": "22.4 / 100", "desc": "Urban drainage channels operating at baseline levels.", "has_rain": True,
        "temp": "17°C", "humidity": "64%", "wind": "4 mph", "temps": ["24°C","23°C","23°C","19°C","19°C","21°C","22°C"], "icons": ["☁️","⛅","☀️","🌧️","🌦️","☀️","☁️"]
    },
    "Nowshera (KPK River Node)": {
        "coords": [34.0105, 71.9866], "risk": "CRITICAL SURGE", "risk_color": "#EF4444", "sar": "ACTIVE", 
        "threat": "88.6 / 100", "desc": "Kabul River discharge tracking high. Surge alerts live.", "has_rain": True,
        "temp": "19°C", "humidity": "58%", "wind": "6 mph", "temps": ["26°C","25°C","24°C","20°C","21°C","23°C","24°C"], "icons": ["☀️","☀️","⛅","🌧️","☁️","☀️","☀️"]
    },
    "Sukkur (Sindh Indus Node)": {
        "coords": [27.7244, 68.8228], "risk": "ELEVATED ALERT", "risk_color": "#F59E0B", "sar": "ACTIVE", 
        "threat": "61.2 / 100", "desc": "Sukkur Barrage telemetry tracking normal distribution parameters.", "has_rain": False,
        "temp": "26°C", "humidity": "42%", "wind": "5 mph", "temps": ["32°C","31°C","31°C","30°C","30°C","29°C","29°C"], "icons": ["☀️","☀️","☀️","☀️","☀️","☀️","☀️"]
    },
    "Rajanpur (South Punjab)": {
        "coords": [29.1044, 70.3250], "risk": "HIGH RISK", "risk_color": "#EF4444", "sar": "MONITOR", 
        "threat": "79.4 / 100", "desc": "Hill torrent tracking layers monitoring active catchment vectors.", "has_rain": False,
        "temp": "23°C", "humidity": "48%", "wind": "3 mph", "temps": ["30°C","29°C","29°C","27°C","26°C","27°C","28°C"], "icons": ["☀️","☀️","☀️","⛅","☁️","☀️","☀️"]
    },
    "Karachi Coastline": {
        "coords": [24.8607, 67.0011], "risk": "LOW / NORMAL", "risk_color": "#10B981", "sar": "STANDBY", 
        "threat": "14.5 / 100", "desc": "Tidal heights tracking at standard seasonal parameters.", "has_rain": False,
        "temp": "28°C", "humidity": "72%", "wind": "11 mph", "temps": ["33°C","33°C","32°C","32°C","31°C","31°C","32°C"], "icons": ["☀️","☀️","☀️","⛅","⛅","☀️","☀️"]
    },
    "Lahore Hub (Ravi Node)": {
        "coords": [31.5204, 74.3587], "risk": "LOW / MINIMAL", "risk_color": "#10B981", "sar": "MONITOR", 
        "threat": "31.8 / 100", "desc": "River bed telemetry operating within safe thresholds.", "has_rain": False,
        "temp": "21°C", "humidity": "55%", "wind": "5 mph", "temps": ["28°C","27°C","27°C","26°C","25°C","25°C","26°C"], "icons": ["☁️","☁️","⛅","☀️","☀️","☀️","⛅"]
    }
}

selected_city = st.sidebar.selectbox("Select Active Operational Node", list(pakistan_cities_db.keys()))
region = st.sidebar.selectbox("Target Basin/District Zone", ["Kabul River Basin", "Indus Delta", "Rajanpur Zone"])
active_node_data = pakistan_cities_db[selected_city]

# 5. Dynamic 3D Rain Overlay Controller Injection
if active_node_data["has_rain"]:
    st.markdown("""
    <div class="rain-canvas">
        <div class="drop d1"></div><div class="drop d2"></div><div class="drop d3"></div>
        <div class="drop d4"></div><div class="drop d5"></div><div class="drop d6"></div>
        <div class="drop d7"></div>
    </div>
    """, unsafe_allow_html=True)

# 6. Primary Platform Header
st.title("🌊 FloodWatch AI Platform")
st.markdown(f"##### *Geospatial Risk Management Hub & Meteorological Tracking* &nbsp;|&nbsp; **Active Sector: {selected_city}**")
st.write("---")

# 7. Optimized Compact Metrics Panel
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">🚨 Current Risk Assessment</div>
        <div class="card-value" style="color: {active_node_data['risk_color']};">{active_node_data['risk']}</div>
        <p class="card-desc">{active_node_data['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">🛰️ Active SAR Radar Layer</div>
        <div class="card-value" style="color: #64FFDA;">{active_node_data['sar']}</div>
        <p class="card-desc">Copernicus Sentinel orbital feed alignment configuration synchronized.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">🏢 Infrastructure Threat Score</div>
        <div class="card-value" style="color: #0DF5C4;">{active_node_data['threat']}</div>
        <p class="card-desc">AI loss assessment mapping model actively rendering perimeters.</p>
    </div>
    """, unsafe_allow_html=True)

# 8. Weather Module Matrix
st.markdown("### 🌤 nighttime Local Meteorology Metrics & 7-Day Outlook")

w_col1, w_col2, w_col3 = st.columns(3)
w_col1.metric(label="🌡️ Current Temperature", value=active_node_data["temp"])
w_col2.metric(label="💧 Relative Humidity", value=active_node_data["humidity"])
w_col3.metric(label="💨 Wind Speed Metrics", value=active_node_data["wind"])

st.write("")
days_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
days_cols = st.columns(7)
for idx, col in enumerate(days_cols):
    with col:
        st.markdown(f"""
        <div style="background: #1E293B; border: 1px solid #475569; border-radius: 12px; padding: 12px; text-align: center;">
            <div style="font-size: 12px; color: #94A3B8; font-weight: bold;">{days_list[idx]}</div>
            <div style="font-size: 26px; margin: 5px 0;">{active_node_data['icons'][idx]}</div>
            <div style="font-size: 15px; font-weight: bold; color: #64FFDA;">{active_node_data['temps'][idx]}</div>
        </div>
        """, unsafe_allow_html=True)
st.write("---")

# 9. Dynamic Geospatial Map Framework
st.markdown(f"### 🗺️ Operational Geospatial Framework Map: {selected_city} Sector")

map_center = active_node_data["coords"]
m = folium.Map(location=map_center, zoom_start=11, tiles="OpenStreetMap")

folium.CircleMarker(
    location=map_center, radius=14, popup=f"Active Threat Alert Region - {selected_city} Hub Node",
    color="#0D9488", fill=True, fill_color="#00FFFF", fill_opacity=0.7
).add_to(m)

st_folium(m, width=1300, height=520, key=f"map_viewport_sync_{selected_city.lower().replace(' ', '_')}")
