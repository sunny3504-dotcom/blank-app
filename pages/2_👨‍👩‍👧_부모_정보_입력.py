# -*- coding: utf-8 -*-
"""
부모 정보 입력 페이지
"""

import streamlit as st
from utils.storage import save_user_data

st.set_page_config(page_title="부모 정보 입력", page_icon="👨‍👩‍👧", layout="wide")

# ==== 🔵 저장된 데이터 불러오기 (추가된 핵심 기능) ====
stored = st.session_state.get("parent_data", {})  # 기존 저장된 부모 정보 불러오기

# ==== 🔧 안전한 기본값 인덱스 계산 함수 ====
def default_index(options, value, fallback_index=0):
    try:
        return options.index(value)
    except:
        return fallback_index


# 사이드바 "홈" 스타일 (연한 회색, 강조 없음)
st.markdown("""
<style>
    /* 사이드바 첫 번째 항목을 "홈"으로 변경 */
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] {
        padding-top: 0.5rem;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] li:first-child {
        background: none !important;
        padding: 0 !important;
        margin-bottom: 0.5rem;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] li:first-child a {
        background: #f0f2f6 !important;
        color: #555 !important;
        border-radius: 0.3rem;
        padding: 0.5rem 0.8rem !important;
        display: block;
        text-align: center;
        font-size: 0.9rem !important;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] li:first-child a:hover {
        background: #e8eaf0 !important;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] li:first-child a span {
        font-size: 0 !important;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] li:first-child a span::before {
        content: "🏠 홈";
        font-size: 0.9rem !important;
        font-weight: 500;
        color: #555;
    }
</style>
""", unsafe_allow_html=True)


# 로그인 확인
if "student_id" not in st.session_state or st.session_state.student_id is None:
    st.error("⚠️ 로그인이 필요합니다. 메인 페이지에서 학생 이름을 입력해주세요.")
    st.stop()

# 로그아웃 버튼
st.sidebar.markdown("---")
if st.sidebar.button("🚪 로그아웃", key="sidebar_logout", use_container_width=True):
    st.session_state.student_id = None
    st.session_state.student_data = None
    st.session_state.parent_data = None
    st.rerun()

st.title("👨‍👩‍👧 부모 정보 입력")
st.markdown(f"**세션 ID:** {st.session_state.student_id}")
st.markdown("자녀의 진로 설계를 위한 부모님의 의견을 입력해주세요.")
st.markdown("---")


