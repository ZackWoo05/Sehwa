import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="전기차 충전소 지도", layout="wide")

# 더미 데이터
chargers = [
    {
        "id": 1,
        "name": "서울시청 충전소 📍",
        "lat": 37.5665,
        "lng": 126.9780,
        "status": "충전 가능 ⚡️",
        "price": "300원/kWh",
        "idle_fee": "점거비용 있음 💸",
        "free_parking": "무료 주차 가능 🅿️"
    },
    {
        "id": 2,
        "name": "을지로입구 충전소 📍",
        "lat": 37.5660,
        "lng": 126.9820,
        "status": "충전 중 🔌",
        "price": "250원/kWh",
        "idle_fee": "점거비용 없음 ✅",
        "free_parking": "무료 주차 불가 ❌"
    }
]

menu = st.sidebar.selectbox("메뉴 선택", ["홈", "충전소 지도", "앱 정보"])

if menu == "홈":
    st.title("🚗 전기차 충전소 위치 확인 웹앱에 오신 것을 환영합니다!")
    st.write("왼쪽 메뉴에서 원하는 페이지를 선택하세요.")

elif menu == "충전소 지도":
    st.title("🔌 충전소 지도")

    # 기본 위치 (예시)
    default_location = [37.5665, 126.9780]

    # 좌우 레이아웃: 지도 + 상세 정보
    col1, col2 = st.columns([3, 1])

    with col2:
        st.header("충전소 선택")
        selected_name = st.selectbox(
            "충전소 목록",
            options=[charger["name"] for charger in chargers]
        )

        selected = next(charger for charger in chargers if charger["name"] == selected_name)

        st.markdown(f"""
        ### {selected['name']}
        - **상태:** {selected['status']}
        - **가격:** {selected['price']}
        - **점거비용:** {selected['idle_fee']}
        - **무료 주차:** {selected['free_parking']}
        """)

    with col1:
        m = folium.Map(location=[selected['lat'], selected['lng']], zoom_start=16)

        folium.Marker(
            default_location,
            tooltip="현재 위치 📍",
            icon=folium.Icon(color="blue", icon="star")
        ).add_to(m)

        for charger in chargers:
            color = "green" if charger["name"] == selected_name else "gray"
            folium.Marker(
                [charger["lat"], charger["lng"]],
                tooltip=charger["name"],
                icon=folium.Icon(color=color, icon="flash")
            ).add_to(m)

        st_folium(m, width=800, height=600)

elif menu == "앱 정보":
    st.title("앱 정보")
    st.markdown("""
    - 제작 동기: 전기차 충전소 위치와 상태를 한눈에 보고 싶어서  
    - 주요 기능: 위치 기반 충전소 지도 표시, 상태 및 가격 정보 팝업 제공  
    - 개발 환경: Python, Streamlit, Folium  
    - 팀원: 홍길동, 김철수, 이영희  
    """)
