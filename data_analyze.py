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
# 🔵 영어 → 한국어 매핑 + 질문 설명문 추가
# ----------------------------------------------------
QUESTION_INFO = {
    "What is your level of familiarity with AI?": {
        "ko": "AI에 대한 친숙도는 어느 정도인가",
        "desc": "응답자가 AI 기술에 대해 기본적으로 얼마나 알고 있는지를 묻는 질문입니다."
    },
    "Do you use any AI-powered devices or applications daily?": {
        "ko": "일상에서 AI 기반 기기나 앱을 사용하는가",
        "desc": "AI가 적용된 서비스나 기기를 일상적으로 사용하는지 조사하는 문항입니다."
    },
    "How much do you trust AI to make decisions in your daily life?": {
        "ko": "일상 속 AI의 의사결정을 얼마나 신뢰하는가",
        "desc": "AI의 판단을 믿고 맡길 수 있는지에 대한 신뢰도를 측정하는 질문입니다."
    },
    "Do you think AI enhances your productivity in daily tasks?": {
        "ko": "AI가 생산성을 향상시킨다고 생각하는가",
        "desc": "AI가 실제로 생활 속 효율성이나 업무 능률을 높여주는지에 대한 인식 조사입니다."
    },
    "In which areas do you think AI will have the biggest impact in the future?": {
        "ko": "미래에 AI가 가장 큰 영향을 미칠 분야는 무엇이라고 생각하는가",
        "desc": "응답자가 예상하는 AI의 미래 영향력 분야를 파악하는 문항입니다."
    },
    "What benefits do you foresee with the advancement of AI?": {
        "ko": "AI 발전이 가져올 이점은 무엇이라고 생각하는가",
        "desc": "AI 기술이 미래에 제공할 긍정적 효과나 혜택을 조사하는 질문입니다."
    },
    "Should there be regulations on the development and use of AI?": {
        "ko": "AI 개발 및 사용에 대한 규제가 필요하다고 생각하는가",
        "desc": "AI 기술의 규제 필요성에 대해 얼마나 공감하는지를 묻는 문항입니다."
    },
    "Do you think AI will improve or worsen human society in the long run?": {
        "ko": "AI가 장기적으로 인간 사회를 개선하거나 악화시킬 수 있다는 의견",
        "desc": "AI의 장기적 영향에 대한 낙관적/비관적 관점을 조사하는 질문입니다."
    },
    "What is your overall opinion on AI?": {
        "ko": "AI에 대한 전반적인 의견은 무엇인가",
        "desc": "AI 기술에 대한 전반적 인식을 파악하는 문항입니다."
    },
    "Would you be interested in learning more about AI and its applications in the future?": {
        "ko": "AI 및 활용 분야를 더 배우고 싶은가",
        "desc": "향후 AI 학습 의향 및 관심도를 파악하는 질문입니다."
    },

    # Count 기반 질문 4개
    "In what areas do you use AI on a daily basis?": {
        "ko": "일상에서 어떤 분야에 AI를 사용하는가",
        "desc": "일상생활에서 AI를 활용하는 구체적인 분야(교육, 엔터테인먼트 등)를 확인하는 문항입니다."
    },
    "How much do you trust AI to make decisions in your daily life?": {
        "ko": "일상 속 AI 의사결정을 얼마나 신뢰하는가",
        "desc": "AI 판단에 대한 신뢰 수준을 측정하는 질문입니다."
    },
    "Do you believe AI will play a significant role in shaping the future?": {
        "ko": "AI가 미래 사회 형성에 중요한 역할을 한다고 생각하는가",
        "desc": "AI가 미래 변화에 미칠 영향력에 대한 관점을 조사하는 문항입니다."
    },
    "What concerns do you have regarding AI in the future?": {
        "ko": "미래 AI에 대해 어떤 우려를 가지고 있는가",
        "desc": "AI 발전에 따른 위험, 걱정, 부정적 요소를 확인하는 질문입니다."
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

    # 자동 설명 출력
    st.info(f"📘 질문 설명: {QUESTION_INFO[target_col]['desc']}")

    # 학생 직접 입력 영역
    st.write("✏️ **해석(학생 작성 영역)**")
    st.text_area("문항 해석을 직접 입력하세요:", key="rate_comment")

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

    # 자동 설명 출력
    st.info(f"📘 질문 설명: {QUESTION_INFO[target_col]['desc']}")

    st.write("✏️ **해석(학생 작성 영역)**")
    st.text_area("문항 해석을 직접 입력하세요:", key="count_comment")

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
