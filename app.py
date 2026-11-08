import streamlit as st
from streamlit_folium import st_folium
import folium
import plotly.graph_objects as go

# 1. Master Page Configuration (Force Dark-Mode Dashboard Frame)
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
    .stApp { animation: fadeIn 0.6s ease-out; background-color: #060913; }

    /* Compact 3D Slate Cards */
    .premium-card {
        background: linear-gradient(135deg, #0B132B 0%, #1C2541 100%);
        border: 1.5px solid #3A506B;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 15px -3px rgba(0,0,0,0.5);
        transform: perspective(1000px) translateZ(0);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 15px;
    }
    .premium-card:hover {
        transform: perspective(1000px) translateZ(12px) translateY(-4px);
        box-shadow: 0 12px 24px -5px rgba(0, 245, 196, 0.2);
        border-color: #00F5C4;
    }
    .card-title { 
        font-size: 11px; font-weight: 700; text-transform: uppercase; 
        letter-spacing: 1px; color: #94A3B8; margin-bottom: 8px; 
    }
    .card-value-flex { display: flex; align-items: center; gap: 8px; }
    .card-value { font-size: 24px; font-weight: 800; line-height: 1.1; }
    
    /* Pulsing Status Badge Core Rings */
    .pulse-ring {
        display: inline-block; width: 10px; height: 10px; border-radius: 50%;
        animation: pulseGlow 1.5s infinite;
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
        70% { box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
    .text-description-box { margin: 0; font-size: 12.5px; color: #CBD5E1; line-height: 1.3; }

    /* Weather Matrix Slider */
    .weather-box-container {
        background: #0B132B; border: 1px solid #1C2541; border-radius: 12px; padding: 12px; text-align: center;
    }

    /* 3D Falling Raindrops Canvas Layer */
    .rain-canvas {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 9999; overflow: hidden;
    }
    .drop {
        position: absolute; bottom: 100%; width: 1.5px; height: 35px;
        background: linear-gradient(transparent, rgba(0, 245, 196, 0.3));
        animation: fall 0.8s linear infinite;
    }
    @keyframes fall {
        0% { transform: translateY(-50px) rotate(12deg); }
        100% { transform: translateY(110vh) rotate(12deg); }
    }
    .d1 { left: 12%; animation-delay: 0s; animation-duration: 0.75s; }
    .d2 { left: 28%; animation-delay: 0.2s; animation-duration: 0.9s; }
    .d3 { left: 45%; animation-delay: 0.1s; animation-duration: 0.7s; }
    .d4 { left: 62%; animation-delay: 0.3s; animation-duration: 0.85s; }
    .d5 { left: 78%; animation-delay: 0.05s; animation-duration: 0.8s; }
    .d6 { left: 92%; animation-delay: 0.15s; animation-duration: 0.95s; }
</style>
""", unsafe_allow_html=True)

# 3. Vector Sidebar Navigation Architecture
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <svg viewBox="0 0 24 24" width="60" height="60" stroke="#00F5C4" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0px 0px 6px rgba(0,245,196,0.4));">
        <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"></path>
        <path d="M12 6v6l4 2"></path>
    </svg>
    <h4 style="color: #64FFDA; margin-top: 10px; font-weight: 700; letter-spacing: 1px; font-size: 14px;">FloodWatch National Node</h4>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("🌍 National Matrix")

# 4. Regional Selection Dropdown Configurations
selected_city = st.sidebar.selectbox("Select Active Operational Node", ["Islamabad Capital Territory", "Nowshera (KPK River Node)", "Sukkur (Sindh Indus Node)", "Rajanpur (South Punjab)"])
region = st.sidebar.selectbox("Target Basin Zone", ["Kabul River Basin", "Indus Delta", "Rajanpur Grid"])
# 5. Flattened Architecture Mapping Logic (Bypasses nested dictionary structure bugs)
if selected_city == "Islamabad Capital Territory":
    map_center = [33.6844, 73.0479]
    risk, risk_color, sar, threat = "MODERATE", "#F59E0B", "STANDBY", "22.4 / 100"
    desc = "Urban drainage channels operating at baseline thresholds."
    has_rain = True
    hydro_flow = [120, 145, 132, 210, 245, 190, 160]
    temp, humidity, wind = "17°C", "64%", "4 mph"
    temps = ["24°C","23°C","23°C","19°C","19°C","21°C","22°C"]
    icons = ["☁️","⛅","☀️","🌧️","🌦️","☀️","☁️"]

elif selected_city == "Nowshera (KPK River Node)":
    map_center = [34.0105, 71.9866]
    risk, risk_color, sar, threat = "CRITICAL SURGE", "#EF4444", "ACTIVE FEED", "88.6 / 100"
    desc = "Kabul River discharge tracking near peak boundaries."
    has_rain = True
    hydro_flow = [450, 510, 480, 680, 712, 640, 590]
    temp, humidity, wind = "19°C", "58%", "6 mph"
    temps = ["26°C","25°C","24°C","20°C","21°C","23°C","24°C"]
    icons = ["☀️","☀️","⛅","🌧️","☁️","☀️","☀️"]

elif selected_city == "Sukkur (Sindh Indus Node)":
    map_center = [27.7244, 68.8228]
    risk, risk_color, sar, threat = "ELEVATED ALERT", "#F59E0B", "ACTIVE FEED", "61.2 / 100"
    desc = "Sukkur Barrage telemetry tracking normal baseline variations."
    has_rain = False
    hydro_flow = [320, 340, 310, 450, 490, 410, 380]
    temp, humidity, wind = "26°C", "42%", "5 mph"
    temps = ["32°C","31°C","31°C","30°C","30°C","29°C","29°C"]
    icons = ["☀️","☀️","☀️","☀️","☀️","☀️","☀️"]

else: # Rajanpur (South Punjab)
    map_center = [29.1044, 70.3250]
    risk, risk_color, sar, threat = "HIGH RISK", "#EF4444", "MONITORING", "79.4 / 100"
    desc = "Hill torrent tracking layers monitoring active catchment vectors."
    has_rain = False
    hydro_flow = [210, 230, 205, 315, 340, 290, 260]
    temp, humidity, wind = "23°C", "48%", "3 mph"
    temps = ["30°C","29°C","29°C","27°C","26°C","27°C","28°C"]
    icons = ["☀️","☀️","☀️","⛅","☁️","☀️","☀️"]

# 6. Dynamic 3D Precipitation Layer Logic
if has_rain:
    st.markdown("""
    <div class="rain-canvas">
        <div class="drop d1"></div><div class="drop d2"></div><div class="drop d3"></div>
        <div class="drop d4"></div><div class="drop d5"></div><div class="drop d6"></div>
    </div>
    """, unsafe_allow_html=True)

# 7. Primary Platform Layout Headers
st.title("🌊 FloodWatch AI Hub")
st.markdown(f"##### *Geospatial Risk Management Hub & Meteorological Tracking* &nbsp;|&nbsp; **Active Sector: {selected_city}**")
st.write("---")

# 8. Compact Metrics with Pulsing Status Rings
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">🚨 Current Risk Assessment</div>
        <div class="card-value-flex">
            <span class="pulse-ring" style="background-color: {risk_color}; box-shadow: 0 0 0 0 {risk_color};"></span>
            <span class="card-value" style="color: {risk_color};">{risk}</span>
        </div>
        <p class="text-description-box" style="margin-top: 6px;">{desc}</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">🛰️ Active SAR Radar Layer</div>
        <div class="card-value-flex">
            <span class="pulse-ring" style="background-color: #64FFDA; box-shadow: 0 0 0 0 rgba(100,255,218,0.7);"></span>
            <span class="card-value" style="color: #64FFDA;">{sar}</span>
        </div>
        <p class="text-description-box" style="margin-top: 6px;">Copernicus Sentinel orbit telemetry aligned perfectly.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">🏢 Infrastructure Threat Score</div>
        <div class="card-value-flex">
            <span class="pulse-ring" style="background-color: #0DF5C4; box-shadow: 0 0 0 0 rgba(13,245,196,0.7);"></span>
            <span class="card-value" style="color: #0DF5C4;">{threat}</span>
        </div>
        <p class="text-description-box" style="margin-top: 6px;">AI loss assessment mapping model actively rendering structural perimeters.</p>
    </div>
    """, unsafe_allow_html=True)

# 9. Weather Metrics Tracker Panel
st.markdown("### 🌤️ Local Meteorology Metrics & 7-Day Outlook")
w_col1, w_col2, w_col3 = st.columns(3)
w_col1.metric(label="🌡️ Current Temperature", value=temp)
w_col2.metric(label="💧 Relative Humidity", value=humidity)
w_col3.metric(label="💨 Wind Speed Metrics", value=wind)

st.write("")
days_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
days_cols = st.columns(7)
for idx, col in enumerate(days_cols):
    with col:
        st.markdown(f"""
        <div class="weather-box-container">
            <div style="font-size: 11px; color: #94A3B8; font-weight: bold;">{days_list[idx]}</div>
            <div style="font-size: 24px; margin: 4px 0;">{icons[idx]}</div>
            <div style="font-size: 14px; font-weight: bold; color: #64FFDA;">{temps[idx]}</div>
        </div>
        """, unsafe_allow_html=True)
st.write("---")

# 10. ADVANCED FEATURES: Plotly Hydro-Chart & Reliable Stadia Dark Map Node
st.markdown("### 📊 Live River Flow Water Discharge Data & Geospatial Telemetry")

chart_col, map_col = st.columns(2)

with chart_col:
    st.markdown("##### 📈 Real-Time Water Flow Spline Volume (Cusecs)")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days_list, y=hydro_flow,
        mode='lines+markers', name='Water Discharge',
        line=dict(color='#00F5C4', width=3, shape='spline'),
        fill='tozeroy', fillcolor='rgba(0, 245, 196, 0.08)',
        marker=dict(size=6, color='#64FFDA')
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=10, b=10), height=400, showlegend=False,
        xaxis=dict(showgrid=True, gridcolor='#1E293B', tickfont=dict(color='#94A3B8')),
        yaxis=dict(showgrid=True, gridcolor='#1E293B', tickfont=dict(color='#94A3B8'))
    )
    st.plotly_chart(fig, use_container_width=True)

with map_col:
    st.markdown(f"##### 🗺️ Operational Geospatial Grid Map")
    m = folium.Map(
    location=map_center, 
    zoom_start=11, 
    tiles="https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png",
    attr='&copy; OpenStreetMap contributors, CyclOSM'
    )


    
    folium.CircleMarker(
        location=map_center, radius=12, popup=f"{selected_city} Active Operational Threat Node",
        color="#00F5C4", fill=True, fill_color="#00FFFF", fill_opacity=0.6
    ).add_to(m)
    
    st_folium(m, width=650, height=400, key=f"stadia_dark_map_node_{selected_city.lower().replace(' ', '_')}_{map_center}")
