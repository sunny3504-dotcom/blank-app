# -*- coding: utf-8 -*-
"""
CareerBridge - AI 진로 추천 플랫폼
특성화고 전기과 학생을 위한 딥러닝 기반 진로 설계 시스템
"""
import os
import streamlit as st
from PIL import Image
from utils.storage import load_user_data

# 페이지 설정
st.set_page_config(
    page_title="로그인",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if 'student_id' not in st.session_state:
    st.session_state.student_id = None

if 'student_data' not in st.session_state:
    st.session_state.student_data = None

if 'parent_data' not in st.session_state:
    st.session_state.parent_data = None

# CSS 스타일링
if st.session_state.student_id:
    # 로그인 후: "홈" (연한 회색)
    st.markdown("""
<style>
    /* 사이드바 "홈" 스타일 (로그인 후) */
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
    
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem 0 1rem 0;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f0ff 100%);
        padding: 2rem;
        border-radius: 1rem;
        border-left: 5px solid #667eea;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        color: #667eea;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #555;
        line-height: 1.6;
    }
    
    .theory-box {
        background: linear-gradient(135deg, #fff9e6 0%, #ffe8cc 100%);
        padding: 2rem;
        border-radius: 1rem;
        border-left: 5px solid #f39c12;
        margin: 2rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        font-size: 1.2rem;
        padding: 1rem 3rem;
        border-radius: 0.8rem;
        border: none;
        width: 100%;
        margin-top: 2rem;
    }
    
    .stButton > button:hover {
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)
else:
    # 로그인 전: "로그인" (보라색)
    st.markdown("""
<style>
    /* 사이드바 "로그인" 스타일 (로그인 전) */
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] {
        padding-top: 1rem;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] li:first-child {
        background: none !important;
        padding: 0 !important;
        margin-bottom: 1rem;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] li:first-child a {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 0.5rem;
        padding: 0.8rem 1rem !important;
        pointer-events: none;
        display: block;
        text-align: center;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] li:first-child a span {
        font-size: 0 !important;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] li:first-child a span::before {
        content: "로그인";
        font-size: 1.2rem !important;
        font-weight: 600;
        color: white;
    }
    
    /* 로고 컨테이너 중앙 정렬 */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem 0 1rem 0;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f0ff 100%);
        padding: 2rem;
        border-radius: 1rem;
        border-left: 5px solid #667eea;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        color: #667eea;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #555;
        line-height: 1.6;
    }
    
    .theory-box {
        background: linear-gradient(135deg, #fff9e6 0%, #ffe8cc 100%);
        padding: 2rem;
        border-radius: 1rem;
        border-left: 5px solid #f39c12;
        margin: 2rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        font-size: 1.2rem;
        padding: 1rem 3rem;
        border-radius: 0.8rem;
        border: none;
        width: 100%;
        margin-top: 2rem;
    }
    
    .stButton > button:hover {
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# 로고 이미지 표시
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=400)
else:
    st.title("🎓 CareerBridge")
st.markdown("</div>", unsafe_allow_html=True)

# 사이드바에 로그아웃 버튼 추가 (로그인 후에만)
if st.session_state.student_id:
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 로그아웃", key="sidebar_logout", use_container_width=True):
        st.session_state.student_id = None
        st.session_state.student_data = None
        st.session_state.parent_data = None
        st.rerun()

# 부제목
st.markdown('<p class="subtitle">특성화고 전기과 학생을 위한 AI 진로 추천 플랫폼</p>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">5000명 졸업생 데이터</div>
        <div class="feature-desc">
            실제 졸업생 빅데이터 기반 분석으로 신뢰도 높은 진로 추천
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💡</div>
        <div class="feature-title">GPT 맞춤형 처방전</div>
        <div class="feature-desc">
            Gemini AI가 생성하는 개인별 진로 로드맵
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">딥러닝 모델 정확도 75%</div>
        <div class="feature-desc">
            TabTransformer AI 기반 정밀 직무 예측
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📚</div>
        <div class="feature-title">교육공학 이론 기반</div>
        <div class="feature-desc">
            과학적 진로 설계 시스템
        </div>
    </div>
    """, unsafe_allow_html=True)

# 이론적 프레임워크 설명
st.markdown("""
<div class="theory-box">
    <h3 style="color: #f39c12; margin-bottom: 1rem;">📖 적용된 교육 이론</h3>
    <p style="line-height: 1.8; color: #555;">
        <strong>• NCS 기반 능력기반교육(CBE)</strong>: 지식·기능·태도 중심 역량 평가<br>
        <strong>• SCCT 사회인지 진로이론</strong>: 자기효능감, 진로목표, 맥락적 지지·장벽 분석<br>
        <strong>• Holland RIASEC 이론</strong>: 흥미 유형과 직무 환경 적합도(Person-Environment Fit)
    </p>
</div>
""", unsafe_allow_html=True)

# 로그인 섹션
st.markdown("---")
st.markdown("### 🔑 시작하기")

# 로그인 폼
with st.form("login_form"):
    st.markdown("학생 이름을 입력하고 진로 분석을 시작하세요.")
    
    student_name = st.text_input(
        "학생 이름 *",
        placeholder="예: 박선희(2025431005)",
        help="학생 이름 또는 학번을 입력해주세요."
    )
    
    submitted = st.form_submit_button("🎓 CareerBridge 시작하기")
    
    if submitted:
        if student_name and len(student_name.strip()) > 0:
            st.session_state.student_id = student_name.strip()
# === [여기 붙여넣으세요] ===
            saved_data = load_user_data(st.session_state.student_id)
            if saved_data:
                if 'student_data' in saved_data:
                    st.session_state.student_data = saved_data['student_data']
                if 'parent_data' in saved_data:
                    st.session_state.parent_data = saved_data['parent_data']
                if 'prescriptions' in saved_data:
                    for key, value in saved_data['prescriptions'].items():
                        st.session_state[key] = value
                st.toast("📂 이전 작업 내용을 불러왔습니다.", icon="✅")
            # ==========================            
            st.success(f"✅ {student_name}님, 환영합니다!")
            st.info("👈 왼쪽 사이드바에서 **학생 정보 입력**을 시작하세요.")
        else:
            st.error("❌ 학생 이름을 입력해주세요.")

# 현재 세션 상태 표시
if st.session_state.student_id:
    st.markdown("---")
    st.markdown(f"**현재 세션:** {st.session_state.student_id}")
    
    # 진행 상태 요약
    progress_col1, progress_col2, progress_col3 = st.columns(3)
    
    with progress_col1:
        if st.session_state.student_data:
            st.success("✅ 학생 정보 입력 완료")
        else:
            st.warning("⏳ 학생 정보 입력 대기")
    
    with progress_col2:
        if st.session_state.parent_data:
            st.success("✅ 부모 정보 입력 완료")
        else:
            st.warning("⏳ 부모 정보 입력 대기")
    
    with progress_col3:
        if st.session_state.student_data and st.session_state.parent_data:
            st.success("✅ AI 분석 준비 완료")
        else:
            st.info("ℹ️ 정보 입력 진행 중")

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 2rem 0;'>
    <p>© 2025 CareerBridge. All rights reserved.</p>
    <p style='font-size: 0.9rem;'>특성화고 전기과 학생을 위한 AI 진로 추천 시스템</p>
</div>
""", unsafe_allow_html=True)
