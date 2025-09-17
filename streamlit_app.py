import streamlit as st
import pydeck as pdk

# ========================
# VWorld API 설정
# ========================
API_KEY = "여기에_API_KEY_입력"
VWORLD_SATELLITE = f"http://api.vworld.kr/req/wmts/1.0.0/{API_KEY}/Satellite/{{z}}/{{y}}/{{x}}.jpeg"
VWORLD_LABEL = f"http://api.vworld.kr/req/wmts/1.0.0/{API_KEY}/Hybrid/{{z}}/{{y}}.png"

# ========================
# 데이터 정의
# ========================
data = [
    {
        "name": "대청도",
        "lat": 37.828,
        "lon": 124.704,
        "desc": "만조 시 도로·항구 침수",
        "url": "https://www.kyeonggi.com/article/20230803580166"
    },
    {
        "name": "연평도",
        "lat": 37.666,
        "lon": 125.700,
        "desc": "여러 섬 도서지역에 만조 및 침수 피해 보고됨",
        "url": "https://www.kyeongin.com/article/1747652"
    },
    {
        "name": "부산 해안",
        "lat": 35.1796,
        "lon": 129.0756,
        "desc": "저지대 주택·도로 침수",
        "url": "https://www.hankyung.com/article/2023030990747"
    }
]

# ========================
# ScatterplotLayer
# ========================
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    get_position='[lon, lat]',
    get_color='[255, 0, 0, 200]',
    get_radius=10000,
    pickable=True,
)

# ========================
# VWorld 지도 (위성 + 한글 라벨)
# ========================
satellite_layer = pdk.Layer(
    "TileLayer",
    tile_url_template=VWORLD_SATELLITE,
    tile_size=256,
    min_zoom=0,
    max_zoom=19,
)

label_layer = pdk.Layer(
    "TileLayer",
    tile_url_template=VWORLD_LABEL,
    tile_size=256,
    min_zoom=0,
    max_zoom=19,
)

# ========================
# 초기 뷰
# ========================
view_state = pdk.ViewState(
    latitude=36.0,
    longitude=128.0,
    zoom=6
)

# ========================
# Deck (툴팁은 설명만)
# ========================
r = pdk.Deck(
    layers=[satellite_layer, label_layer, scatter_layer],
    initial_view_state=view_state,
    tooltip={
        "html": "<div style='padding:5px;'><b>{name}</b><br/>{desc}</div>",
        "style": {"backgroundColor": "white", "color": "black"}
    }
)

# ========================
# Streamlit 실행
# ========================
st.title("🌊 해수면 상승 피해 지역 지도")
st.pydeck_chart(r)

st.markdown("## 📌 피해 지역 카드")

# 카드형 박스 (expander 활용)
for d in data:
    with st.expander(f"✅ {d['name']} — {d['desc']}"):
        st.markdown(f"[👉 관련 기사 보러가기]({d['url']})")
