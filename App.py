import streamlit as st
import pandas as pd
import plotly.express as px

# 가상의 데이터 생성
@st.cache_data
def load_data():
    data = {
        'district': ['송정1동', '송정2동', '도산동', '신가동', '신창동'],
        'carbon_emission': [120, 150, 90, 200, 180],
        'energy_efficiency': ['B', 'C', 'A', 'D', 'C'],
        'latitude': [35.1368, 35.1398, 35.1528, 35.1608, 35.1778],
        'longitude': [126.7928, 126.7958, 126.8088, 126.8168, 126.8338]
    }
    return pd.DataFrame(data)

def main():
    st.title('광산구 탄소발자국 지도')

    # 데이터 로드
    df = load_data()

    # 사이드바 - 필터링 옵션
    st.sidebar.header('필터링 옵션')
    selected_districts = st.sidebar.multiselect(
        '지역 선택',
        options=df['district'].unique(),
        default=df['district'].unique()
    )

    # 데이터 필터링
    filtered_df = df[df['district'].isin(selected_districts)]

    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["지도", "차트", "파이 차트"])

    with tab1:
        st.subheader('탄소발자국 지도')
        fig_map = px.scatter_mapbox(filtered_df, 
                                    lat="latitude", 
                                    lon="longitude", 
                                    size="carbon_emission",
                                    color="carbon_emission",
                                    hover_name="district", 
                                    zoom=11,
                                    mapbox_style="open-street-map")
        st.plotly_chart(fig_map)

    with tab2:
        st.subheader('지역별 탄소 배출량')
        fig_bar = px.bar(filtered_df, x='district', y='carbon_emission', 
                         color='energy_efficiency', 
                         labels={'carbon_emission': '탄소 배출량', 'district': '지역'})
        st.plotly_chart(fig_bar)

    with tab3:
        st.subheader('에너지 효율 등급 분포')
        fig_pie = px.pie(filtered_df, names='energy_efficiency', values='carbon_emission',
                         title='에너지 효율 등급별 탄소 배출량 분포')
        st.plotly_chart(fig_pie)

    # 탄소 저감 제안
    st.subheader('탄소 저감을 위한 제안')
    if st.button('탄소 저감 아이디어 생성'):
        ideas = [
            "대중교통 이용 장려 프로그램 도입",
            "건물 에너지 효율 개선 지원",
            "재생에너지 사용 확대",
            "녹지 공간 확충",
            "자전거 도로 확대"
        ]
        for idea in ideas:
            st.write(f"- {idea}")

if __name__ == "__main__":
    main()
