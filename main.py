# -*- coding: utf-8 -*-
import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="전기차 충전소 지도", layout="wide")

# 사이드바 메뉴
menu = st.sidebar.radio("메뉴 선택", ["홈", "충전소 지도", "충전기별 지원 차량", "앱 정보"])

if menu == "홈":
    st.title("🚗 전기차 충전소 위치 확인 웹앱에 오신 것을 환영합니다!")
    st.write("왼쪽 메뉴에서 원하는 페이지를 선택하세요.")

elif menu == "충전소 지도":
    st.title("🔌 전기차 충전소 위치 확인")
    st.markdown("📍 현재 위치를 기준으로 반경 5km 이내 충전소를 확인해보세요!")

    current_lat = 37.5665
    current_lng = 126.9780

    chargers = [
        {
            "name": "서울시청 충전소 📍",
            "lat": 37.5665,
            "lng": 126.9780,
            "status": "충전 가능 ⚡️",
            "price": "300원/kWh 🔋",
            "idle_fee": "점거비용 있음 💸",
            "free_parking": "무료 주차 가능 🅿️",
            "type": "DC콤보, AC완속"
        },
        {
            "name": "을지로입구 충전소 📍",
            "lat": 37.5660,
            "lng": 126.9820,
            "status": "충전 중 🔌",
            "price": "250원/kWh 🔋",
            "idle_fee": "점거비용 없음 ✅",
            "free_parking": "무료 주차 불가 ❌",
            "type": "차데모"
        }
    ]

    m = folium.Map(location=[current_lat, current_lng], zoom_start=15)

    folium.Marker(
        [current_lat, current_lng],
        tooltip="현재 위치 📍",
        icon=folium.Icon(color="blue", icon="star")
    ).add_to(m)

    for charger in chargers:
        tooltip = charger["name"]
        popup_html = f"""
        <div style="min-width:180px; max-width:250px; font-size:13px; line-height:1.4; white-space:nowrap;">
            <strong>{charger['name']}</strong><br>
            🔌 충전기 타입: {charger['type']}<br>
            ⚡ 상태: {charger['status']}<br>
            💰 가격: {charger['price']}<br>
            💸 점거비용: {charger['idle_fee']}<br>
            🅿️ 무료 주차: {charger['free_parking']}
        </div>
        """
        folium.Marker(
            [charger["lat"], charger["lng"]],
            tooltip=tooltip,
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(color="green", icon="flash")
        ).add_to(m)

    st_folium(m, width=900, height=600)

elif menu == "충전기별 지원 차량":
    st.title("🚘 충전기별 지원 차량 안내")

    # 충전기 타입 선택
    charger_type = st.selectbox("충전기 타입을 선택하세요", ["DC콤보", "AC완속", "차데모"])

    # 충전기별 차량 목록
    vehicle_dict = {
        "DC콤보": [
            "테슬라 모델 3/Y (어댑터 필요)",
            "현대 아이오닉5/6",
            "기아 EV6",
            "폭스바겐 ID.4",
            "BMW i4, iX",
        ],
        "AC완속": [
            "르노 조에",
            "쉐보레 볼트 EV",
            "현대 코나 EV",
            "기아 니로 EV",
            "테슬라 전 모델 (변환 어댑터 필요)",
        ],
        "차데모": [
            "닛산 리프",
            "기아 쏘울 EV (구형)",
            "미쓰비시 아웃랜더 PHEV",
        ]
    }

    st.markdown(f"### {charger_type} 지원 차량 목록")
    for car in vehicle_dict.get(charger_type, []):
        st.markdown(f"- {car}")

elif menu == "앱 정보":
    st.title("앱 정보")
    st.markdown("""
    - 제작 동기: 전기차 충전소 위치와 상태를 한눈에 확인하기 위해 개발했습니다.  
    - 주요 기능: 위치 기반 충전소 지도 표시, 충전소 상태 및 가격 정보 팝업 제공  
    - 개발 환경: Python, Streamlit, Folium  
    - 팀원: 홍길동, 김철수, 이영희  
    """)
