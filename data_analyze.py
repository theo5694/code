import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Age-Based Analysis Dashboard", layout="wide")
st.title("📊 Age Group 기반 자동 분석 대시보드 (한국어 UI 완성본)")

@st.cache_data
def load_data():
    return pd.read_csv("DATASET.csv")

df = load_data()

AGE_COL = "What is your age group?"

if AGE_COL not in df.columns:
    st.error(f"❌ 데이터셋에 '{AGE_COL}' 컬럼이 없습니다.")
    st.stop()

# -----------------------------------
# 🔵 영어 → 한국어 매핑
# -----------------------------------
EN_KR_MAP = {
    # 비율 기반 10문항
    "What is your level of familiarity with AI?": "AI에 대한 친숙도는 어느 정도인가",
    "Do you use any AI-powered devices or applications daily?": "일상에서 AI 기반 기기나 앱을 사용하는가",
    "How much do you trust AI to make decisions in your daily life?": "일상 속 AI의 의사결정을 얼마나 신뢰하는가",
    "Do you think AI enhances your productivity in daily tasks?": "AI가 생산성을 향상시킨다고 생각하는가",
    "In which areas do you think AI will have the biggest impact in the future?": "미래에 AI가 가장 큰 영향을 미칠 분야는 무엇이라고 생각하는가",
    "What benefits do you foresee with the advancement of AI?": "AI 발전이 가져올 이점은 무엇이라고 생각하는가",
    "Should there be regulations on the development and use of AI?": "AI 개발 및 사용에 대한 규제가 필요하다고 생각하는가",
    "Do you think AI will improve or worsen human society in the long run?": "AI가 장기적으로 인간 사회를 개선하거나 악화시킬 수 있다는 의견",
    "What is your overall opinion on AI?": "AI에 대한 전반적인 의견은 무엇인가",
    "Would you be interested in learning more about AI and its applications in the future?": "AI 및 활용 분야를 더 배우고 싶은가",

    # 개수 기반 4문항
    "In what areas do you use AI on a daily basis?": "일상에서 어떤 분야에 AI를 사용하는가",
    "How much do you trust AI to make decisions in your daily life?": "일상 속 AI 의사결정을 얼마나 신뢰하는가",
    "Do you believe AI will play a significant role in shaping the future?": "AI가 미래 사회 형성에 중요한 역할을 한다고 생각하는가",
    "What concerns do you have regarding AI in the future?": "미래 AI에 대해 어떤 우려를 가지고 있는가"
}

KR_EN_MAP = {v: k for k, v in EN_KR_MAP.items()}

RATE_COLUMNS = list(EN_KR_MAP.keys())[:10]
COUNT_COLUMNS = list(EN_KR_MAP.keys())[10:]

RATE_COLUMNS_KR = [EN_KR_MAP[q] for q in RATE_COLUMNS]
COUNT_COLUMNS_KR = [EN_KR_MAP[q] for q in COUNT_COLUMNS]

tab1, tab2, tab3 = st.tabs(["👥 나이 분포", "📊 비율(%) 비교", "📘 개수 비교"])

# -----------------------------
#  탭 1 — 나이 분포
# -----------------------------
with tab1:
    st.subheader("👥 Age Group Distribution (나이 분포)")
    fig_age = px.histogram(df, x=AGE_COL, title="나이 그룹 분포")
    st.plotly_chart(fig_age, use_container_width=True)


# -----------------------------
#  탭 2 — 비율(%) 비교
# -----------------------------
with tab2:
    st.subheader("📊 문항 선택 (비율 기반 / 한국어 선택)")

    kr_choice = st.selectbox("비율로 분석할 문항 선택", RATE_COLUMNS_KR)
    target_col = KR_EN_MAP[kr_choice]

    # 🔶 학생이 직접 해석을 적는 칸
    st.write("✏️ **해석(학생 작성 영역)**")
    st.text_area("문항 해석을 직접 입력하세요:", placeholder="예: 이 질문은 사람들이 AI에 얼마나 익숙한지를 묻고 있다.", key="rate_comment")

    cat_df = df.groupby([AGE_COL, target_col]).size().reset_index(name="count")
    total = cat_df.groupby(AGE_COL)["count"].transform("sum")
    cat_df["percentage"] = cat_df["count"] / total * 100

    fig = px.bar(
        cat_df,
        x=AGE_COL,
        y="percentage",
        color=target_col,
        title=f"연령대별 {kr_choice} (비율 비교)",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("📘 응답 분포")
    st.table(df[target_col].value_counts())


# -----------------------------
#  탭 3 — 개수(count) 비교
# -----------------------------
with tab3:
    st.subheader("📘 문항 선택 (개수 기반 / 한국어 선택)")

    kr_choice = st.selectbox("개수로 분석할 문항 선택", COUNT_COLUMNS_KR)
    target_col = KR_EN_MAP[kr_choice]

    # 🔶 학생이 직접 해석을 적는 칸
    st.write("✏️ **해석(학생 작성 영역)**")
    st.text_area("문항 해석을 직접 입력하세요:", placeholder="예: 이 질문은 사람들이 어떤 분야에서 AI를 사용하는지를 묻고 있다.", key="count_comment")

    count_df = df.groupby([AGE_COL, target_col]).size().reset_index(name="count")

    fig = px.bar(
        count_df,
        x=AGE_COL,
        y="count",
        color=target_col,
        barmode="group",
        title=f"연령대별 {kr_choice} (개수 비교)",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("📘 응답 분포표")
    st.table(df[target_col].value_counts())
