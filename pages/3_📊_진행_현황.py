# -*- coding: utf-8 -*-
"""
데이터 수집 진행 현황 페이지
"""

import streamlit as st

st.set_page_config(page_title="진행 현황", page_icon="📊", layout="wide")

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

st.title("📊 데이터 수집 진행 현황")
st.markdown(f"**세션 ID:** {st.session_state.student_id}")
st.markdown("---")

# 진행 현황 카드
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎓 학생 데이터")
    if st.session_state.student_data is not None:
        st.success("✅ **완료**")
        st.info("학생의 역량 및 관심사 입력이 완료되었습니다.")
        
        with st.expander("📄 입력된 학생 정보 미리보기"):
            data = st.session_state.student_data
            st.write(f"**학년:** {data.get('학년')}")
            st.write(f"**희망직무:** {data.get('학생_희망직무')}")
            st.write(f"**전기교과성취도:** {data.get('학생_전기교과성취도')}")
            st.write(f"**수학교과성취도:** {data.get('학생_수학교과성취도')}")
            st.write(f"**자격증(전기기능사):** {data.get('학생_자격증_전기기능사')}")
            
            # 직업기초능력 평균
            jik_avg = (
                data.get('학생_직기초_의사소통_국어', 0) +
                data.get('학생_직기초_의사소통_영어', 0) +
                data.get('학생_직기초_수리활용', 0) +
                data.get('학생_직기초_문제해결', 0) +
                data.get('학생_직기초_직무적응', 0)
            ) / 5
            st.write(f"**직업기초능력 평균:** {jik_avg:.1f}점")
        
        if st.button("🔄 학생 정보 수정하기", key="edit_student"):
            st.info("👈 사이드바에서 **🎓 학생 정보 입력**을 선택하여 수정할 수 있습니다.")
    else:
        st.warning("⚠️ **미완료**")
        st.info("학생의 역량 및 관심사 입력이 필요합니다.")
        if st.button("📝 학생 정보 입력하러 가기"):
            st.info("👈 사이드바에서 **🎓 학생 정보 입력**을 선택하세요.")

with col2:
    st.markdown("### 👨‍👩‍👧 부모 데이터")
    if st.session_state.parent_data is not None:
        st.success("✅ **완료**")
        st.info("부모님의 자녀 진로 인식 정보 입력이 완료되었습니다.")
        
        with st.expander("📄 입력된 부모 정보 미리보기"):
            data = st.session_state.parent_data
            st.write(f"**부모 희망직무:** {data.get('부모_희망직무')}")
            st.write(f"**진로 지지수준:** {data.get('부모_지지수준')}")
            st.write(f"**자녀 강점 인식:** {data.get('부모_자녀강점인식')}")
            st.write(f"**진로 대화 빈도:** {data.get('부모_진로대화빈도')}")
        
        if st.button("🔄 부모 정보 수정하기", key="edit_parent"):
            st.info("👈 사이드바에서 **👨‍👩‍👧 부모 정보 입력**을 선택하여 수정할 수 있습니다.")
    else:
        st.warning("⚠️ **미완료**")
        st.info("부모님의 자녀 진로 인식 정보 입력이 필요합니다.")
        if st.button("📝 부모 정보 입력하러 가기"):
            st.info("👈 사이드바에서 **👨‍👩‍👧 부모 정보 입력**을 선택하세요.")

# 안내 메시지
st.markdown("---")

if st.session_state.student_data is None or st.session_state.parent_data is None:
    st.warning("""
    ⚠️ **정확한 분석을 위해 학생과 부모 데이터를 모두 입력해주세요.**
    
    AI 딥러닝 모델은 다음 항목들을 종합적으로 분석합니다:
    - NCS 직업기초능력 (의사소통, 수리활용, 문제해결 등)
    - RIASEC 흥미 검사 결과
    - 교과 성취도 (전기, 수학)
    - 부모-학생 진로 인식 차이
    """)
else:
    st.success("""
    ✅ **모든 데이터 입력이 완료되었습니다!**
    
    이제 딥러닝 모델이 맞춤형 진로 분석을 시작할 수 있습니다.
    아래 버튼을 눌러 Gemini AI를 통한 진로 분석 결과를 시작하세요.
    """)

# 분석 시작 버튼
st.markdown("---")

if st.session_state.student_data is not None and st.session_state.parent_data is not None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 AI 진로 분석 시작하기", use_container_width=True, type="primary"):
            st.info("👈 사이드바에서 **🎯 결과 분석**을 선택하세요.")
else:
    st.info("💡 학생과 부모 정보를 모두 입력하면 분석을 시작할 수 있습니다.")

# 시스템 안내
st.markdown("---")
st.markdown("### 💡 분석 과정 안내")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **1단계: NCS 직무 정보 매핑**
    
    📌 입력된 데이터를 NCS 직무 분류 체계와 매핑합니다.
    """)

with col2:
    st.markdown("""
    **2단계: 딥러닝 모델 예측**
    
    🤖 TabTransformer 모델이 5000명의 졸업생 데이터를 기반으로 최적의 직무를 예측합니다.
    """)

with col3:
    st.markdown("""
    **3단계: AI 처방전 생성**
    
    💡 Gemini AI가 학생-부모 데이터를 종합하여 맞춤형 진로 로드맵을 생성합니다.
    """)
