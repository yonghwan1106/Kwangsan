import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# 가상의 데이터 생성
@st.cache_data
def load_data():
    districts = [
        '송정1동', '송정2동', '도산동', '신가동', '신창동', 
        '운남동', '월곡1동', '월곡2동', '첨단1동', '첨단2동',
        '소촌동', '우산동', '비아동', '수완동', '하남동'
    ]
    data = {
        'district': districts,
        'carbon_emission': np.random.randint(80, 220, len(districts)),
        'energy_efficiency': np.random.choice(['A', 'B', 'C', 'D', 'E'], len(districts)),
        'population': np.random.randint(5000, 50000, len(districts)),
        'green_area': np.random.randint(1000, 10000, len(districts)),
        'public_transport_usage': np.random.randint(20, 80, len(districts)),
        'latitude': np.random.uniform(35.1, 35.2, len(districts)),
        'longitude': np.random.uniform(126.8, 126.9, len(districts))
    }
    df = pd.DataFrame(data)
    df['carbon_per_capita'] = df['carbon_emission'] / (df['population'] / 1000)
    return df

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

    metric_options = {
        '탄소 배출량': 'carbon_emission',
        '인구 당 탄소 배출량': 'carbon_per_capita',
        '인구': 'population',
        '녹지 면적': 'green_area',
        '대중교통 이용률': 'public_transport_usage'
    }
    selected_metric = st.sidebar.selectbox('표시할 지표', list(metric_options.keys()))

    # 데이터 필터링
    filtered_df = df[df['district'].isin(selected_districts)]

    # 탭 생성
    tab1, tab2, tab3, tab4 = st.tabs(["지도", "차트", "상관관계", "데이터"])

    with tab1:
        st.subheader('탄소발자국 지도')
        st.map(filtered_df, latitude='latitude', longitude='longitude', size=metric_options[selected_metric])

    with tab2:
        st.subheader(f'지역별 {selected_metric}')
        chart = alt.Chart(filtered_df).mark_bar().encode(
            x='district',
            y=metric_options[selected_metric],
            color='energy_efficiency',
            tooltip=['district', metric_options[selected_metric], 'energy_efficiency']
        ).interactive()
        st.altair_chart(chart, use_container_width=True)

    with tab3:
        st.subheader('변수 간 상관관계')
        correlation = filtered_df[list(metric_options.values())].corr()
        st.dataframe(correlation.round(2))  # 소수점 2자리까지 표시
        st.write("1에 가까울수록 강한 양의 상관관계, -1에 가까울수록 강한 음의 상관관계를 나타냅니다.")

    with tab4:
        st.subheader('데이터 테이블')
        st.dataframe(filtered_df)

    # 탄소 저감 제안
    st.subheader('탄소 저감을 위한 제안')
    if st.button('탄소 저감 아이디어 생성'):
        ideas = [
            "대중교통 이용 장려 프로그램 도입",
            "건물 에너지 효율 개선 지원",
            "재생에너지 사용 확대",
            "녹지 공간 확충",
            "자전거 도로 확대",
            "에너지 효율이 낮은 건물 개선 집중",
            "지역별 탄소 중립 목표 설정",
            "주민 참여형 탄소 저감 캠페인 실시",
            "친환경 기업 유치 및 지원",
            "폐기물 재활용 및 업사이클링 센터 설립"
        ]
        for idea in ideas:
            st.write(f"- {idea}")

    # 지역 비교 기능
    st.subheader('지역 비교')
    col1, col2 = st.columns(2)
    with col1:
        district1 = st.selectbox('첫 번째 지역', df['district'].unique(), key='district1')
    with col2:
        district2 = st.selectbox('두 번째 지역', df['district'].unique(), key='district2')

    if district1 and district2:
        comparison_df = df[df['district'].isin([district1, district2])]
        comparison_chart = alt.Chart(comparison_df).mark_bar().encode(
            x='district',
            y=alt.Y(metric_options[selected_metric], title=selected_metric),
            color='district',
            column='variable',
            tooltip=['district', 'variable', 'value']
        ).transform_fold(
            list(metric_options.values()),
            as_=['variable', 'value']
        ).interactive()
        st.altair_chart(comparison_chart, use_container_width=True)

if __name__ == "__main__":
    main()
