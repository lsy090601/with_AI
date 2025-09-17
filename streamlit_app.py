import streamlit as st
import pydeck as pdk
import pandas as pd

st.set_page_config(layout="wide")
st.title("🌊 Sunny-day Flooding Map – Callout Demo")

# 샘플 데이터 (위도, 경도, 장소, 설명)
data = pd.DataFrame({
    "lat": [37.828, 37.666],
    "lon": [124.700, 126.933],
    "place": ["대청도", "부산 해안"],
    "desc": ["만조 시 도로·항구 침수", "저지대 주택 및 도로 침수"]
})

# 지도 중심
view_state = pdk.ViewState(
    latitude=36.5,
    longitude=127.8,
    zoom=6,
    pitch=0
)

# 마커 레이어
point_layer = pdk.Layer(
    "ScatterplotLayer",
    data,
    get_position='[lon, lat]',
    get_fill_color='[0, 100, 200, 160]',
    get_radius=60000,
    pickable=True
)

# 화살표(라인) 레이어
arrow_data = pd.DataFrame({
    "from_lat": [37.828, 37.666],
    "from_lon": [124.700, 126.933],
    "to_lat": [38.2, 37.8],
    "to_lon": [125.2, 127.3],
    "label": ["대청도 침수", "부산 침수"]
})

line_layer = pdk.Layer(
    "LineLayer",
    arrow_data,
    get_source_position='[from_lon, from_lat]',
    get_target_position='[to_lon, to_lat]',
    get_color='[255, 0, 0, 160]',
    get_width=3,
    pickable=True
)

# Deck 초기화
r = pdk.Deck(
    layers=[point_layer, line_layer],
    initial_view_state=view_state,
    tooltip={"text": "{place}: {desc}"}
)

st.pydeck_chart(r)

st.subheader("📌 피해 설명")
for _, row in data.iterrows():
    st.markdown(f"**{row['place']}** – {row['desc']}")