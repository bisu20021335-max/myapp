import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# 1. 스트림릿 페이지 설정 (제목 및 레이아웃)
st.set_page_config(page_title="캘리포니아 주택 데이터 대시보드", layout="wide")
st.title("📊 California Housing 데이터 분석 대시보드")
st.markdown("기존 데이터 분석 코드를 스트림릿 대시보드로 전환한 화면입니다.")

# 2. 데이터 로드 (캐싱을 적용하여 속도 향상)
@st.cache_data
def load_data():
    # 깃허브 리포지토리에 데이터 파일을 함께 올릴 것이므로 파일명만 지정합니다.
    return pd.read_csv('california_housing_train.csv')

try:
    df = load_data()

    # 3. 데이터프레임 출력
    st.subheader("📋 데이터프레임 미리보기 (상위 5개 행)")
    st.dataframe(df.head(), use_container_width=True)

    st.write("---")

    # 4. 시각화 섹션 (화면을 2분할하여 좌우로 배치)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('💵 소득 vs 주택 가치 관계')
        # 스트림릿에서는 객체지향 방식으로 fig, ax를 생성하는 것이 안전합니다.
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        ax1.scatter(df['median_income'], df['median_house_value'], alpha=0.5, color='#3498db')
        ax1.set_title('Median Income vs Median House Value')
        ax1.set_xlabel('Median Income')
        ax1.set_ylabel('Median House Value')
        ax1.grid(True)
        # plt.show() 대신 st.pyplot() 사용
        st.pyplot(fig1)

    with col2:
        st.subheader('🏠 주택 연식 분포')
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.hist(df['housing_median_age'], bins=30, edgecolor='black', color='#2ecc71')
        ax2.set_title('Distribution of Housing Median Age')
        ax2.set_xlabel('Housing Median Age')
        ax2.set_ylabel('Frequency')
        ax2.grid(True)
        st.pyplot(fig2)

except FileNotFoundError:
    st.error("⚠️ 'california_housing_train.csv' 파일을 찾을 수 없습니다. 깃허브 리포지토리에 파일이 올바르게 업로드되었는지 확인해주세요.")
