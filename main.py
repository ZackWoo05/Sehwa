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

csv_path = "chargerinfo_sample.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    # 위도경도 분리
    df[['위도', '경도']] = df['위도경도'].str.split(',', expand=True).astype(float)
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

address = st.text_input("📍 위치를 입력하세요 (예: 래미안 원펜타스)", "")
default_lat, default_lng = 37.5665, 126.9780
lat, lng = kakao_geocode(address) if address else (None, None)
map_center = [lat, lng] if lat and lng else [default_lat, default_lng]

if menu == "충전소 지도":
    st.title("🔌 전기차 충전소 위치 확인")
    df = load_data(csv_path)
    m = folium.Map(location=map_center, zoom_start=14)
    folium.Marker(map_center, tooltip="검색된 위치 📍", icon=folium.Icon(color="blue", icon="search")).add_to(m)
    for _, row in df.iterrows():
        folium.Marker(
            [row['위도'], row['경도']],
            tooltip=row['충전소명'],
            popup=folium.Popup(f"""
                <b>{row['충전소명']}</b><br>
                📍 주소: {row['주소']}<br>
                ⚡ 충전기 타입: {row['충전기타입']}<br>
                🏢 시설: {row['시설구분(대)']} - {row['시설구분(소)']}<br>
            """, max_width=300),
            icon=folium.Icon(color="green", icon="flash")
        ).add_to(m)
    st_folium(m, width=900, height=600)

elif menu == "차량별 충전 호환정보":
    st.title("🚘 차량별 충전 호환 정보")
    selected_car = st.selectbox("차량을 선택하세요", ["전체 보기"] + list(vehicle_info.keys()))
    if selected_car == "전체 보기":
        for name, info in vehicle_info.items():
            with st.expander(name):
                st.write(info)
    else:
        st.write(vehicle_info[selected_car])

elif menu == "홈":
    st.title("🚗 전기차 충전소 위치 확인 웹앱에 오신 것을 환영합니다!")
    st.write("왼쪽 메뉴에서 원하는 페이지를 선택하세요.")

elif menu == "앱 정보":
    st.title("앱 정보")
    st.markdown("""
    - 제작 동기: 전기차 충전소 위치와 상태를 한눈에 확인하기 위해 개발했습니다.  
    - 주요 기능: 위치 기반 충전소 지도 표시, 충전소 상태 및 차량별 호환 정보 제공  
    - 개발 환경: Python, Streamlit, Folium  
    - 팀원: 홍길동, 김철수, 이영희  
    """)
