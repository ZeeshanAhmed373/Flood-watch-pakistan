"""Entry point. Run locally: streamlit run app.py"""
import streamlit as st

from components.damage_assessment import render_damage_assessment
from components.map_view import render_map_dashboard
from components.weather_dashboard import render_weather_dashboard

st.set_page_config(page_title="FloodWatch Pakistan", page_icon="🌊", layout="wide")
st.title("🌊 FloodWatch Pakistan")
st.caption("Rainfall monitoring, flood alerts, satellite mapping and AI damage assessment")

view = st.sidebar.radio("View", ["Weather & alerts", "Satellite map", "AI damage assessment"])
st.sidebar.divider()

if view == "Weather & alerts":
    render_weather_dashboard()
elif view == "Satellite map":
    render_map_dashboard()
else:
    render_damage_assessment()
