import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드 함수
def load_data():
    # 실제 데이터를 로드하는 코드로 대체해야 합니다.
    # 여기서는 예시 데이터를 생성합니다.
    df = pd.DataFrame({
        'latitude': [35.1595454, 35.1395454, 35.1495454],
        'longitude': [126.8526012, 126.8326012, 126.8426012],
        'building_name': ['건물A', '건물B', '건물C'],
        'energy_efficiency': ['A', 'B', 'C'],
        'carbon_emission': [100, 200, 150]
    })
    return df

# 메인 앱
def main():
    st.title('광산구 탄소발자국 지도')

    # 데이터 로드
    df = load_data()

    # 사이드바 - 필터링 옵션
    st.sidebar.header('필터링 옵션')
    selected_efficiency = st.sidebar.multiselect(
        '에너지 효율 등급',
        options=df['energy_efficiency'].unique(),
        default=df['energy_efficiency'].unique()
    )

    # 데이터 필터링
    filtered_df = df[df['energy_efficiency'].isin(selected_efficiency)]

    # 지도 표시
    st.subheader('탄소 배출량 지도')
    st.map(filtered_df, latitude='latitude', longitude='longitude', size='carbon_emission')

    # 통계 차트
    st.subheader('건물별 탄소 배출량')
    fig = px.bar(filtered_df, x='building_name', y='carbon_emission', 
                 title='건물별 탄소 배출량')
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
