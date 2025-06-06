# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

st.set_page_config(page_title="전기차 충전소 지도", layout="wide")

menu = st.sidebar.radio("메뉴 선택", ["홈", "충전소 지도", "차량별 충전 호환정보", "앱 정보"])

# 차량 정보 데이터
vehicle_info = {
    "테슬라 모델 3": {"충전기": ["DC콤보", "AC완속"], "어댑터 필요": True, "배터리": "57.5~82 kWh", "주행거리": "400~500km", "충전시간": "30분"},
    "테슬라 모델 S": {"충전기": ["DC콤보", "AC완속"], "어댑터 필요": True, "배터리": "95~100 kWh", "주행거리": "560~650km", "충전시간": "30분"},
    "테슬라 모델 X": {"충전기": ["DC콤보", "AC완속"], "어댑터 필요": True, "배터리": "95~100 kWh", "주행거리": "500~580km", "충전시간": "30분"},
    "테슬라 모델 Y": {"충전기": ["DC콤보", "AC완속"], "어댑터 필요": True, "배터리": "75~82 kWh", "주행거리": "400~510km", "충전시간": "30분"},
    "현대 아이오닉5": {"충전기": ["DC콤보", "AC완속"], "어댑터 필요": False, "배터리": "72.6 kWh", "주행거리": "429~458km", "충전시간": "18분"},
    "현대 아이오닉6": {"충전기": ["DC콤보", "AC완속"], "어댑터 필요": False, "배터리": "77.4 kWh", "주행거리": "500~610km", "충전시간": "18분"},
    "현대 아이오닉9": {"충전기": ["DC콤보", "AC완속"], "어댑터 필요": False, "배터리": "예정", "주행거리": "예정", "충전시간": "예정"},
    "기아 EV3": {"충전기": ["DC콤보", "AC완속"], "어댑터 필요": False, "배터리": "58~77 kWh", "주행거리": "400~500km", "충전시간": "18~25분"},
    "기아 EV6": {"충전기": ["DC콤보", "AC완속"], "어댑터 필요": False, "배터리": "77.4 kWh", "주행거리": "400~475km", "충전시간": "18분"},
    "기아 EV9": {"충전기": ["DC콤보", "AC완속"], "어댑터 필요": False, "배터리": "99.8 kWh", "주행거리": "500~550km", "충전시간": "24분"},
    "벤츠 EQE": {"충전기": ["DC콤보", "AC완속"], "어댑터 필요": False, "배터리": "90.6 kWh", "주행거리": "500~550km", "충전시간": "32분"},
    "BMW i4": {"충전기": ["DC콤보", "AC완속"], "어댑터 필요": False, "배터리": "80.7 kWh", "주행거리": "429~520km", "충전시간": "31분"},
    "닛산 리프": {"충전기": ["차데모", "AC완속"], "어댑터 필요": False, "배터리": "40~62 kWh", "주행거리": "250~350km", "충전시간": "40분"}
}

csv_url = "https://raw.githubusercontent.com/ZackWoo05/Sehwa/04a6d4ca291a442e85eba44f411f6f3aeeeb7399/chargerinfo_sample.csv"

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df[['위도', '경도']] = df['위도경도'].str.split(",", expand=True).astype(float)
    return df

df = load_data(csv_url)
chargers = df.to_dict(orient="records")

if menu == "홈":
    st.title("🚗 전기차 충전소 위치 확인 웹앱에 오신 것을 환영합니다!")
    st.write("왼쪽 메뉴에서 원하는 페이지를 선택하세요.")

elif menu == "충전소 지도":
    st.title("🔌 전기차 충전소 위치 확인")
    st.markdown("📍 위치를 입력하거나 차량을 선택하면 맞춤 정보를 확인할 수 있습니다.")

    address = st.text_input("📍 위치를 입력하세요 (예: 래미안 원펜타스)", "서울특별시 서초구 반포동")
    location = None
    if address:
        geolocator = Nominatim(user_agent="ev_map")
        try:
            location = geolocator.geocode(address, timeout=5)
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            st.error(f"❌ 위치 검색 중 오류 발생: {e}")
            location = None

    if location:
        map_center = [location.latitude, location.longitude]
    else:
        st.warning("⚠️ 해당 주소를 찾을 수 없습니다. 기본 위치(서울)로 설정됩니다.")
        map_center = [37.5665, 126.9780]

    vehicle_options = ["전체"] + list(vehicle_info.keys())
    selected_vehicle = st.selectbox("🚘 내 차량을 선택하세요", vehicle_options)

    m = folium.Map(location=map_center, zoom_start=12)

    folium.Marker(
        map_center,
        tooltip="현재 위치 📍",
        icon=folium.Icon(color="blue", icon="star")
    ).add_to(m)

    for charger in chargers:
        charger_types = [t.strip() for t in str(charger["충전기타입"]).split(",")]
        if selected_vehicle == "전체" or any(ct in vehicle_info.get(selected_vehicle, {}).get("충전기", []) for ct in charger_types):
            popup_html = f"""
            <div style="min-width:180px; max-width:250px; font-size:13px; line-height:1.4; white-space:nowrap;">
                <strong>{charger['충전소명']}</strong><br>
                📍 주소: {charger['주소']}<br>
                🔌 충전기 타입: {charger['충전기타입']}<br>
                ⚡ 충전량: {charger['급속충전량']}<br>
                🏢 시설구분: {charger['시설구분(대)']} - {charger['시설구분(소)']}<br>
                🚫 제한사항: {charger['이용자제한']}
            </div>
            """
            folium.Marker(
                location=[charger['위도'], charger['경도']],
                tooltip=charger['충전소명'],
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
    - 데이터 출처: GitHub (chargerinfo_sample.csv)  
    - 주요 기능: 위치 기반 충전소 지도 표시, 차량별 호환 충전소 필터링, 상세 제원 제공  
    - 개발 환경: Python, Streamlit, Folium  
    - 제작자: ZackWoo05  
    """)
