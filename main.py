# -*- coding: utf-8 -*-
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="전기차 충전소 지도", layout="wide")

menu = st.sidebar.radio("메뉴 선택", ["홈", "충전소 지도", "차량별 충전 호환정보", "앱 정보"])

# 🔌 차량 정보 데이터
vehicle_info = {
    "테슬라 모델 3": {
        "충전기": ["DC콤보", "AC완속"],
        "어댑터 필요": True,
        "배터리": "57.5~82 kWh",
        "주행거리": "400~500km",
        "충전시간": "30분 (급속 기준)"
    },
    "현대 아이오닉5": {
        "충전기": ["DC콤보", "AC완속"],
        "어댑터 필요": False,
        "배터리": "72.6 kWh",
        "주행거리": "429~458km",
        "충전시간": "18분 (350kW 급속)"
    },
    "기아 EV6": {
        "충전기": ["DC콤보", "AC완속"],
        "어댑터 필요": False,
        "배터리": "77.4 kWh",
        "주행거리": "400~475km",
        "충전시간": "18분 (350kW 급속)"
    },
    "닛산 리프": {
        "충전기": ["차데모", "AC완속"],
        "어댑터 필요": False,
        "배터리": "40~62 kWh",
        "주행거리": "250~350km",
        "충전시간": "40분"
    }
}

# 🚘 충전소 데이터
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

if menu == "홈":
    st.title("🚗 전기차 충전소 위치 확인 웹앱에 오신 것을 환영합니다!")
    st.write("왼쪽 메뉴에서 원하는 페이지를 선택하세요.")

elif menu == "충전소 지도":
    st.title("🔌 전기차 충전소 위치 확인")
    st.markdown("📍 차량을 선택하면 해당 차량에 맞는 충전소만 지도에 표시됩니다.")

    # 차량 선택 옵션 (전체 추가)
    vehicle_options = ["전체"] + list(vehicle_info.keys())
    selected_vehicle = st.selectbox("🚘 내 차량을 선택하세요", vehicle_options)

    # 현재 위치 기준 지도 생성
    current_lat, current_lng = 37.5665, 126.9780
    m = folium.Map(location=[current_lat, current_lng], zoom_start=15)

    # 현재 위치 마커
    folium.Marker(
        [current_lat, current_lng],
        tooltip="현재 위치 📍",
        icon=folium.Icon(color="blue", icon="star")
    ).add_to(m)

    # 🔎 마커 필터링
    for charger in chargers:
        charger_types = [t.strip() for t in charger["type"].split(",")]

        # 전체 선택 시 모든 충전소 표시
        if selected_vehicle == "전체" or any(ct in vehicle_info.get(selected_vehicle, {}).get("충전기", []) for ct in charger_types):
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
                tooltip=charger["name"],
                popup=folium.Popup(popup_html, max_width=250),
                icon=folium.Icon(color="green", icon="flash")
            ).add_to(m)

    st_folium(m, width=900, height=600)

elif menu == "차량별 충전 호환정보":
    st.title("🚘 차량별 충전 호환 정보")

    vehicle_options = ["전체"] + list(vehicle_info.keys())
    selected_vehicle = st.selectbox("차량 선택", vehicle_options)

    if selected_vehicle == "전체":
        st.info("전체를 선택하면 호환 정보가 제공되지 않습니다. 특정 차량을 선택해 주세요.")
    else:
        info = vehicle_info[selected_vehicle]
        st.markdown(f"### ✅ {selected_vehicle} 제원 정보")
        st.write(f"🔌 호환 충전기: {', '.join(info['충전기'])}")
        st.write(f"🔧 어댑터 필요: {'예' if info['어댑터 필요'] else '아니오'}")
        st.write(f"🔋 배터리 용량: {info['배터리']}")
        st.write(f"🚗 1회 주행거리: {info['주행거리']}")
        st.write(f"⚡ 예상 충전 시간: {info['충전시간']}")

elif menu == "앱 정보":
    st.title("앱 정보")
    st.markdown("""
    - 제작 동기: 전기차 충전소 위치와 상태를 한눈에 확인하기 위해 개발했습니다.  
    - 주요 기능: 위치 기반 충전소 지도 표시, 차량별 호환 충전소 필터링, 상세 제원 제공  
    - 개발 환경: Python, Streamlit, Folium  
    - 팀원: 홍길동, 김철수, 이영희  
    """)
