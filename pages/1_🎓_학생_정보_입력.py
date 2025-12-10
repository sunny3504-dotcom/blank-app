# -*- coding: utf-8 -*-
"""
학생 정보 입력 페이지
"""

import streamlit as st
from utils.storage import save_user_data

st.set_page_config(page_title="학생 정보 입력", page_icon="🎓", layout="wide")

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

# 폼 시작
with st.form("student_form"):
    
    # ========== 1단계: 기본 정보 ==========
    st.subheader("📝 1단계: 기본 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        학년 = st.selectbox(
            "학년 *", 
            [1, 2, 3], 
            index=1,
            help="현재 본인의 학년을 선택해주세요."
        )
    
    with col2:
        학생_희망직무 = st.selectbox(
            "희망 직무(NCS) *",
            ["내선전기공사", "변전설비공사", "외선전기공사", "전기공사관리", 
             "전기기기설계", "전기기기유지보수", "전기기기제작", "전기전선제조"],
            help="앞으로 일하고 싶은 전기 분야 직무를 선택해주세요."
        )
    
    st.markdown("---")
    
    # ========== 2단계: 역량 평가 ==========
    st.subheader("📊 2단계: 역량 평가")
    
    # 직업기초능력평가
    st.markdown("**직업기초능력평가 등급**")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        학생_직기초_의사소통_국어 = st.selectbox(
            "의사소통(국어) *", 
            [1, 2, 3, 4, 5],
            index=2,
            help="직업기초능력 평가의 의사소통(국어) 영역 등급을 선택해주세요."
        )
    
    with col2:
        학생_직기초_의사소통_영어 = st.selectbox(
            "의사소통(영어) *", 
            [1, 2, 3, 4, 5],
            index=2,
            help="직업기초능력 평가의 의사소통(영어) 영역 등급을 선택해주세요."
        )
    
    with col3:
        학생_직기초_수리활용 = st.selectbox(
            "수리활용 *", 
            [1, 2, 3, 4, 5],
            index=2,
            help="직업기초능력 평가의 수리활용 영역 등급을 선택해주세요."
        )
    
    with col4:
        학생_직기초_문제해결 = st.selectbox(
            "문제해결 *", 
            [1, 2, 3, 4, 5],
            index=2,
            help="직업기초능력 평가의 문제해결 영역 등급을 선택해주세요."
        )
    
    with col5:
        학생_직기초_직무적응 = st.selectbox(
            "직무적응 *", 
            [1, 2, 3, 4, 5],
            index=2,
            help="직무 적응 능력 평가 등급을 선택해주세요."
        )
    
    # 교과 성취도
    st.markdown("**교과 성취도**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        학생_전기교과성취도 = st.selectbox(
            "전기 교과 성취도 *",
            ["A", "B", "C", "D", "E"],
            index=1,
            help="최근 성취도 평가에서 받은 전기 교과 등급을 선택해주세요."
        )
    
    with col2:
        학생_수학교과성취도 = st.selectbox(
            "수학 교과 성취도 *",
            ["A", "B", "C", "D", "E"],
            index=1,
            help="최근 성취도 평가에서 받은 수학 교과 등급을 선택해주세요."
        )
    
    with col3:
        학생_NCS능력단위_수행평가 = st.selectbox(
            "NCS 능력단위 수행평가 *",
            ["A", "B", "C", "D", "E"],
            index=1,
            help="NCS 능력단위 평가에서 받은 등급을 선택해주세요."
        )
    
    # 자격증
    st.markdown("**자격증**")
    col1, col2 = st.columns(2)
    
    with col1:
        학생_자격증_전기기능사 = st.selectbox(
            "전기기능사 *",
            ["유", "무"],
            index=1,
            help="전기기능사 자격증 취득 여부를 선택해주세요."
        )
    
    with col2:
        학생_자격증_철도전기신호기능사 = st.selectbox(
            "철도전기신호기능사 *",
            ["유", "무"],
            index=1,
            help="철도전기신호기능사 자격증 취득 여부를 선택해주세요."
        )
    
    st.markdown("---")
    
    # ========== 3단계: 직업 선호도 및 적합성 ==========
    st.subheader("💼 3단계: 직업 선호도 및 적합성")
    
    col1, col2 = st.columns(2)
    
    with col1:
        학생_직업환경유형 = st.selectbox(
            "직업 환경 유형 *",
            ["관료형", "기업형", "전문직형", "창업형", "학자형", "해외형"],
            help="본인의 성향과 잘 맞는 직업 환경 유형을 선택해주세요."
        )
        
        학생_산업선호도1순위 = st.selectbox(
            "산업선호도 1순위 *",
            ["개인서비스", "공공", "교육", "교통/물류", "금융", 
             "미디어/엔터테인먼트", "보건/의료", "산업기술/에너지공정", 
             "전자/첨단기술", "제조"],
            help="가장 관심있는 산업 분야를 선택해주세요."
        )
        
        학생_흥미일관성등급 = st.selectbox(
            "흥미 일관성 등급 *",
            ["A", "B", "C", "D", "E"],
            index=2,
            help="여러 진로검사나 경험에서 흥미가 일관되게 나타났는지 선택해주세요."
        )
        
        학생_기업직무적합1순위 = st.selectbox(
            "기업직무적합 1순위 *",
            ["기획", "마케팅", "생산", "연구개발", "영업", "인사", "재무", "홍보"],
            help="가장 잘 맞을 것 같은 기업 내 직무를 선택해주세요."
        )
    
    with col2:
        학생_산업선호도2순위 = st.selectbox(
            "산업선호도 2순위 *",
            ["개인서비스", "공공", "교육", "교통/물류", "금융", 
             "미디어/엔터테인먼트", "보건/의료", "산업기술/에너지공정", 
             "전자/첨단기술", "제조"],
            help="두 번째로 관심있는 산업 분야를 선택해주세요."
        )
        
        학생_기업직무적합2순위 = st.selectbox(
            "기업직무적합 2순위 *",
            ["기획", "마케팅", "생산", "연구개발", "영업", "인사", "재무", "홍보"],
            help="두 번째로 적합한 기업 내 직무를 선택해주세요."
        )
    
    # 근무 환경 선호
    st.markdown("**근무 환경 선호**")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        학생_근무환경선호_실내실외 = st.selectbox(
            "실내·실외 선호 *",
            ["실내", "실외", "상관없음"],
            index=2,
            help="선호하는 근무 환경을 선택해주세요."
        )
    
    with col2:
        학생_근무환경선호_교대근무 = st.selectbox(
            "교대근무 *",
            ["가능", "불가"],
            help="2교대, 3교대 등 번갈아 가며 근무하는 교대 근무가 가능한지 선택해주세요."
        )
    
    with col3:
        학생_근무환경선호_야간근무 = st.selectbox(
            "야간근무 *",
            ["가능", "불가"],
            help="밤 시간대 근무가 가능한지 선택해주세요."
        )
    
    with col4:
        학생_근무환경선호_고소작업 = st.selectbox(
            "고소작업 *",
            ["가능", "불가"],
            help="높은 곳에서의 작업이 가능한지 선택해주세요."
        )
    
    with col5:
        학생_근무환경선호_팀작업 = st.selectbox(
            "팀작업 선호 *",
            ["상관없음", "팀 작업 선호", "혼자 작업 선호"],
            help="업무 수행 시 선호하는 협업 방식을 선택해주세요."
        )
    
    st.markdown("---")
    
    # ========== 4단계: 자기인식 및 진로 관련 태도 ==========
    st.subheader("🧠 4단계: 자기인식 및 진로 관련 태도")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        학생_자기강점인식 = st.selectbox(
            "자기 강점 인식 *",
            ["매우 낮음", "낮음", "보통", "높음", "매우 높음"],
            index=2,
            help="스스로 인식하는 나의 강점 수준을 선택해주세요."           
        )
        
        학생_진로결정자기효능감 = st.selectbox(
            "진로결정 자기효능감 *",
            ["매우 낮음", "낮음", "보통", "높음", "매우 높음"],
            index=2,
            help="진로를 스스로 결정할 수 있는 자신감 수준을 선택해주세요."
        )
        
        학생_부모지지인식 = st.selectbox(
            "부모 지지 인식 *",
            ["매우 낮음", "낮음", "보통", "높음", "매우 높음"],
            index=2,
            help="부모님이 나의 진로를 얼마나 지지한다고 느끼는지 선택해주세요."
        )
    
    with col2:
        학생_학습태도자기평가 = st.selectbox(
            "학습태도 자기평가 *",
            ["매우 낮음", "낮음", "보통", "높음", "매우 높음"],
            index=2,
            help="학습 임하는 나의 태도와 노력 수준을 선택해주세요."
        )
        
        학생_진로변화의향 = st.selectbox(
            "진로 변화 의향 *",
            ["매우 낮음", "낮음", "보통", "높음", "매우 높음"],
            index=2,
            help="진로 계획을 바꿀 의향이 어느 정도인지 선택해주세요."
        )
        
        학생_부모압력인식 = st.selectbox(
            "부모 압력 인식 *",
            ["매우 낮음", "낮음", "보통", "높음", "매우 높음"],
            index=2,
            help="부모님이 진로에 얼마나 영향을 주거나 압력을 가한다고 느끼는지 선택해주세요."
        )
    
    with col3:
        학생_희망직무전망인식 = st.selectbox(
            "희망직무 전망 인식 *",
            ["매우 낮음", "낮음", "보통", "높음", "매우 높음"],
            index=2,
            help="희망 직무의 미래 전망을 어떻게 보는지 선택해주세요."
        )
        
        학생_진로대화만족도 = st.selectbox(
            "진로 대화 만족도 *",
            ["매우 불만족", "불만족", "보통", "만족", "매우 만족"],
            index=2,
            help="부모님과의 진로 대화에 얼마나 만족하는지 선택해주세요."
        )
    
    # 자기강점유형 및 희망직무일치수준
    col1, col2 = st.columns(2)
    
    with col1:
        학생_자기강점유형 = st.selectbox(
            "자기 강점 유형 *",
            ["책임감", "문제해결력", "집중력", "손재능", "의사소통", "협업능력", "리더십", "창의성", "기타"],
            help="본인이 가진 주요 강점을 선택해주세요."
        )
    
    with col2:
        학생_희망직무일치수준 = st.selectbox(
            "희망직무 일치 수준 *",
            ["거의 동일", "부분 유사", "완전 다름"],
            index=1,
            help="나와 부모님의 희망 직무가 어느 정도 일치한다고 생각하는지 선택해주세요."
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
# === [여기 붙여넣으세요] ===
        save_user_data(st.session_state.student_id, student_data=student_data)
        # ==========================        
        st.success("✅ 학생 정보가 저장되었습니다!")
        st.info("👈 사이드바에서 **📊 진행 현황**을 확인하거나, **👨‍👩‍👧 부모 정보 입력**으로 이동하세요.")
