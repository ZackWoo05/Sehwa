# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="전기차 충전소 지도", layout="wide")

menu = st.sidebar.radio("메뉴 선택", ["홈", "충전소 지도", "앱 정보"])

# GitHub 파일 URL (raw 주소로 바꿔주세요)
excel_url = "https://raw.githubusercontent.com/USERNAME/REPO/main/chargerinfo.xlsx"

@st.cache_data
def load_data(url):
    df = pd.read_excel(url)
    df[['위도', '경도']] = df['위도경도'].str.split(",", expand=True).astype(float)
    return df

df = load_data(excel_url)

if menu == "홈":
    st.title("🚗 전기차 충전소 위치 확인 웹앱에 오신 것을 환영합니다!")
    st.write("왼쪽 메뉴에서 원하는 페이지를 선택하세요.")

elif menu == "충전소 지도":
    st.title("🔌 전기차 충전소 위치 확인")
    st.markdown("📍 GitHub에서 불러온 충전소 위치를 지도에 표시합니다.")

    # 기본 지도 위치
    map_center = [df['위도'].mean(), df['경도'].mean()]
    m = folium.Map(location=map_center, zoom_start=11)

    for _, row in df.iterrows():
        popup_html = f"""
        <div style="min-width:180px; max-width:250px; font-size:13px; line-height:1.4; white-space:nowrap;">
            <strong>{row['충전소명']}</strong><br>
            📍 주소: {row['주소']}<br>
            🔌 충전기 타입: {row['충전기타입']}<br>
            ⚡ 충전량: {row['급속충전량']}<br>
            🏢 시설구분: {row['시설구분(대)']} - {row['시설구분(소)']}<br>
            🚫 제한사항: {row['이용자제한']}
        </div>
        """
        folium.Marker(
            location=[row['위도'], row['경도']],
            tooltip=row['충전소명'],
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(color="green", icon="flash")
        ).add_to(m)

    st_folium(m, width=900, height=600)

elif menu == "앱 정보":
    st.title("앱 정보")
    st.markdown("""
    - 데이터 출처: GitHub에 업로드한 chargerinfo.xlsx  
    - 주요 기능: 전국 충전소 위치 지도 표시, 충전기 정보 팝업  
    - 기술 스택: Python, Streamlit, Pandas, Folium  
    """)
