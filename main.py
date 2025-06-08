import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# GitHub Raw URLs
url1 = "https://raw.githubusercontent.com/ZackWoo05/Sehwa/234c446f6e368583be840f2a93aceea87e112151/chargerinfo_part1.csv"
url2 = "https://raw.githubusercontent.com/ZackWoo05/Sehwa/234c446f6e368583be840f2a93aceea87e112151/chargerinfo_part2.csv"

st.set_page_config(page_title="전기차 충전소 지도", layout="wide")
st.title("🔌 전국 전기차 충전소 클러스터 지도")

@st.cache_data
def load_combined_data(url1, url2):
    df1 = pd.read_csv(url1, low_memory=False)
    df2 = pd.read_csv(url2, low_memory=False)
    df = pd.concat([df1, df2], ignore_index=True)

    # 위도경도 분리
    df[['위도', '경도']] = df['위도경도'].str.split(',', expand=True)

    # 숫자형 변환 (오류는 NaN으로 처리)
    df['위도'] = pd.to_numeric(df['위도'], errors='coerce')
    df['경도'] = pd.to_numeric(df['경도'], errors='coerce')

    # NaN 제거
    df.dropna(subset=['위도', '경도'], inplace=True)

    # 대한민국 좌표 범위로 제한 (예외 제거)
    df = df[(df['위도'] > 33) & (df['위도'] < 39) & (df['경도'] > 124) & (df['경도'] < 132)]

    return df

df = load_combined_data(url1, url2)

# 지역(시도) 필터 추가
if '시도' in df.columns:
    시도_목록 = ["전체 보기"] + sorted(df['시도'].dropna().unique())
    선택한_시도 = st.selectbox("📍 지역(시/도) 선택", 시도_목록)
    if 선택한_시도 != "전체 보기":
        df = df[df['시도'] == 선택한_시도]

# 마커 수 제한 (최대 300개)
df = df.head(300)

# 지도 중심: 서울 세화고등학교
map_center = [37.5009, 126.9872]
m = folium.Map(location=map_center, zoom_start=13)

# 마커 클러스터 적용
marker_cluster = MarkerCluster().add_to(m)

# 마커 추가
for _, row in df.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        tooltip=row['충전소명'],
        popup=folium.Popup(f"""
            <b>{row['충전소명']}</b><br>
            📍 주소: {row['주소']}<br>
            ⚡ 충전기 타입: {row['충전기타입']}<br>
            🏢 시설: {row['시설구분(대)']} - {row['시설구분(소)']}<br>
        """, max_width=300),
        icon=folium.Icon(color="green", icon="flash")
    ).add_to(marker_cluster)

# Streamlit에서 지도 출력
st_folium(m, width=900, height=600)
