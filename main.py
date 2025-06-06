# -*- coding: utf-8 -*-
import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 제목
st.set_page_config(page_title="전기차 충전소 지도", layout="wide")

menu = st.sidebar.radio("메뉴 선택", ["홈", "충전소 지도", "앱 정보"])

if menu == "홈":
    st.title("🚗 전기차 충전소 위치 확인 웹앱에 오신 것을 환영합니다!")
    st.write("왼쪽 메뉴에서 원하는 페이지를 선택하세요.")

elif menu == "충전소 지도":
    st.title("🔌 전기차 충전소 위치 확인")

    st.markdown("📍 현재 위치를 기준으로 반경 5km 이내 충전소를 확인해보세요!")

    # 현재 위치 설정 (더미 위치: 서울 시청)
    current_lat = 37.5665
    current_lng = 126.9780

    # 더미 충전소 데이터
    chargers = [
        {
            "name": "서울시청 충전소 📍",
            "lat": 37.5665,
            "lng": 126.9780,
            "status": "충전 가능 ⚡️",
            "price": "300원/kWh 🔋",
            "idle_fee": "점거비용 있음 💸",
            "free_parking": "무료 주차 가능 🅿️"
        },
        {
            "name": "을지로입구 충전소 📍",
            "lat": 37.5660,
            "lng": 126.9820,
            "status": "충전 중 🔌",
            "price": "250원/kWh 🔋",
            "idle_fee": "점거비용 없음 ✅",
            "free_parking": "무료 주차 불가 ❌"
        }
    ]

    # 지도 생성
    m = folium.Map(location=[current_lat, current_lng], zoom_start=15)

    # 현재 위치 마커
    folium.Marker(
        [current_lat, current_lng],
        tooltip="현재 위치 📍",
        icon=folium.Icon(color="blue", icon="star")
    ).add_to(m)

    # 충전소 마커 추가
    for charger in chargers:
        tooltip = charger["name"]
        popup_html = f"""
        <div style="font-weight:bold; margin-bottom:8px;">{charger['name']}</div>
        <div style="margin-bottom:6px;">⚡ 상태: {charger['status']}</div>
        <div style="margin-bottom:6px;">💰 가격: {charger['price']}</div>
        <div style="margin-bottom:6px;">💸 점거비용: {charger['idle_fee']}</div>
        <div>🅿️ 무료 주차: {charger['free_parking']}</div>
        """
        folium.Marker(
            [charger["lat"], charger["lng"]],
            tooltip=tooltip,
            popup=popup_html,
            icon=folium.Icon(color="green", icon="flash")
        ).add_to(m)

    # 지도 표시
    st_folium(m, width=900, height=600)

elif menu == "앱 정보":
    st.title("앱 정보")
    st.markdown("""
    - 제작 동기: 전기차 충전소 위치와 상태를 한눈에 확인하기 위해 개발했습니다.  
    - 주요 기능: 위치 기반 충전소 지도 표시, 충전소 상태 및 가격 정보 팝업 제공  
    - 개발 환경: Python, Streamlit, Folium  
    - 팀원: 홍길동, 김철수, 이영희  
    """)
