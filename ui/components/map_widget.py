import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from config import settings

def render():
    st.markdown("### 🗺️ Live Traffic Grid")

    # 1. Create Fake Data (Just to test the screen)
    # Generates 50 random dots around the center coordinates
    data = pd.DataFrame({
        'lat': [settings.MAP_CENTER_LAT + np.random.normal(0, 0.02) for _ in range(50)],
        'lon': [settings.MAP_CENTER_LON + np.random.normal(0, 0.02) for _ in range(50)],
    })

    # 2. Define the visual layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position='[lon, lat]',
        get_color='[200, 30, 0, 160]', # Red color
        get_radius=200,
    )

    # 3. Set the camera view
    view_state = pdk.ViewState(
        latitude=settings.MAP_CENTER_LAT,
        longitude=settings.MAP_CENTER_LON,
        zoom=settings.INITIAL_ZOOM,
        pitch=50,
    )

    # 4. Render
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state
    ))