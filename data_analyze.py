import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Age-Based Analysis Dashboard", layout="wide")
st.title("📊 Age Group 기반 자동 분석 대시보드 (한국어 UI + 질문 설명 포함)")

@st.cache_data
def load_data():
    return pd.read_csv("DATASET.csv")

df = load_data()

AGE_COL = "What is your age group?"

if AGE_COL not in df.columns:
    st.error(f"❌ 데이터셋에 '{AGE_COL}' 컬럼이 없습니다.")
    st.stop()

# ----------------------------------------------------
# 🔵 질문 한국어 + 설명문 (자동 해석)
# ----------------------------------------------------
QUESTION_INFO = {
    "What is your level of familiarity with AI?": {
        "ko": "AI에 대한 친숙도는 어느 정도인가",
        "desc": "연령이 높을수록 인공지능에 익숙하지 않은 경행을 보인다."
    },
    "Do you use any AI-powered devices or applications daily?": {
        "ko": "일상에서 AI 기반 기기나 앱을 사용하는가",
        "desc": "주로 모든 연령에서 절반정도의 인원이 인공지능을 활용한다."
    },
    "How much do you trust AI to make decisions in your daily life?": {
        "ko": "일상 속 AI 의사결정을 얼마나 신뢰하는가",
        "desc": "미성년자와 35~44세 사이를 제외하면 대부분 ."
    },
    "Do you think AI enhances your productivity in daily tasks?": {
        "ko": "AI가 생산성을 향상시킨다고 생각하는가",
        "desc": "AI가 실제로 효율성과 생산성을 높여주는지에 대한 인식 조사입니다."
    },
    "In which areas do you think AI will have the biggest impact in the future?": {
        "ko": "미래에 AI가 가장 큰 영향을 미칠 분야는 무엇이라고 생각하는가",
        "desc": "응답자가 예상하는 AI의 미래 영향력 분야를 파악합니다."
    },
    "What benefits do you foresee with the advancement of AI?": {
        "ko": "AI 발전이 가져올 이점은 무엇이라고 생각하는가",
        "desc": "AI 기술의 발전으로 기대되는 긍정적 효과를 묻습니다."
    },
    "Should there be regulations on the development and use of AI?": {
        "ko": "AI 개발 및 사용에 대한 규제가 필요하다고 생각하는가",
        "desc": "AI 기술에 대한 규제 필요성을 평가하는 문항입니다."
    },
    "Do you think AI will improve or worsen human society in the long run?": {
        "ko": "AI가 장기적으로 인간 사회에 미치는 영향은 긍정적인가 부정적인가",
        "desc": "AI의 장기적 사회적 영향에 대한 인식을 조사합니다."
    },
    "What is your overall opinion on AI?": {
        "ko": "AI에 대한 전반적인 의견은 무엇인가",
        "desc": "응답자의 AI에 대한 전체적인 태도를 확인하는 질문입니다."
    },
    "Would you be interested in learning more about AI and its applications in the future?": {
        "ko": "AI 및 활용 분야를 더 배우고 싶은가",
        "desc": "향후 AI 관련 학습 의향을 묻습니다."
    },

    # Count 기반 질문
    "In what areas do you use AI on a daily basis?": {
        "ko": "일상에서 어떤 분야에 AI를 사용하는가",
        "desc": "일상생활 중 AI를 사용하는 구체적인 분야를 조사합니다."
    },
    "How much do you trust AI to make decisions in your daily life?": {
        "ko": "일상 속 AI 의사결정을 얼마나 신뢰하는가",
        "desc": "AI 판단에 대한 신뢰 수준을 묻습니다."
    },
    "Do you believe AI will play a significant role in shaping the future?": {
        "ko": "AI가 미래 사회 형성에 중요한 역할을 한다고 생각하는가",
        "desc": "미래 변화에서 AI의 영향력을 평가합니다."
    },
    "What concerns do you have regarding AI in the future?": {
        "ko": "미래 AI에 대해 어떤 우려를 가지고 있는가",
        "desc": "AI 발전에 따른 걱정·부정적 요소를 조사합니다."
    }
}

# 영어→한국어 변환 테이블
EN_KR_MAP = {k: v["ko"] for k, v in QUESTION_INFO.items()}
KR_EN_MAP = {v["ko"]: k for k, v in QUESTION_INFO.items()}

RATE_COLUMNS = list(EN_KR_MAP.keys())[:10]
COUNT_COLUMNS = list(EN_KR_MAP.keys())[10:]

RATE_COLUMNS_KR = [EN_KR_MAP[q] for q in RATE_COLUMNS]
COUNT_COLUMNS_KR = [EN_KR_MAP[q] for q in COUNT_COLUMNS]

# -----------------------------
# 탭 구성
# -----------------------------
tab1, tab2, tab3 = st.tabs(["👥 나이 분포", "📊 비율(%) 비교", "📘 개수 비교"])

# -----------------------------
# TAB 1 — 나이 분포
# -----------------------------
with tab1:
    st.subheader("👥 Age Group Distribution (나이 분포)")
    fig_age = px.histogram(df, x=AGE_COL, title="나이 그룹 분포")
    st.plotly_chart(fig_age, use_container_width=True)

# -----------------------------
# TAB 2 — 비율 비교
# -----------------------------
with tab2:
    st.subheader("📊 문항 선택 (비율 기반 / 한국어 선택)")

    kr_choice = st.selectbox("비율로 분석할 문항 선택", RATE_COLUMNS_KR)
    target_col = KR_EN_MAP[kr_choice]

    # 자동 설명 (해석)
    st.info(f"📘 **질문 해석**: {QUESTION_INFO[target_col]['desc']}")

    # 데이터 처리
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
# TAB 3 — 개수 비교
# -----------------------------
with tab3:
    st.subheader("📘 문항 선택 (개수 기반 / 한국어 선택)")

    kr_choice = st.selectbox("개수로 분석할 문항 선택", COUNT_COLUMNS_KR)
    target_col = KR_EN_MAP[kr_choice]

    # 자동 설명
    st.info(f"📘 **질문 해석**: {QUESTION_INFO[target_col]['desc']}")

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
