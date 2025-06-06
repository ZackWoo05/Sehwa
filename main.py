import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="전기차 충전소 지도", layout="wide")

menu = st.sidebar.selectbox("메뉴 선택", ["홈", "충전소 지도", "앱 정보"])

if menu == "홈":
    st.title("🚗 전기차 충전소 위치 확인 웹앱에 오신 것을 환영합니다!")
    st.write("왼쪽 메뉴에서 원하는 페이지를 선택하세요.")

elif menu == "충전소 지도":
    st.title("🔌 충전소 지도")

    # 현재 위치 (더미)
    current_lat, current_lng = 37.5665, 126.9780

    chargers = [
        {
            "name": "서울시청 충전소 📍",
            "lat": 37.5665,
            "lng": 126.9780,
            "status": "충전 가능 ⚡️",
            "price": "300원/kWh",
            "idle_fee": "점거비용 있음 💸",
            "free_parking": "무료 주차 가능 🅿️"
        },
        {
            "name": "을지로입구 충전소 📍",
            "lat": 37.5660,
            "lng": 126.9820,
            "status": "충전 중 🔌",
            "price": "250원/kWh",
            "idle_fee": "점거비용 없음 ✅",
            "free_parking": "무료 주차 불가 ❌"
        }
    ]

    m = folium.Map(location=[current_lat, current_lng], zoom_start=15)

    folium.Marker(
        [current_lat, current_lng],
        tooltip="현재 위치 📍",
        icon=folium.Icon(color="blue", icon="star")
    ).add_to(m)

    for charger in chargers:
        # 보기 좋은 HTML로 정보 꾸미기
        popup_html = f"""
        <div style="font-family: 'Arial'; line-height: 1.5;">
            <h4 style="margin-bottom:5px;">{charger['name']}</h4>
            <p style="margin:0;"><strong>상태:</strong> {charger['status']}</p>
            <p style="margin:0;"><strong>가격:</strong> {charger['price']}</p>
            <p style="margin:0;"><strong>점거비용:</strong> {charger['idle_fee']}</p>
            <p style="margin:0;"><strong>무료 주차:</strong> {charger['free_parking']}</p>
        </div>
        """
        folium.Marker(
            [charger["lat"], charger["lng"]],
            tooltip=charger["name"],
            popup=popup_html,
            icon=folium.Icon(color="green", icon="flash")
        ).add_to(m)

    st_folium(m, width=900, height=600)

elif menu == "앱 정보":
    st.title("앱 정보")
    st.markdown("""
    - 제작 동기: 전기차 충전소 위치와 상태를 한눈에 보고 싶어서  
    - 주요 기능: 위치 기반 충전소 지도 표시, 상태 및 가격 정보 팝업 제공  
    - 개발 환경: Python, Streamlit, Folium  
    - 팀원: 홍길동, 김철수, 이영희  
    """)
