import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="해수면 상승 피해 지도", layout="wide")

st.title("🌊 해수면 상승 피해 지역 지도")

# 지도 기본 설정 (한국 중심)
m = folium.Map(location=[36.5, 127.8], zoom_start=6, tiles="OpenStreetMap")

# 피해 지역 데이터
data = [
    {
        "name": "대청도",
        "lat": 37.82,
        "lon": 124.7,
        "desc": "만조 시 도로·항구 침수"
    },
    {
        "name": "연평도",
        "lat": 37.66,
        "lon": 125.7,
        "desc": "해안가 도로 침수 및 주민 대피"
    },
    {
        "name": "부산 해안",
        "lat": 35.1,
        "lon": 129.04,
        "desc": "저지대 주택·도로 침수",
        "image": "busan_flood.png"   # 같은 폴더에 저장 필요
    }
]

# 마커 추가
for d in data:
    if "image" in d:
        html = f"""
        <h4>{d['name']}</h4>
        <p>{d['desc']}</p>
        <img src="{d['image']}" width="200">
        """
    else:
        html = f"""
        <h4>{d['name']}</h4>
        <p>{d['desc']}</p>
        """
    iframe = folium.IFrame(html=html, width=250, height=250)
    popup = folium.Popup(iframe, max_width=250)
    folium.Marker([d["lat"], d["lon"]], popup=popup, tooltip=d["name"]).add_to(m)

# 지도 출력
st_data = st_folium(m, width=800, height=600)
