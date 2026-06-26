import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import platform
import koreanize-matplotlib




# 마이너스 기호(-)가 깨지는 현상 방지
plt.rc('axes', unicode_minus=False)
# =================================================================


# 1. 스트림릿 페이지 레이아웃 설정
st.set_page_config(page_title="교통사고 통계 대시보드", layout="wide")
st.title("🚗 교통사고 사상자 연령층별/성별 통계 대시보드")
st.markdown("한국도로교통공단 데이터를 활용하여 연령층 및 성별 사상자 현황을 시각화한 대시보드입니다.")

# 2. 데이터 로드 (캐싱을 적용하여 새로고침 시 속도 향상)
@st.cache_data
def load_data():
    return pd.read_csv('한국도로교통공단_사상자 연령층별 성별 교통사고 통계_20241231.csv', encoding='cp949')

try:
    car_combined = load_data()

    # 총 사상자수 계산
    car_combined['총 사상자수'] = car_combined['사망자수'] + car_combined['중상자수'] + car_combined['경상자수'] + car_combined['부상신고자수']

    # 데이터프레임 확인 섹션
    st.subheader("📋 데이터 미리보기 (상위 5개 행)")
    st.dataframe(car_combined.head(), use_container_width=True)

    st.write("---")

    # 3. 시각화 섹션
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('👥 연령층별 총 교통사고 사상자수')
        casualties_by_age_combined = car_combined.groupby('사상자연령층')['총 사상자수'].sum().reset_index()

        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='사상자연령층', y='총 사상자수', data=casualties_by_age_combined, palette='viridis', ax=ax1)
        ax1.set_title('연령층별 총 교통사고 사상자수', fontsize=14)
        ax1.set_xlabel('사상자 연령층', fontsize=11)
        ax1.set_ylabel('총 사상자수', fontsize=11)
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right', fontsize=9)
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig1)

    with col2:
        st.subheader('👫 연령층별 성별 사상자수 비교')
        casualties_by_age_gender_combined = car_combined.groupby(['사상자연령층', '사상자성별'])['총 사상자수'].sum().reset_index()

        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='사상자연령층', y='총 사상자수', hue='사상자성별', data=casualties_by_age_gender_combined, 
                    palette={'남': 'skyblue', '여': 'salmon', '기타/불명': 'grey'}, ax=ax2)
        ax2.set_title('연령층별 성별 총 교통사고 사상자수 비교', fontsize=14)
        ax2.set_xlabel('사상자 연령층', fontsize=11)
        ax2.set_ylabel('총 사상자수', fontsize=11)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right', fontsize=9)
        ax2.legend(title='성별', fontsize=9, title_fontsize=10)
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig2)

except FileNotFoundError:
    st.error("⚠️ CSV 파일을 찾을 수 없습니다. 깃허브 리포지토리에 파일이 올바르게 업로드되었는지 파일명을 확인해주세요.")
