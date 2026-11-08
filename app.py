import streamlit as st
from streamlit_folium import st_folium
import folium

# 1. Force Premium Layout Configuration
st.set_page_config(
    page_title="FloodWatch AI - Premium Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Advanced 3D Effects, Glassmorphism, and Animation CSS Injection
st.markdown("""
<style>
    /* Smooth Entrance Animation for the entire page */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .reportview-container .main .block-container {
        animation: fadeIn 0.8s ease-out;
    }

    /* 3D Glassmorphism Premium KPI Cards */
    .premium-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 25px;
        color: white;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transform: perspective(1000px) translateZ(0);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 20px;
    }

    /* Interactive 3D Depth Hover Shift Effect */
    .premium-card:hover {
        transform: perspective(1000px) translateZ(15px) translateY(-5px);
        box-shadow: 0 15px 45px 0 rgba(13, 148, 136, 0.4);
        border-color: #0D9488;
    }

    .card-title {
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #8892B0;
        margin-bottom: 8px;
    }

    .card-value {
        font-size: 32px;
        font-weight: 800;
        color: #64FFDA;
    }
</style>
""", unsafe_allow_index=True)

# 3. Dynamic Side Navigation Header
st.sidebar.image("https://unsplash.com", use_column_width=True)
st.sidebar.header("🌍 Navigation Matrix")
region = st.sidebar.selectbox("Target Basin/District", ["Kabul River Basin", "Indus Delta", "Rajanpur Zone"])

# 4. Premium Interface Header Display
st.title("🌊 FloodWatch AI")
st.markdown("##### *Predictive Geospatial Intelligence Platform for Disaster Mitigation*")

# 5. Rendering the Interactive 3D Interface Elements
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="premium-card">
        <div class="card-title">🚨 Current Risk Assessment</div>
        <div class="card-value">HIGH SURGE</div>
        <p style="margin: 8px 0 0 0; font-size: 13px; color: #E2E8F0;">Kabul River Basin surge expected within 48h.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="premium-card">
        <div class="card-title">🛰️ Active SAR Radar Layer</div>
        <div class="card-value">SENTINEL-1</div>
        <p style="margin: 8px 0 0 0; font-size: 13px; color: #E2E8F0;">Cloud-penetrating radar processing operational.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="premium-card">
        <div class="card-title">🏢 Infrastructure Threat Score</div>
        <div class="card-value">84.2 / 100</div>
        <p style="margin: 8px 0 0 0; font-size: 13px; color: #E2E8F0;">AI damage forecasting mapping node active.</p>
    </div>
    """, unsafe_allow_html=True)

# 6. Core Mapping Integration Layout
st.markdown("### 🗺️ Live Resiliency Mapping Model")

# Baseline Coordinate Mapping configuration
m = folium.Map(location=[34.0105, 71.9866], zoom_start=11, tiles="CartoDB dark_matter")
folium.CircleMarker(
    location=[34.0105, 71.9866],
    radius=15,
    popup="Nowshera Threat Area",
    color="#0D9488",
    fill=True,
    fill_color="#00FFFF"
).add_to(m)

# Expose Map Component natively to layout window
st_folium(m, width=1300, height=500)
