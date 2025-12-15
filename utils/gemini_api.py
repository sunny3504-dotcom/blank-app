"""
Gemini API 통합 모듈
NCS, SCCT, RIASEC 기반 진로 처방전 생성 (가독성 개선 버전)
"""

import streamlit as st
import os


def initialize_gemini():
    """Gemini API 초기화"""
    try:
        import google.generativeai as genai

        # API 키 확인
        api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

        if not api_key:
            return None

        genai.configure(api_key=api_key)

        # 모델 초기화
        model = genai.GenerativeModel('gemini-flash-latest')
        return model

    except Exception as e:
        st.warning(f"⚠️ Gemini API 초기화 실패: {e}")
        return None



def generate_prescription(student_data: dict, parent_data: dict, prediction: dict):
    """
    NCS CBE, SCCT, RIASEC 이론 기반 맞춤형 진로 처방전 생성
    """

    model = initialize_gemini()

    if model is None:
        return generate_fallback_prescription(student_data, parent_data, prediction)

    # 직업기초능력 평균 계산
    jik_avg = (
        student_data.get('학생_직기초_의사소통_국어', 3) +
        student_data.get('학생_직기초_의사소통_영어', 3) +
        student_data.get('학생_직기초_수리활용', 3) +
        student_data.get('학생_직기초_문제해결', 3) +
        student_data.get('학생_직기초_직무적응', 3)
    ) / 5

    # 프롬프트 생성
    prompt = f"""
※ 개인정보, 의료정보, 정신건강, 가족 갈등, 심리 진단, 상담 등 민감한 내용은 절대 언급하거나 추론하지 마십시오.
학생과 부모를 평가하거나 단정하는 표현도 사용하지 마십시오.

⚠️ 아래 규칙은 반드시 지켜야 합니다.
1) 출력은 반드시 3개의 섹션으로 구성해야 합니다.
2) 각 섹션 제목은 반드시 아래 형식을 따라야 합니다:
   [진로 로드맵], [강점·약점 전략], [부모–학생 분석]
3) 각 섹션 본문은 제목 바로 아래에 작성해야 합니다.
4) 각 섹션 사이에는 반드시 정확히 [[SECTION_SPLIT]] 를 삽입해야 합니다.
5) 구분자를 생략하거나 변형하면 안 됩니다.
6) 섹션 1 → 섹션 2 → 섹션 3 순서를 반드시 유지하십시오.

당신은 특성화고 전기과 학생을 위한 전문 진로 컨설턴트입니다.
아래 학생 데이터를 기반으로 **가독성이 높고 실천적인 진로 처방전**을 작성하세요.

---
## 1. 학생 기본 데이터
- 학년: {student_data.get('학년', 1)}학년
- 희망 직무: {student_data.get('학생_희망직무', '')} (일치도: {student_data.get('학생_희망직무일치수준', '')})
- 추천 직무(AI): {prediction['top3_jobs'][0]} (적합도 {prediction['top3_probs'][0]*100:.1f}%)

## 2. 역량 및 성향 (NCS & RIASEC)
- 직업기초능력 평균: {jik_avg:.2f}등급
- 교과성취도: 전기({student_data.get('학생_전기교과성취도')}), 수학({student_data.get('학생_수학교과성취도')})
- 자격증: 전기기능사({student_data.get('학생_자격증_전기기능사')})
- 흥미유형: {student_data.get('학생_직업환경유형', '')}
- 근무선호: {student_data.get('학생_근무환경선호_실내실외', '')}, {student_data.get('학생_근무환경선호_팀작업', '')}

## 3. 부모님 인식 (SCCT 배경)
- 부모 희망직무: {parent_data.get('부모_희망직무', '')}
- 지지 수준: {parent_data.get('부모_지지수준', '')}
- 압력 수준: {parent_data.get('부모_압력수준', '')}
- 진로 대화 빈도: {parent_data.get('부모_진로대화빈도', '')}

---

## 반드시 작성할 결과물 (3개 섹션)

[진로 로드맵]
- 현재 위치: 학생의 현재 역량을 NCS 관점에서 요약
- 학년별 목표: {student_data.get('학년', 1)}학년부터 졸업까지의 로드맵
- 성장 전략: 부족한 직업기초능력/교과목 보완 전략 2~3개
[[SECTION_SPLIT]]

[강점·약점 전략]
- 핵심 강점: 학생의 강점이 추천 직무({prediction['top3_jobs'][0]})에서 어떻게 발휘되는지
- 보완점: 약점을 보완하기 위한 구체적 학습/태도 전략
- 직무 적합성(Fit): 학생 성향과 직무 환경의 일치 여부 분석
[[SECTION_SPLIT]]

[부모–학생 분석]
- 인식 차이: 부모와 학생의 희망 직무 차이를 객관적으로 비교
- 지지와 소통: 부모의 지지·압력 수준 기반 대화 전략
- AI 제언: 갈등을 줄이고 시너지를 낼 수 있는 실질적 제안

이제 작성을 시작하세요.
"""

    try:
        response = model.generate_content(prompt)

        # 응답 안전성 체크
        if (
            not response
            or not getattr(response, "candidates", None)
            or len(response.candidates) == 0
            or not response.candidates[0].content.parts
        ):
            return {
                "roadmap": "⚠️ Gemini가 안전성 정책으로 인해 응답을 생성하지 못했습니다.",
                "strategy": "⚠️ 기본 분석만 제공됩니다.",
                "gap_analysis": "⚠️ 응답 생성 실패로 인해 간단한 메시지만 제공합니다."
            }

        text = response.text

        # 섹션 분리
        parts = text.split("[[SECTION_SPLIT]]")
        roadmap = parts[0].strip() if len(parts) > 0 else ""
        strategy = parts[1].strip() if len(parts) > 1 else ""
        gap_analysis = parts[2].strip() if len(parts) > 2 else ""

        # 헤더 제거 함수
        def clean_headers(t):
            return "\n".join([line for line in t.split("\n") if not line.startswith("#")]).strip()

        return {
            "roadmap": clean_headers(roadmap),
            "strategy": clean_headers(strategy),
            "gap_analysis": clean_headers(gap_analysis),
            "full_text": text.replace("[[SECTION_SPLIT]]", "\n\n---\n\n")
        }

    except Exception as e:
        st.error(f"❌ Gemini API 호출 오류: {e}")
        return generate_fallback_prescription(student_data, parent_data, prediction)



def generate_fallback_prescription(student_data: dict, parent_data: dict, prediction: dict):
    """Gemini API 사용 불가 시 기본 처방전"""
    
    roadmap = f"""
**🎓 NCS 기반 단계별 성장 로드맵**
* 직업기초능력 평균 {student_data.get('학생_직기초_의사소통_국어', 3)}등급
"""

    strategy = f"""
**💪 강점·약점 기반 전략**
* 강점: {student_data.get('학생_자기강점유형', '성실함')}
"""

    gap_analysis = f"""
**👨‍👩‍👧 부모–학생 인식 분석**
* 학생 희망직무: {student_data.get('학생_희망직무', '')}
"""

    return {
        "roadmap": roadmap,
        "strategy": strategy,
        "gap_analysis": gap_analysis,
        "full_text": f"{roadmap}\n\n{strategy}\n\n{gap_analysis}"
    }
