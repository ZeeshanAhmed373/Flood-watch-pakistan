import streamlit as st
from streamlit_folium import st_folium
import folium

# 1. Premium Layout Page Setup
st.set_page_config(
    page_title="FloodWatch AI - Premium Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Modern 3D Dark Glassmorphism High-Contrast CSS
st.markdown("""
<style>
    /* Global Page Smooth Entrance Animation */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .stApp {
        animation: fadeIn 0.8s ease-out;
    }

    /* 3D Dark Cards for Maximum Text Visibility & Appeal */
    .premium-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 2px solid #334155;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        transform: perspective(1000px) translateZ(0);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 20px;
    }

    /* Vibrant 3D Glow on Hover */
    .premium-card:hover {
        transform: perspective(1000px) translateZ(20px) translateY(-6px);
        box-shadow: 0 20px 35px -5px rgba(13, 148, 136, 0.3);
        border-color: #0D9488;
    }

    /* Bold, High-Contrast Typography */
    .card-title {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #94A3B8; /* Muted Slate Gray Header */
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .card-value {
        font-size: 34px;
        font-weight: 800;
        color: #0DF5C4; /* Highly Visible Neon Mint Emerald */
        margin-bottom: 8px;
        line-height: 1.1;
    }

    .card-desc {
        margin: 0;
        font-size: 14px;
        color: #E2E8F0; /* Clean Off-White for perfect readability */
        font-weight: 400;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Configuration with a Fixed, High-Quality Banner Image
st.sidebar.image("https://unsplash.com", use_column_width=True)
st.sidebar.header("🌍 Navigation Matrix")
region = st.sidebar.selectbox("Target Basin/District", ["Kabul River Basin", "Indus Delta", "Rajanpur Zone"])

# 4. Clean Master Titles
st.title("🌊 FloodWatch AI")
st.markdown("##### *Predictive Geospatial Intelligence Platform for Disaster Mitigation*")
st.write("---")

# 5. High-Contrast Premium Metrics Grid Layout
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="premium-card">
        <div class="card-title">🚨 Current Risk Assessment</div>
        <div class="card-value">HIGH SURGE</div>
        <p class="card-desc">Kabul River Basin surge expected within 48h. Regional alerts broadcasted.</p>
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

# 6. Core Map Integration (Bypassing broken API keys with 100% Free OpenStreetMap)
st.markdown("### 🗺️ Live Resiliency Mapping Model")

# Using 'OpenStreetMap' tiles which are open-source and NEVER block traffic with API walls
m = folium.Map(location=[34.0105, 71.9866], zoom_start=11, tiles="OpenStreetMap")

# Add a prominent glowing custom indicator marker over the test region
folium.CircleMarker(
    location=[34.0105, 71.9866],
    radius=14,
    popup="Nowshera Structural Threat Alert Area",
    color="#0D9488",
    fill=True,
    fill_color="#00FFFF",
    fill_opacity=0.7
).add_to(m)

# Expose Map Component natively to layout window
st_folium(m, width=1300, height=550)
