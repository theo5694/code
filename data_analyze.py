import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import os
from scipy.stats import chi2_contingency

# --- 페이지 설정 ---
st.set_page_config(
    page_title="AI 사용 분석 대시보드 (최종)",
    page_icon="🤖",
    layout="wide"
)

# --- 데이터 로딩 함수 ---
@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"'{file_path}' 파일을 찾을 수 없습니다. 경로를 확인하세요.")
        return None
    try:
        data = pd.read_csv(file_path)
        data['SessionDate'] = pd.to_datetime(data['SessionDate'])
        data['UsedAgain'] = data['UsedAgain'].astype(bool)
        return data
    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {e}")
        return None


# --- 데이터 로드 ---
FILE_PATH = r'C:\Users\user\Desktop\학교 프로젝트\pjt\soinsu\ai_assistant_usage_student_life.csv'
df = load_data(FILE_PATH)

# =========================================================================
# 📌 제목 및 개요
# =========================================================================
st.title("🤖 학생 AI 어시스턴트 사용 분석 대시보드")
st.markdown("---")

st.markdown("### 🔍 분석 개요")
st.markdown("이 대시보드는 **학생 AI 어시스턴트 사용 데이터**를 기반으로, 사용자의 특성(수준, 전공), 사용 행태(시간, 프롬프트 수)가 최종 **만족도와 재사용 의사**에 미치는 영향을 분석합니다.")

if df is not None:
    st.info(f"📊 **현재 데이터 (필터링 전):** 총 **{df.shape[0]:,}**개 행")

st.markdown("---")

with st.expander("📋 주요 변수 설명 (클릭하여 열기)"):
    st.markdown("""
    - **SessionID**: 세션 고유 ID  
    - **StudentLevel**: 학생 수준 (High School, Undergraduate, Graduate)  
    - **Discipline**: 전공 분야  
    - **SessionDate**: 세션 날짜  
    - **SessionLengthMin**: 세션 길이 (분 단위)  
    - **TotalPrompts**: 총 프롬프트(질문) 개수  
    - **TaskType**: 작업 유형  
    - **AI_AssistanceLevel**: AI 도움 수준 (1~5점)  
    - **FinalOutcome**: 세션 최종 결과  
    - **UsedAgain**: 재사용 의사 여부 (True/False)  
    - **SatisfactionRating**: 만족도 (1~5점)
    """)

st.markdown("---")

