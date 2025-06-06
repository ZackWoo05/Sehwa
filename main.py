# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests
import urllib3

# SSL 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
    df[['위도', '경도']] = df[['위도', '경도']].astype(float)
    return df

def kakao_geocode(address):
    api_key = "8e3a592f2b86c799c3be4f26f492a5d5"
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": address}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5, verify=False)
        if response.status_code == 200:
            result = response.json()
            if result['documents']:
                lat = float(result['documents'][0]['y'])
                lng = float(result['documents'][0]['x'])
                return lat, lng
    except Exception as e:
        st.error(f"❌ 주소 변환 실패: {e}")
    return None, None

# 지도 중심 설정 처리
address = st.text_input("📍 위치를 입력하세요 (예: 래미안 원펜타스)", "")
default_lat, default_lng = 37.5665, 126.9780
lat, lng = kakao_geocode(address) if address else (None, None)
if lat is not None and lng is not None:
    map_center = [lat, lng]
else:
    if address:
        st.warning("❌ 유효한 주소가 아니거나 지도에서 찾을 수 없습니다. 기본 위치(서울 시청)로 설정합니다.")
    map_center = [default_lat, default_lng]

if menu == "충전소 지도":
    st.title("🔌 전기차 충전소 위치 확인")
    df = load_data(csv_url)

    m = folium.Map(location=map_center, zoom_start=14)
    folium.Marker(
        location=map_center,
        tooltip="검색된 위치 📍",
        icon=folium.Icon(color="blue", icon="search")
    ).add_to(m)

    for i, row in df.iterrows():
        folium.Marker(
            [row["위도"], row["경도"]],
            tooltip=row["충전소명"],
            popup=folium.Popup(f"""
                <b>{row['충전소명']}</b><br>
                📍 주소: {row['주소']}<br>
                ⚡ 충전기 타입: {row['충전기타입']}<br>
                💰 요금: {row['이용요금']}<br>
                🅿️ 주차: {row['주차여부']}<br>
            """, max_width=300),
            icon=folium.Icon(color="green", icon="flash")
        ).add_to(m)

    st_folium(m, width=900, height=600)
