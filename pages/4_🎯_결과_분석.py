# -*- coding: utf-8 -*-
"""
AI 진로 분석 결과 페이지
"""

import streamlit as st
import sys
from pathlib import Path
import hashlib
import json
from utils.storage import save_user_data

# utils 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.model import predict_job
from utils.gemini_api import generate_prescription
import plotly.graph_objects as go

st.set_page_config(page_title="결과 분석", page_icon="🎯", layout="wide")

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

# 로그인 및 데이터 확인
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

if st.session_state.student_data is None or st.session_state.parent_data is None:
    st.error("⚠️ 학생과 부모 데이터를 모두 입력해야 분석을 시작할 수 있습니다.")
    st.info("👈 사이드바에서 **📊 진행 현황**을 확인하세요.")
    st.stop()

st.title("🎯 AI 진로 설계 리포트")
st.markdown(f"**학생:** {st.session_state.student_id}")
st.markdown("---")

# 분석 실행
with st.spinner("🤖 딥러닝 모델이 데이터를 분석하고 있습니다..."):
    try:
        # 예측 실행
        prediction = predict_job(
            st.session_state.student_data,
            st.session_state.parent_data
        )
        
        if prediction is None:
            st.error("❌ 예측 중 오류가 발생했습니다. 입력 데이터를 확인해주세요.")
            st.stop()
        
    except Exception as e:
        st.error(f"❌ 예측 오류: {str(e)}")
        st.stop()

# 1. AI 추천 직무 (Top 3)
st.markdown("## 🎯 AI 추천 직무 (딥러닝 분석 결과)")

col1, col2, col3 = st.columns(3)

for i, (job, prob) in enumerate(zip(prediction['top3_jobs'], prediction['top3_probs'])):
    with [col1, col2, col3][i]:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8f9ff 0%, #e8f0ff 100%); 
                    padding: 2rem; border-radius: 1rem; border-left: 5px solid #667eea;
                    text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <h3 style="color: #667eea; margin: 0;">🥇 {i+1}위</h3>
            <h2 style="color: #2c3e50; margin: 1rem 0;">{job}</h2>
            <p style="font-size: 2rem; font-weight: 700; color: #667eea; margin: 0;">
                {prob*100:.1f}%
            </p>
            <p style="color: #7f8c8d; font-size: 0.9rem; margin: 0.5rem 0 0 0;">적합도</p>
        </div>
        """, unsafe_allow_html=True)

# 여백 추가 (겹침 방지)
st.markdown("<br><br>", unsafe_allow_html=True)

# 확률 분포 차트
st.markdown("### 📊 전체 직무 적합도 분포")

fig = go.Figure(data=[
    go.Bar(
        x=prediction['top3_jobs'],
        y=prediction['top3_probs'],
        marker=dict(
            color=['#667eea', '#764ba2', '#9b6ec9'],
            line=dict(color='white', width=2)
        ),
        text=[f"{p*100:.1f}%" for p in prediction['top3_probs']],
        textposition='auto',
    )
])

fig.update_layout(
    title="상위 3개 추천 직무 적합도",
    xaxis_title="직무",
    yaxis_title="적합도 (%)",
    height=400,
    yaxis=dict(tickformat='.0%'),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

st.plotly_chart(fig, use_container_width=True)

# 희망 직무 비교
st.markdown("---")
st.markdown("## 🔍 희망 직무 비교 분석")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="background: #e8f8f0; padding: 1.5rem; border-radius: 1rem; border-left: 5px solid #27ae60;">
        <h4 style="color: #27ae60; margin: 0 0 0.5rem 0;">🎓 학생 희망</h4>
        <h3 style="color: #2c3e50; margin: 0;">{prediction['student_hope']}</h3>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: #fff3e6; padding: 1.5rem; border-radius: 1rem; border-left: 5px solid #f39c12;">
        <h4 style="color: #f39c12; margin: 0 0 0.5rem 0;">👨‍👩‍👧 부모 희망</h4>
        <h3 style="color: #2c3e50; margin: 0;">{prediction['parent_hope']}</h3>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: #e8e8ff; padding: 1.5rem; border-radius: 1rem; border-left: 5px solid #667eea;">
        <h4 style="color: #667eea; margin: 0 0 0.5rem 0;">🤖 AI 추천</h4>
        <h3 style="color: #2c3e50; margin: 0;">{prediction['top3_jobs'][0]}</h3>
    </div>
    """, unsafe_allow_html=True)

# 일치도 분석
if prediction['student_hope'] == prediction['parent_hope'] == prediction['top3_jobs'][0]:
    st.success("✅ 학생, 부모, AI가 모두 동일한 직무를 추천하고 있습니다! 매우 이상적인 진로 방향입니다.")
