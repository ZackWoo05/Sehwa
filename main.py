# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(page_title="전기차 충전소 지도", layout="wide")

menu = st.sidebar.radio("메뉴 선택", ["홈", "충전소 지도", "차량별 충전 호환정보", "앱 정보"])

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

csv_url = "https://raw.githubusercontent.com/ZackWoo05/Sehwa/main/chargerinfo_sample.csv"

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df[['위도', '경도']] = df['위도경도'].str.split(',', expand=True)
    df['위도'] = df['위도'].astype(str).str.strip().astype(float)
    df['경도'] = df['경도'].astype(str).str.strip().astype(float)
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

# 입력 주소 기준 지도 중심
address = st.text_input("📍 위치를 입력하세요 (예: 래미안 원펜타스)", "")
default_lat, default_lng = 37.5665, 126.9780
lat, lng = kakao_geocode(address) if address else (None, None)
map_center = [lat, lng] if lat and lng else [default_lat, default_lng]
if address and (lat is None or lng is None):
    st.warning("❌ 유효한 주소가 아니거나 찾을 수 없습니다. 기본 위치(서울 시청)로 설정합니다.")

if menu == "홈":
    st.title("🚗 전기차 충전소 위치 확인 웹앱")
    st.write("왼쪽 메뉴에서 기능을 선택하세요.")

elif menu == "충전소 지도":
    st.title("🔌 전기차 충전소 위치 확인")
    df = load_data(csv_url)

    m = folium.Map(location=map_center, zoom_start=14)
    folium.Marker(map_center, tooltip="검색된 위치 📍", icon=folium.Icon(color="blue", icon="search")).add_to(m)

    for _, row in df.iterrows():
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

elif menu == "차량별 충전 호환정보":
    st.title("🚙 차량별 충전 호환정보")
    selected_car = st.selectbox("차량을 선택하세요", ["전체 보기"] + list(vehicle_info.keys()))
    if selected_car == "전체 보기":
        st.write("전체 차량 정보:")
        st.dataframe(pd.DataFrame(vehicle_info).T)
    else:
        info = vehicle_info[selected_car]
        st.markdown(f"""
        ### 🚗 {selected_car}
        - 충전기: {", ".join(info["충전기"])}
        - 어댑터 필요 여부: {"필요" if info["어댑터 필요"] else "불필요"}
        - 배터리 용량: {info["배터리"]}
        - 1회 주행거리: {info["주행거리"]}
        - 급속 충전시간: {info["충전시간"]}
        """)

elif menu == "앱 정보":
    st.title("ℹ️ 앱 정보")
    st.markdown("""
    - 목적: 전기차 충전소 위치 및 차량별 호환 정보 제공  
    - 기능: 위치 기반 충전소 지도, 차량 충전 호환표, 주소 검색 기능  
    - 기술 스택: Python, Streamlit, Pandas, Folium, Kakao Map API  
    - 개발자: ZackWoo05
    """)
