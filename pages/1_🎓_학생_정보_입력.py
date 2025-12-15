# -*- coding: utf-8 -*-
"""
학생 정보 입력 페이지
"""

import streamlit as st
from utils.storage import save_user_data

st.set_page_config(page_title="학생 정보 입력", page_icon="🎓", layout="wide")

# ==== 🔵 저장된 데이터 불러오기 (추가된 유일한 핵심 기능) ====
stored = st.session_state.get("student_data", {})  # ⚡ 기존 저장된 값을 불러오는 핵심 코드

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
if 'student_id' not in st.session_state or st.session_state.student_id is None:
    st.error("⚠️ 로그인이 필요합니다. 메인 페이지에서 학생 이름을 입력해주세요.")
    st.stop()

# 사이드바에 로그아웃 버튼 추가
st.sidebar.markdown("---")
if st.sidebar.button("🚪 로그아웃", key="sidebar_logout", use_container_width=True):
    st.session_state.student_id = None
    st.session_state.student_data = None
    st.session_state.parent_data = None
    st.rerun()

st.title("🎓 학생 정보 입력")
st.markdown(f"**세션 ID:** {st.session_state.student_id}")
st.markdown("---")

# -------------------------------------------------------
# ⚠️ 선택박스 기본값 설정을 위한 헬퍼 함수 (오류 방지용)
# -------------------------------------------------------
def default_index(options, value, fallback_index=0):
    try:
        return options.index(value)
    except:
        return fallback_index


