import streamlit as st
import folium
from streamlit_folium import st_folium
from math import sqrt

st.set_page_config(page_title="전기차 충전소 지도", layout="wide")

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

default_location = [37.5665, 126.9780]

st.title("🚗 전기차 충전소 지도")

col1, col2 = st.columns([3, 1])

with col1:
    m = folium.Map(location=default_location, zoom_start=16)

    for charger in chargers:
        folium.Marker(
            [charger["lat"], charger["lng"]],
            tooltip=charger["name"],
            icon=folium.Icon(color="green", icon="flash")
        ).add_to(m)

    # 현재 위치 마커
    folium.Marker(
        default_location,
        tooltip="현재 위치 📍",
        icon=folium.Icon(color="blue", icon="star")
    ).add_to(m)

    # folium 지도 렌더링 및 클릭 이벤트 정보 받아오기
    map_data = st_folium(m, width=800, height=600)

clicked_latlng = map_data.get("last_clicked")

selected = None
if clicked_latlng is not None:
    click_lat = clicked_latlng["lat"]
    click_lng = clicked_latlng["lng"]

    # 클릭 좌표와 가장 가까운 충전소 찾기 (단순 유클리드 거리)
    def dist(c):
        return sqrt((c["lat"] - click_lat)**2 + (c["lng"] - click_lng)**2)

    selected = min(chargers, key=dist)
else:
    selected = chargers[0]  # 기본값

with col2:
    st.header("충전소 정보")
    st.markdown(f"""
    ### {selected['name']}
    - **상태:** {selected['status']}
    - **가격:** {selected['price']}
    - **점거비용:** {selected['idle_fee']}
    - **무료 주차:** {selected['free_parking']}
    """)

