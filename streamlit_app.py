# -*- coding: utf-8 -*-
"""
================================================
한국 연안 해수면 상승 통합 대시보드
- 해수면 상승 추이 시각화
- 피해 지역 지도 표시 (+ 뉴스 기사 토글)
- 청소년 정신건강 영향 데이터
================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pydeck as pdk

# ========================
# 페이지 설정
# ========================
st.set_page_config(
    page_title="🌊 해수면 상승과 청소년 정신건강 대시보드",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================
# CSS 스타일 적용
# ========================
st.markdown("""
<style>
    .main {padding-top: 0rem;}
    .block-container {padding: 2rem 1rem 3rem 1rem;}
    h1 {color: #1e3a8a; font-size: 2.5rem !important;}
    h2 {color: #1e40af; margin-top: 2rem;}
    .stMetric {
        background-color: #f0f9ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# ========================
# 타이틀 및 소개
# ========================
st.title("🌊 밀려오는 파도, 밀려오는 불안")
st.markdown("### 해수면 상승이 청소년 정신건강과 일상생활에 미치는 영향")
st.caption("데이터 출처: 기획재정부, 해양수산부, 국립해양조사원")

# ========================
# 탭 생성
# ========================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 해수면 상승 추이",
    "🗺️ 피해 지역 지도",
    "😰 청소년 정신건강 영향",
    "📈 미래 시나리오"
])

# ========================
# TAB 1: 해수면 상승 추이
# ========================
with tab1:
    st.header("📊 한국 연안 해수면 상승 추이 (1989-2024)")

    @st.cache_data
    def load_sea_level_data():
        years = list(range(1989, 2025))
        sea_levels = [
            0, 2, 4, 7, 9, 12, 14, 16, 19, 22,
            24, 27, 30, 32, 35, 38, 41, 44, 47, 50,
            53, 57, 60, 63, 67, 70, 74, 77, 81, 85,
            89, 93, 97, 101, 105, 110
        ]
        df = pd.DataFrame({
            'year': years,
            'sea_level_mm': sea_levels,
            'sea_level_cm': [s/10 for s in sea_levels]
        })
        df['annual_rise'] = df['sea_level_mm'].diff()
        df['5yr_avg'] = df['annual_rise'].rolling(window=5, center=True).mean()
        return df

    df = load_sea_level_data()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("총 상승량 (35년)", f"{df['sea_level_cm'].iloc[-1]:.1f} cm",
                  f"+{df['sea_level_mm'].iloc[-1]} mm")
    with col2:
        avg_rise = df['sea_level_mm'].iloc[-1] / 35
        st.metric("연평균 상승률", f"{avg_rise:.2f} mm/년", "가속화 중")
    with col3:
        recent_5yr = df['annual_rise'].tail(5).mean()
        st.metric("최근 5년 평균", f"{recent_5yr:.2f} mm/년",
                  f"+{(recent_5yr/avg_rise-1)*100:.1f}%")
    with col4:
        st.metric("2050년 예상", "~20 cm", "IPCC 예측")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['year'], y=df['sea_level_cm'],
        mode='lines+markers', name='해수면 상승',
        line=dict(color='#0066CC', width=3),
        marker=dict(size=6, color='#1E90FF')
    ))
    fig.add_trace(go.Scatter(
        x=df['year'], y=df['5yr_avg']/10,
        mode='lines', name='5년 이동평균 상승률',
        line=dict(color='#FF6B6B', width=2, dash='dash'),
        yaxis='y2'
    ))
    fig.update_layout(
        title='한국 연안 해수면 변화 추이',
        xaxis_title='연도', yaxis_title='해수면 상승 (cm)',
        yaxis2=dict(title='연간 상승률 (cm/년)', overlaying='y', side='right'),
        height=500, hovermode='x unified', plot_bgcolor='white'
    )
    st.plotly_chart(fig, use_container_width=True)

# ========================
# TAB 2: 피해 지역 지도
# ========================
with tab2:
    st.header("🗺️ 해수면 상승 피해 지역 현황")

    # 피해 지역 데이터 (기사 URL 포함)
    damage_data = pd.DataFrame([
        {"name":"대청도","lat":37.828,"lon":124.704,"severity":3,
         "desc":"만조 시 도로·항구 침수 발생","impact":"어업 활동 제한, 주민 대피",
         "url":"https://www.kyeonggi.com/article/20230803580166",
         "color":[255,100,100,200]},
        {"name":"연평도","lat":37.666,"lon":125.700,"severity":3,
         "desc":"도서지역 만조 침수 피해","impact":"선박 운항 중단, 물자 보급 차질",
         "url":"https://www.kyeongin.com/article/1747652",
         "color":[255,100,100,200]},
        {"name":"부산 해안","lat":35.1796,"lon":129.0756,"severity":2,
         "desc":"저지대 주택·도로 침수","impact":"해운대, 광안리 일대 침수",
         "url":"https://www.hankyung.com/article/2023030990747",
         "color":[255,150,100,200]}
    ])

    # 지도 기본 뷰
    view_state = pdk.ViewState(latitude=36.0, longitude=128.0, zoom=6)

    scatter_layer = pdk.Layer(
        "ScatterplotLayer", data=damage_data,
        get_position='[lon, lat]', get_color='color',
        get_radius='severity * 15000', pickable=True
    )
    text_layer = pdk.Layer(
        "TextLayer", data=damage_data,
        get_position='[lon, lat]', get_text='name', get_size=14,
        get_color=[0,0,0,255], get_alignment_baseline="'bottom'"
    )

    # ⭐ 지도 잘 보이게 map_style=None
    r = pdk.Deck(
        layers=[scatter_layer, text_layer],
        initial_view_state=view_state,
        map_style=None,
        tooltip={"html": "<b>{name}</b><br/>{desc}<br/>{impact}"}
    )
    st.pydeck_chart(r)

    # 피해 지역 상세 정보 + 기사 링크 (토글)
    st.markdown("### 📋 피해 지역 상세 정보")
    for idx, row in damage_data.iterrows():
        severity_emoji = ["", "🟡", "🟠", "🔴"][row['severity']]
        with st.expander(f"{severity_emoji} {row['name']} - {row['desc']}"):
            st.markdown(f"**위치:** {row['lat']:.3f}°N, {row['lon']:.3f}°E")
            st.markdown(f"**피해 정도:** {'★' * row['severity']}")
            st.markdown(f"**주요 영향:** {row['impact']}")
            if row['url']:
                st.markdown(f"[📰 관련 기사 보기]({row['url']})")

# ========================
# TAB 3, TAB 4, 사이드바 (이전 코드 유지)
# ========================
# 👉 그대로 두면 됨