# 폼 시작
with st.form("student_form"):
    
    # ========== 1단계: 기본 정보 ==========
    st.subheader("📝 1단계: 기본 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        options = [1, 2, 3]
        학년 = st.selectbox(
            "학년 *",
            options,
            index=default_index(options, stored.get("학년", 2), 1),
            help="현재 본인의 학년을 선택해주세요."
        )
    
    with col2:
        options = ["내선전기공사", "변전설비공사", "외선전기공사", "전기공사관리", 
             "전기기기설계", "전기기기유지보수", "전기기기제작", "전기전선제조"]
        학생_희망직무 = st.selectbox(
            "희망 직무(NCS) *",
            options,
            index=default_index(options, stored.get("학생_희망직무", options[0])),
            help="앞으로 일하고 싶은 전기 분야 직무를 선택해주세요."
        )
    
    st.markdown("---")
    
    # ========== 2단계: 역량 평가 ==========
    st.subheader("📊 2단계: 역량 평가")
    
    # 직업기초능력평가
    st.markdown("**직업기초능력평가 등급**")
    col1, col2, col3, col4, col5 = st.columns(5)

    # 국어
    with col1:
        options = [1,2,3,4,5]
        학생_직기초_의사소통_국어 = st.selectbox(
            "의사소통(국어) *",
            options,
            index=default_index(options, stored.get("학생_직기초_의사소통_국어", 3), 2)
        )

    # 영어
    with col2:
        options = [1,2,3,4,5]
        학생_직기초_의사소통_영어 = st.selectbox(
            "의사소통(영어) *",
            options,
            index=default_index(options, stored.get("학생_직기초_의사소통_영어", 3), 2)
        )

    # 수리활용
    with col3:
        options = [1,2,3,4,5]
        학생_직기초_수리활용 = st.selectbox(
            "수리활용 *",
            options,
            index=default_index(options, stored.get("학생_직기초_수리활용", 3), 2)
        )

    # 문제해결
    with col4:
        options = [1,2,3,4,5]
        학생_직기초_문제해결 = st.selectbox(
            "문제해결 *",
            options,
            index=default_index(options, stored.get("학생_직기초_문제해결", 3), 2)
        )

    # 직무적응
    with col5:
        options = [1,2,3,4,5]
        학생_직기초_직무적응 = st.selectbox(
            "직무적응 *",
            options,
            index=default_index(options, stored.get("학생_직기초_직무적응", 3), 2)
        )
    
    # 교과 성취도
    st.markdown("**교과 성취도**")
    col1, col2, col3 = st.columns(3)

    with col1:
        options = ["A","B","C","D","E"]
        학생_전기교과성취도 = st.selectbox(
            "전기 교과 성취도 *",
            options,
            index=default_index(options, stored.get("학생_전기교과성취도", "B"), 1)
        )
    
    with col2:
        options = ["A","B","C","D","E"]
        학생_수학교과성취도 = st.selectbox(
            "수학 교과 성취도 *",
            options,
            index=default_index(options, stored.get("학생_수학교과성취도", "B"), 1)
        )
    
    with col3:
        options = ["A","B","C","D","E"]
        학생_NCS능력단위_수행평가 = st.selectbox(
            "NCS 능력단위 수행평가 *",
            options,
            index=default_index(options, stored.get("학생_NCS능력단위_수행평가", "B"), 1)
        )
    
    # 자격증
    st.markdown("**자격증**")
    col1, col2 = st.columns(2)

    with col1:
        options = ["유", "무"]
        학생_자격증_전기기능사 = st.selectbox(
            "전기기능사 *",
            options,
            index=default_index(options, stored.get("학생_자격증_전기기능사", "무"), 1)
        )
    
    with col2:
        options = ["유", "무"]
        학생_자격증_철도전기신호기능사 = st.selectbox(
            "철도전기신호기능사 *",
            options,
            index=default_index(options, stored.get("학생_자격증_철도전기신호기능사", "무"), 1)
        )
    
    st.markdown("---")
    
    # ========== 3단계: 직업 선호도 및 적합성 ==========
    st.subheader("💼 3단계: 직업 선호도 및 적합성")
    
    col1, col2 = st.columns(2)

    # ---- LEFT ----
    with col1:
        # 직업환경유형
        options = ["관료형","기업형","전문직형","창업형","학자형","해외형"]
        학생_직업환경유형 = st.selectbox(
            "직업 환경 유형 *",
            options,
            index=default_index(options, stored.get("학생_직업환경유형", options[0]))
        )
        
        # 산업선호도 1순위
        options = ["개인서비스","공공","교육","교통/물류","금융",
            "미디어/엔터테인먼트","보건/의료","산업기술/에너지공정",
            "전자/첨단기술","제조"]
        학생_산업선호도1순위 = st.selectbox(
            "산업선호도 1순위 *",
            options,
            index=default_index(options, stored.get("학생_산업선호도1순위", options[0]))
        )
        
        # 기업직무적합 1순위
        options = ["기획","마케팅","생산","연구개발","영업","인사","재무","홍보"]
        학생_기업직무적합1순위 = st.selectbox(
            "기업직무적합 1순위 *",
            options,
            index=default_index(options, stored.get("학생_기업직무적합1순위", options[0]))
        )

    # ---- RIGHT ----
    with col2:
        # 흥미 일관성 등급
        options = ["A","B","C","D","E"]
        학생_흥미일관성등급 = st.selectbox(
            "흥미 일관성 등급 *",
            options,
            index=default_index(options, stored.get("학생_흥미일관성등급", "C"), 2)
        )
        
        # 산업선호도 2순위
        options = ["개인서비스","공공","교육","교통/물류","금융",
            "미디어/엔터테인먼트","보건/의료","산업기술/에너지공정",
            "전자/첨단기술","제조"]
        학생_산업선호도2순위 = st.selectbox(
            "산업선호도 2순위 *",
            options,
            index=default_index(options, stored.get("학생_산업선호도2순위", options[0]))
        )
        
        # 기업직무적합 2순위
        options = ["기획","마케팅","생산","연구개발","영업","인사","재무","홍보"]
        학생_기업직무적합2순위 = st.selectbox(
            "기업직무적합 2순위 *",
            options,
            index=default_index(options, stored.get("학생_기업직무적합2순위", options[1]), 1)
        )
    
    # 근무 환경 선호
    st.markdown("**근무 환경 선호**")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        options = ["실내","실외","상관없음"]
        학생_근무환경선호_실내실외 = st.selectbox(
            "실내·실외 선호 *",
            options,
            index=default_index(options, stored.get("학생_근무환경선호_실내실외", "상관없음"), 2)
        )
    
    with col2:
        options = ["가능","불가"]
        학생_근무환경선호_교대근무 = st.selectbox(
            "교대근무 *",
            options,
            index=default_index(options, stored.get("학생_근무환경선호_교대근무", "불가"))
        )
    
    with col3:
        options = ["가능","불가"]
        학생_근무환경선호_야간근무 = st.selectbox(
            "야간근무 *",
            options,
            index=default_index(options, stored.get("학생_근무환경선호_야간근무", "불가"))
        )
    
    with col4:
        options = ["가능","불가"]
        학생_근무환경선호_고소작업 = st.selectbox(
            "고소작업 *",
            options,
            index=default_index(options, stored.get("학생_근무환경선호_고소작업", "불가"))
        )
    
    with col5:
        options = ["상관없음","팀 작업 선호","혼자 작업 선호"]
        학생_근무환경선호_팀작업 = st.selectbox(
            "팀작업 선호 *",
            options,
            index=default_index(options, stored.get("학생_근무환경선호_팀작업", "상관없음"))
        )
    
    st.markdown("---")
    
    # ========== 4단계: 자기인식 및 진로 관련 태도 ==========
    st.subheader("🧠 4단계: 자기인식 및 진로 관련 태도")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        options = ["매우 낮음","낮음","보통","높음","매우 높음"]
        학생_자기강점인식 = st.selectbox(
            "자기 강점 인식 *",
            options,
            index=default_index(options, stored.get("학생_자기강점인식", "보통"), 2)
        )
        
        학생_진로결정자기효능감 = st.selectbox(
            "진로결정 자기효능감 *",
            options,
            index=default_index(options, stored.get("학생_진로결정자기효능감", "보통"), 2)
        )
        
        학생_부모지지인식 = st.selectbox(
            "부모 지지 인식 *",
            options,
            index=default_index(options, stored.get("학생_부모지지인식", "보통"), 2)
        )
    
    with col2:
        options = ["매우 낮음","낮음","보통","높음","매우 높음"]
        학생_학습태도자기평가 = st.selectbox(
            "학습태도 자기평가 *",
            options,
            index=default_index(options, stored.get("학생_학습태도자기평가", "보통"), 2)
        )
        
        학생_진로변화의향 = st.selectbox(
            "진로 변화 의향 *",
            options,
            index=default_index(options, stored.get("학생_진로변화의향", "보통"), 2)
        )
        
        학생_부모압력인식 = st.selectbox(
            "부모 압력 인식 *",
            options,
            index=default_index(options, stored.get("학생_부모압력인식", "보통"), 2)
        )
    
    with col3:
        options = ["매우 낮음","낮음","보통","높음","매우 높음"]
        학생_희망직무전망인식 = st.selectbox(
            "희망직무 전망 인식 *",
            options,
            index=default_index(options, stored.get("학생_희망직무전망인식", "보통"), 2)
        )
        
        options = ["매우 불만족","불만족","보통","만족","매우 만족"]
        학생_진로대화만족도 = st.selectbox(
            "진로 대화 만족도 *",
            options,
            index=default_index(options, stored.get("학생_진로대화만족도", "보통"), 2)
        )
    
    # 자기강점유형 및 희망직무일치수준
    col1, col2 = st.columns(2)
    
    with col1:
        options = ["책임감", "문제해결력", "집중력", "손재능", "의사소통", "협업능력", "리더십", "창의성", "기타"]
        학생_자기강점유형 = st.selectbox(
            "자기 강점 유형 *",
            options,
            index=default_index(options, stored.get("학생_자기강점유형", options[0]))
        )
    
    with col2:
        options = ["거의 동일", "부분 유사", "완전 다름"]
        학생_희망직무일치수준 = st.selectbox(
            "희망직무 일치 수준 *",
            options,
            index=default_index(options, stored.get("학생_희망직무일치수준", "부분 유사"), 1)
        )
    
    # 제출 버튼
    st.markdown("---")
    submitted = st.form_submit_button("💾 학생 정보 저장하기", use_container_width=True)
    
    if submitted:
        # 데이터 저장
        student_data = {
            "student_name": st.session_state.student_id,
            "학년": 학년,
            "학생_희망직무": 학생_희망직무,
            "학생_직기초_의사소통_국어": 학생_직기초_의사소통_국어,
            "학생_직기초_의사소통_영어": 학생_직기초_의사소통_영어,
            "학생_직기초_수리활용": 학생_직기초_수리활용,
            "학생_직기초_문제해결": 학생_직기초_문제해결,
            "학생_직기초_직무적응": 학생_직기초_직무적응,
            "학생_전기교과성취도": 학생_전기교과성취도,
            "학생_수학교과성취도": 학생_수학교과성취도,
            "학생_NCS능력단위_수행평가": 학생_NCS능력단위_수행평가,
            "학생_자격증_전기기능사": 학생_자격증_전기기능사,
            "학생_자격증_철도전기신호기능사": 학생_자격증_철도전기신호기능사,
            "학생_직업환경유형": 학생_직업환경유형,
            "학생_산업선호도1순위": 학생_산업선호도1순위,
            "학생_산업선호도2순위": 학생_산업선호도2순위,
            "학생_흥미일관성등급": 학생_흥미일관성등급,
            "학생_기업직무적합1순위": 학생_기업직무적합1순위,
            "학생_기업직무적합2순위": 학생_기업직무적합2순위,
            "학생_근무환경선호_실내실외": 학생_근무환경선호_실내실외,
            "학생_근무환경선호_교대근무": 학생_근무환경선호_교대근무,
            "학생_근무환경선호_야간근무": 학생_근무환경선호_야간근무,
            "학생_근무환경선호_고소작업": 학생_근무환경선호_고소작업,
            "학생_근무환경선호_팀작업": 학생_근무환경선호_팀작업,
            "학생_자기강점인식": 학생_자기강점인식,
            "학생_학습태도자기평가": 학생_학습태도자기평가,
            "학생_희망직무전망인식": 학생_희망직무전망인식,
            "학생_진로결정자기효능감": 학생_진로결정자기효능감,
            "학생_진로변화의향": 학생_진로변화의향,
            "학생_부모지지인식": 학생_부모지지인식,
            "학생_부모압력인식": 학생_부모압력인식,
            "학생_진로대화만족도": 학생_진로대화만족도,
            "학생_자기강점유형": 학생_자기강점유형,
            "학생_희망직무일치수준": 학생_희망직무일치수준
        }
        
        st.session_state.student_data = student_data
        save_user_data(st.session_state.student_id, student_data=student_data)

        st.success("✅ 학생 정보가 저장되었습니다!")
        st.info("👈 사이드바에서 **📊 진행 현황**을 확인하거나, **👨‍👩‍👧 부모 정보 입력**으로 이동하세요.")
