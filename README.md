# 🎓 CareerBridge AI - 최종 완성 버전

특성화고 전기과 학생을 위한 AI 기반 진로 추천 시스템

---

## ✅ 완성된 기능

### 1. 딥러닝 기반 직무 예측
- **TabTransformer 모델** (정확도 75%)
- 5,000명 졸업생 데이터 학습
- NCS 기반 8개 전기 직무 분류

### 2. AI 맞춤형 진로 처방전
- **Gemini API** 통합 (gemini-flash-latest)
- NCS CBE, SCCT, RIASEC 이론 기반
- 3개 섹션: 진로 로드맵, 강점·약점 전략, 부모-학생 분석

### 3. 완성된 UI/UX
- 로그인/로그아웃 시스템
- 4개 페이지: 학생 정보, 부모 정보, 진행 현황, 결과 분석
- 데이터 캐싱 (중복 API 호출 방지)
- 반응형 디자인

---

## 📦 설치 방법

### 1. 필수 요구사항
- Python 3.8+
- pip

### 2. 패키지 설치
```bash
pip install -r requirements.txt --break-system-packages
```

### 3. Gemini API 키 설정
1. Google AI Studio에서 API 키 발급: https://aistudio.google.com/app/apikey
2. `.streamlit/secrets.toml` 파일 생성:
```toml
GEMINI_API_KEY = "여기에_발급받은_API_키_입력"
```

---

## 🚀 실행 방법

```bash
streamlit run app.py
```

브라우저에서 자동으로 열립니다 (기본: http://localhost:8501)

---

## 📁 파일 구조

```
careerbridge_final_complete/
├── app.py                          # 메인 앱 (로그인)
├── requirements.txt                # 패키지 목록
├── assets/
│   └── logo.png                    # 로고 이미지
├── models/
│   ├── best_model.pth              # 학습된 모델
│   ├── cat_encoders.pkl            # 범주형 인코더
│   ├── scaler.pkl                  # 스케일러
│   └── target_label_encoder.pkl    # 타겟 인코더
├── utils/
│   ├── gemini_api.py               # ✅ 수정: Gemini API (파싱 로직 개선)
│   └── model.py                    # ✅ 수정: ML 모델 ('불일치' → '완전 다름')
└── pages/
    ├── 1_🎓_학생_정보_입력.py       # 학생 데이터 입력
    ├── 2_👨‍👩‍👧_부모_정보_입력.py   # 부모 데이터 입력
    ├── 3_📊_진행_현황.py           # ✅ 수정: 데이터 수집 현황 (switch_page 제거)
    └── 4_🎯_결과_분석.py           # ✅ 수정: AI 분석 결과 (캐싱 추가)
```

---

## 🔧 주요 수정 사항

### 1. `utils/gemini_api.py`
- ✅ 원본 상세 프롬프트 복원 (NCS, SCCT, RIASEC)
- ✅ 파싱 로직 완전히 개선
- ✅ "1. 2. 3." 숫자만 제거 (제목은 유지)
- ✅ 다음 섹션 제목에서 자동으로 끊기
- ✅ fallback 함수 키 수정 (영어 키)

### 2. `utils/model.py`
- ✅ 희망직무일치수준: '불일치' → '완전 다름' (모델 학습 값)

### 3. `pages/4_🎯_결과_분석.py`
- ✅ 데이터 해시 기반 캐싱 (API 호출 최소화)
- ✅ import hashlib, json 추가
- ✅ 키 이름 통일 (roadmap, strategy, gap_analysis)

### 4. `pages/3_📊_진행_현황.py`
- ✅ st.switch_page() 제거 (Streamlit 1.29.0 호환)
- ✅ 안내 메시지로 대체

### 5. `requirements.txt`
- ✅ Streamlit 1.29.0 (안정 버전)
- ✅ google-generativeai 0.8.0+

---

## 🎯 사용 방법

### 1단계: 로그인
- 학생 이름 입력

### 2단계: 데이터 입력
- **학생 정보**: 학년, 희망직무, 직업기초능력, 교과 성취도 등
- **부모 정보**: 희망직무, 지지 수준, 진로 대화 빈도 등

### 3단계: 진행 현황 확인
- 입력 완료 여부 체크
- "AI 진로 분석 시작하기" 버튼 클릭

### 4단계: 결과 분석
- **AI 추천 직무 Top 3** (적합도 %)
- **전체 직무 적합도 분포** (차트)
- **희망 직무 비교 분석** (학생/부모/AI)
- **AI 맞춤형 진로 처방전** (3개 탭)
  - 🗺️ 진로 로드맵
  - 💪 강점·약점 전략
  - 👨‍👩‍👧 부모-학생 분석
- **전체 처방전 다운로드** (TXT)

---

## ⚠️ 주의사항

### Gemini API 무료 할당량
- **분당 15회** (gemini-flash-latest)
- **일일 1,500회**
- 초과 시 429 에러 (다음날까지 대기)

### 캐싱 기능
- 같은 데이터 재입력 시 API 호출 안 함
- 데이터 변경 시 자동으로 새 처방전 생성
- 로그아웃 시 캐시 초기화

---

## 🐛 트러블슈팅

### 1. Gemini API 오류
```
❌ Gemini API 키가 설정되지 않았습니다.
```
**해결:** `.streamlit/secrets.toml` 파일에 API 키 추가

### 2. 모델 로딩 오류
```
❌ 모델 로딩 오류: ...
```
**해결:** `models/` 폴더의 파일 확인 (4개 필수)

### 3. 인코딩 오류
```
⚠️ 인코딩 오류 (희망직무일치수준): ...
```
**해결:** 이미 수정됨 (utils/model.py)

### 4. 캐시 문제
**해결:** 캐시 삭제 후 재시작
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
streamlit run app.py
```

---

## 📊 기술 스택

- **Frontend**: Streamlit 1.29.0
- **ML**: PyTorch 2.0+, TabTransformer
- **AI**: Google Gemini API (gemini-flash-latest)
- **Data**: Pandas, NumPy, Scikit-learn
- **Visualization**: Plotly

---

## 📝 라이선스

Educational use only.

---

## 👤 개발자

Sunny 
Yonsei University Graduate School of Education
Educational Technology

---

## 🎉 완성!

**모든 기능이 안정적으로 작동합니다!**

문제 발생 시:
1. 캐시 삭제
2. 로그아웃 후 재로그인
3. 데이터 재입력

**Good luck with your project!** 🚀