elif prediction['student_hope'] == prediction['top3_jobs'][0]:
    st.info("ℹ️ AI 추천이 학생의 희망과 일치합니다. 객관적 데이터가 학생의 선택을 지지하고 있습니다.")
elif prediction['parent_hope'] == prediction['top3_jobs'][0]:
    st.info("ℹ️ AI 추천이 부모님의 희망과 일치합니다. 부모님의 직관이 데이터와 부합합니다.")
else:
    st.warning("⚠️ 학생, 부모, AI의 추천이 서로 다릅니다. 아래 맞춤형 처방전에서 조율 방안을 확인하세요.")

# AI 처방전 생성
st.markdown("---")
st.markdown("## 💡 AI 맞춤형 진로 처방전")

# 캐시 키 생성 (데이터 내용 기반 해시)
cache_data = json.dumps({
    'student': st.session_state.student_data,
    'parent': st.session_state.parent_data,
    'prediction': prediction
}, sort_keys=True)
cache_key = f"prescription_{hashlib.md5(cache_data.encode()).hexdigest()}"

# 이미 생성된 처방전이 있으면 재사용
if cache_key not in st.session_state:
    with st.spinner("🤖 Gemini AI가 맞춤형 진로 로드맵을 생성하고 있습니다..."):
        try:
            prescription = generate_prescription(
                st.session_state.student_data,
                st.session_state.parent_data,
                prediction
            )
            # 캐시에 저장
            st.session_state[cache_key] = prescription
# === [여기 붙여넣으세요] ===
            save_user_data(
                st.session_state.student_id, 
                prescription=prescription, 
                cache_key=cache_key
            )
            # ==========================            
            if prescription is None:
                st.warning("""
                ⚠️ **Gemini API 키가 설정되지 않았습니다.**
                
                AI 맞춤형 처방전을 생성하려면 다음 단계를 따라주세요:
                
                1. Google AI Studio에서 Gemini API 키 발급: https://aistudio.google.com/app/apikey
                2. Codespaces에서 `.streamlit/secrets.toml` 파일 생성
                3. 다음 내용 추가:
                ```
                GEMINI_API_KEY = "여기에_API_키_입력"
                ```
                4. 앱 재시작
                
                **현재는 기본 템플릿 처방전이 표시됩니다.**
                """)
                prescription = {
                    'roadmap': "AI 처방전 생성을 위해 Gemini API 키를 설정해주세요.",
                    'strategy': "API 키 설정 후 맞춤형 분석이 제공됩니다.",
                    'gap_analysis': "API 키 설정 후 상세한 조율 전략이 제공됩니다.",
                    'full_text': "AI 처방전 생성을 위해 Gemini API 키를 설정해주세요."
                }
                st.session_state[cache_key] = prescription
        except Exception as e:
            st.error(f"❌ 처방전 생성 오류: {str(e)}")
            prescription = None
            st.session_state[cache_key] = prescription
else:
    # 캐시된 처방전 사용
    st.info("✅ 저장된 처방전을 불러왔습니다. (동일한 데이터, API 호출 안 함)")
    prescription = st.session_state[cache_key]

if prescription:
    # 탭으로 구분
    tab1, tab2, tab3 = st.tabs(["🗺️ 진로 로드맵", "💪 강점·약점 전략", "👨‍👩‍👧 부모-학생 분석"])
    
    with tab1:
        st.markdown("### 🗺️ 진로 로드맵")
        st.markdown(prescription['roadmap'])
    
    with tab2:
        st.markdown("### 💪 강점·약점 기반 전략")
        st.markdown(prescription['strategy'])
    
    with tab3:
        st.markdown("### 👨‍👩‍👧 부모-학생 인식 차이 분석 및 처방")
        st.markdown(prescription['gap_analysis'])
    
    # 전체 처방전 다운로드
    st.markdown("---")
    st.download_button(
        label="📄 전체 처방전 다운로드 (TXT)",
        data=prescription['full_text'],
        file_name=f"진로처방전_{st.session_state.student_id}.txt",
        mime="text/plain"
    )

# 추가 정보
st.markdown("---")
st.markdown("### 📚 다음 단계")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **📖 학습 자료 추천**
    - NCS 학습모듈 활용
    - 온라인 강좌 수강
    - 실무 프로젝트 참여
    """)

with col2:
    st.markdown("""
    **🎯 실행 계획**
    - 자격증 취득 일정 수립
    - 멘토 찾기
    - 인턴십 기회 탐색
    """)

# 재분석 버튼
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔄 데이터 수정 후 재분석하기", use_container_width=True):
        st.info("👈 사이드바에서 **📊 진행 현황**으로 이동하여 데이터를 수정할 수 있습니다.")