# =========================================================================
# 📊 데이터 필터
# =========================================================================
if df is not None:
    st.sidebar.header("📊 필터 옵션")

    selected_level = st.sidebar.multiselect(
        "학생 수준 선택", options=df['StudentLevel'].unique(),
        default=df['StudentLevel'].unique()
    )

    selected_discipline = st.sidebar.multiselect(
        "전공 선택", options=df['Discipline'].unique(),
        default=df['Discipline'].unique()
    )

    selected_task = st.sidebar.multiselect(
        "작업 유형 선택", options=df['TaskType'].unique(),
        default=df['TaskType'].unique()
    )

    df_filtered = df.query(
        "StudentLevel == @selected_level & Discipline == @selected_discipline & TaskType == @selected_task"
    )

    if df_filtered.empty:
        st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
    else:
        # =========================================================================
        # 📂 분석 탭 구성
        # =========================================================================
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 핵심 요약", "🕒 세션 길이 분석", "🎓 수준별 분석",
            "🧩 작업 유형 분석", "📊 상관관계 분석", "📋 원본 데이터"
        ])

        # --------------------------------------------
        # 📈 탭 1. 핵심 요약
        # --------------------------------------------
        with tab1:
            st.header("1. 핵심 요약 지표")
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            col1.metric("총 세션 수", f"{df_filtered.shape[0]:,}")
            col2.metric("평균 만족도", f"{df_filtered['SatisfactionRating'].mean():.2f} / 5")
            col3.metric("평균 세션 길이 (분)", f"{df_filtered['SessionLengthMin'].mean():.1f} 분")
            col4.metric("평균 프롬프트 수", f"{df_filtered['TotalPrompts'].mean():.1f} 개")
            col5.metric("재사용률", f"{(df_filtered['UsedAgain'].mean() * 100):.1f}%")
            col6.metric("평균 AI 도움 수준", f"{df_filtered['AI_AssistanceLevel'].mean():.2f}")

        # --------------------------------------------
        # 🕒 탭 2. 세션 길이 vs 만족도
        # --------------------------------------------
        with tab2:
            st.header("2. 세션 길이 vs 만족도")

            fig = px.scatter(
                df_filtered, x='SessionLengthMin', y='SatisfactionRating',
                color='StudentLevel', hover_data=['TaskType', 'TotalPrompts'],
                labels={'SessionLengthMin': '세션 길이 (분)', 'SatisfactionRating': '만족도'},
                title="AI 사용 시간과 만족도 관계"
            )
            # y축 자동 확대
            ymin, ymax = df_filtered['SatisfactionRating'].min(), df_filtered['SatisfactionRating'].max()
            fig.update_layout(yaxis_range=[max(1, ymin - 0.3), min(5, ymax + 0.3)])
            st.plotly_chart(fig, use_container_width=True)

        # --------------------------------------------
        # 🎓 탭 3. 수준별 분석
        # --------------------------------------------
        with tab3:
            st.header("3. 학생 수준(StudentLevel) vs 만족도")
            colA, colB = st.columns(2)

            with colA:
                avg_sat = df_filtered.groupby('StudentLevel')['SatisfactionRating'].mean().reset_index()
                fig_bar = px.bar(avg_sat, x='StudentLevel', y='SatisfactionRating',
                                 color='StudentLevel', title="학생 수준별 평균 만족도")
                ymin, ymax = avg_sat['SatisfactionRating'].min(), avg_sat['SatisfactionRating'].max()
                fig_bar.update_layout(yaxis_range=[max(1, ymin - 0.3), min(5, ymax + 0.3)])
                st.plotly_chart(fig_bar, use_container_width=True)

            with colB:
                fig_scatter = px.scatter(
                    df_filtered, x='SessionLengthMin', y='SatisfactionRating',
                    color='StudentLevel', title="수준별 세션 길이-만족도 분포"
                )
                ymin, ymax = df_filtered['SatisfactionRating'].min(), df_filtered['SatisfactionRating'].max()
                fig_scatter.update_layout(yaxis_range=[max(1, ymin - 0.3), min(5, ymax + 0.3)])
                st.plotly_chart(fig_scatter, use_container_width=True)

        # --------------------------------------------
        # 🧩 탭 4. 작업 유형 분석
        # --------------------------------------------
        with tab4:
            st.header("4. 작업 유형(TaskType) vs 만족도")
            colA, colB = st.columns(2)

            with colA:
                avg_task = df_filtered.groupby('TaskType')['SatisfactionRating'].mean().reset_index()
                fig_bar = px.bar(avg_task, x='TaskType', y='SatisfactionRating',
                                 color='TaskType', title="작업 유형별 평균 만족도")
                ymin, ymax = avg_task['SatisfactionRating'].min(), avg_task['SatisfactionRating'].max()
                fig_bar.update_layout(yaxis_range=[max(1, ymin - 0.3), min(5, ymax + 0.3)])
                st.plotly_chart(fig_bar, use_container_width=True)

            with colB:
                fig_scatter = px.scatter(
                    df_filtered, x='SessionLengthMin', y='SatisfactionRating',
                    color='TaskType', title="작업별 세션 길이-만족도 분포"
                )
                ymin, ymax = df_filtered['SatisfactionRating'].min(), df_filtered['SatisfactionRating'].max()
                fig_scatter.update_layout(yaxis_range=[max(1, ymin - 0.3), min(5, ymax + 0.3)])
                st.plotly_chart(fig_scatter, use_container_width=True)

        # --------------------------------------------
        # 📊 탭 5. 상관관계 분석
        # --------------------------------------------
        with tab5:
            st.header("5. 상관관계 분석")
            numeric_df = df_filtered[['SessionLengthMin', 'TotalPrompts', 'AI_AssistanceLevel', 'SatisfactionRating']]
            corr = numeric_df.corr()

            fig_corr = ff.create_annotated_heatmap(
                z=corr.values, x=list(corr.columns), y=list(corr.index),
                colorscale='Viridis', showscale=True
            )
            fig_corr.update_layout(title="수치형 변수 간 상관관계 Heatmap")
            st.plotly_chart(fig_corr, use_container_width=True)

            st.subheader("범주형 관계: 학생 수준 vs 작업 유형")
            contingency = pd.crosstab(df_filtered['StudentLevel'], df_filtered['TaskType'])
            st.dataframe(contingency)

            if contingency.min().min() > 0:
                chi2, p, _, _ = chi2_contingency(contingency)
                st.code(f"카이제곱 통계량: {chi2:.2f}, P-value: {p:.3f}")
                if p < 0.05:
                    st.success("✅ 유의미한 관계가 있음 (P < 0.05)")
                else:
                    st.warning("⚠️ 통계적으로 유의미하지 않음 (P ≥ 0.05)")

        # --------------------------------------------
        # 📋 탭 6. 원본 데이터
        # --------------------------------------------
        with tab6:
            st.header("6. 원본 데이터")
            if st.checkbox("전체 데이터 표시", key='show_data'):
                st.dataframe(df_filtered)
            else:
                st.dataframe(df_filtered.head(10))
else:
    st.warning("데이터 파일을 불러올 수 없습니다. 경로를 확인하세요.")