# -------------------------------------------------------
# 폼 시작
# -------------------------------------------------------
with st.form("parent_form"):

    # ========== 1. 부모의 희망 및 지지 ==========
    st.subheader("💼 부모의 희망 및 지지")

    col1, col2 = st.columns(2)

    with col1:
        options = ["내선전기공사", "변전설비공사", "외선전기공사", "전기공사관리",
                   "전기기기설계", "전기기기유지보수", "전기기기제작", "전기전선제조"]
        부모_희망직무 = st.selectbox(
            "희망 직무 *",
            options,
            index=default_index(options, stored.get("부모_희망직무", options[0]))
        )

        options = ["매우 낮음", "낮음", "보통", "높음", "매우 높음"]
        부모_지지수준 = st.selectbox(
            "진로 지지 수준 *",
            options,
            index=default_index(options, stored.get("부모_지지수준", "보통"), 2)
        )

    with col2:
        options = ["매우 낮음", "낮음", "보통", "높음", "매우 높음"]
        부모_압력수준 = st.selectbox(
            "압력 수준 *",
            options,
            index=default_index(options, stored.get("부모_압력수준", "보통"), 2)
        )

    st.markdown("---")

    # ========== 2. 자녀에 대한 인식 ==========
    st.subheader("👦 자녀에 대한 인식")

    col1, col2 = st.columns(2)

    with col1:
        options = ["매우 낮음", "낮음", "보통", "높음", "매우 높음"]
        부모_자녀강점인식 = st.selectbox(
            "자녀 강점 인식 *",
            options,
            index=default_index(options, stored.get("부모_자녀강점인식", "보통"), 2)
        )

        부모_자녀학습태도인식 = st.selectbox(
            "자녀 학습태도 인식 *",
            options,
            index=default_index(options, stored.get("부모_자녀학습태도인식", "보통"), 2)
        )

        부모_미래직업전망인식 = st.selectbox(
            "미래 직업 전망 인식 *",
            options,
            index=default_index(options, stored.get("부모_미래직업전망인식", "보통"), 2)
        )

    with col2:
        options = ["매우 낮음", "낮음", "보통", "높음", "매우 높음"]
        부모_자녀진로변화허용도 = st.selectbox(
            "자녀 진로 변화 허용도 *",
            options,
            index=default_index(options, stored.get("부모_자녀진로변화허용도", "보통"), 2)
        )

        options = ["거의 하지 않는다", "가끔 한다", "보통이다", "자주 한다", "매우 자주 한다"]
        부모_진로대화빈도 = st.selectbox(
            "진로 대화 빈도 *",
            options,
            index=default_index(options, stored.get("부모_진로대화빈도", "보통이다"), 2)
        )

    st.markdown("---")

    # ========== 3. 부모 본인의 직업 ==========
    st.subheader("👔 부모 본인의 직업")

    col1, col2 = st.columns(2)

    with col1:
        options = ["전문직(의료/법률/기술/연구)", "사무직(행정·경영)", "교육직",
                   "서비스직", "영업/판매", "생산/기술직", "공공/공무원",
                   "자영업", "운전/운송직", "군/경찰/소방", "IT/기술직", "기타"]
        부모_현재직무 = st.selectbox(
            "부모 현재 직무 *",
            options,
            index=default_index(options, stored.get("부모_현재직무", options[0]))
        )

    with col2:
        options = ["매우 불만족", "불만족", "보통", "만족", "매우 만족"]
        부모_직무만족도 = st.selectbox(
            "직무 만족도 *",
            options,
            index=default_index(options, stored.get("부모_직무만족도", "보통"), 2)
        )

    st.markdown("---")

    # ========== 4. 자녀 강점 및 직무 일치도 ==========
    st.subheader("💡 자녀 강점 및 직무 일치도")

    col1, col2 = st.columns(2)

    with col1:
        options = ["책임감", "문제해결력", "집중력", "손재능", "의사소통",
                   "협업능력", "리더십", "창의성", "기타"]
        부모_자녀강점유형 = st.selectbox(
            "자녀 강점 유형 *",
            options,
            index=default_index(options, stored.get("부모_자녀강점유형", options[0]))
        )

    with col2:
        options = ["거의 동일", "부분 유사", "완전 다름"]
        부모_희망직무일치수준 = st.selectbox(
            "희망직무 일치 수준 *",
            options,
            index=default_index(options, stored.get("부모_희망직무일치수준", "부분 유사"), 1)
        )

    # 제출 버튼
    st.markdown("---")
    submitted = st.form_submit_button("💾 부모 정보 저장하기", use_container_width=True)

    if submitted:
        parent_data = {
            "부모_희망직무": 부모_희망직무,
            "부모_지지수준": 부모_지지수준,
            "부모_압력수준": 부모_압력수준,
            "부모_자녀강점인식": 부모_자녀강점인식,
            "부모_자녀학습태도인식": 부모_자녀학습태도인식,
            "부모_미래직업전망인식": 부모_미래직업전망인식,
            "부모_자녀진로변화허용도": 부모_자녀진로변화허용도,
            "부모_진로대화빈도": 부모_진로대화빈도,
            "부모_현재직무": 부모_현재직무,
            "부모_직무만족도": 부모_직무만족도,
            "부모_자녀강점유형": 부모_자녀강점유형,
            "부모_희망직무일치수준": 부모_희망직무일치수준
        }

        st.session_state.parent_data = parent_data
        save_user_data(st.session_state.student_id, parent_data=parent_data)

        st.success("✅ 부모 정보가 저장되었습니다!")
        st.info("👈 사이드바에서 **📊 진행 현황**을 확인하세요.")
