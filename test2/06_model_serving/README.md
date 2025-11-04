# KoBERT 감정 분석 웹앱 (FastAPI + Streamlit)

이 프로젝트는 **한국어 감정 분석(KoBERT 기반)** 모델을 **FastAPI** 백엔드와 **Streamlit** 프론트엔드로 통합하여 웹 환경에서 문장을 입력하면 즉시 감정을 예측해주는 애플리케이션입니다.

---

## 프로젝트 구조
```
test2/

└── 06_model_serving/

├── main.py           # FastAPI: 모델 로드 + 감정 예측 API

├── frontend.py       # Streamlit: 웹 UI (입력 + 결과 시각화)

├── pyproject.toml    # uv 의존성 관리

├── uv.lock           # 버전 고정 (재현성 확보)

└── .gitignore        # 불필요 파일 제외 설정

```
---

## 실행 방법

### 1️⃣환경 세팅

이 프로젝트는 **uv(패키지 관리자)** 를 사용합니다.

```
pip install uv
uv init -p (파이썬 버전)
uv sync    # 의존성 설치
```
---

### 2️⃣ 백엔드 실행 (FastAPI)
```
uv run uvicorn main:app --reload --port 8000
```
- 모델이 자동으로 로드되고 `/predict` API가 활성화 됨
- 브라우저에서 http://127.0.0.1:8000/docs 로 접속하면 API 테스트 가능.

---
### 3️⃣ 프론트엔드 실행 (Streamlit)
```
uv run streamlit run frontend.py
```
- 웹페이지가 자동 실행되며 http://localhost:8501 에서 사용 가능.
- 문장을 입력하면 모델이 감정을 분석하고 막대그래프로 확률을 시각화함

---

## 주요 기능
| 구분 | 기술 | 설명 |
| --- | --- | --- |
| **모델** | [jeonghyeon97/koBERT-Senti5](https://huggingface.co/jeonghyeon97/koBERT-Senti5) | 한국어 감정 분류 모델 |
| **백엔드** | FastAPI | REST API 서버 (감정 예측 수행) |
| **프론트엔드** | Streamlit | 사용자 입력/결과 시각화 UI |
| **환경 관리** | uv + pyproject.toml | Python 패키지 버전 관리 |
| **시각화** | Altair (<5.0) / Matplotlib | 감정별 확률 막대그래프 표시 |


----

## API 예시
**요청**

```
POST /predict
{
  "text": "오늘 하루가 너무 즐거워요!"
}

```

**응답**

```
{
  "sentiment": "Happy",
  "probabilities": {
    "Angry": 0.01,
    "Fear": 0.03,
    "Happy": 0.85,
    "Tender": 0.08,
    "Sad": 0.03
  }
}
```

---

## 프로젝트 실행 화면
```
한국어 감정 분석 웹앱 (KoBERT 기반)
-----------------------------------
문장을 입력하세요:
> 오늘 하루가 너무 즐거워요!

예측된 감정: **Happy**
[감정별 확률 막대 그래프 표시]
```

---
## pyproject.toml 주요 설정
```
[project]
name = "06-model-serving"
version = "0.1.0"
requires-python = ">=3.14"

dependencies = [
    "altair<5",                   # Streamlit 호환 버전
    "matplotlib>=3.10.7",         # 대체 시각화 라이브러리
    "pandas>=2.3.3",              # 데이터 처리
    "pyarrow>=22.0.0",            # Streamlit 내부 최적화용
    "streamlit>=1.50.0",          # 프론트엔드
    "typing-extensions>=4.15.0"   # Altair 호환성용
]
```

---
## 라이선스


이 프로젝트는 **MIT License**를 따르며, 모델은 [Hugging Face Hub](https://huggingface.co/jeonghyeon97/koBERT-Senti5)의 공개 KoBERT-Senti5를 사용합니다.

---


## 확장 계획

- [ ]  감정별 색상 테마 적용 (예: Happy=노랑, Sad=파랑)
- [ ]  사용자 입력 로그 저장
- [ ]  REST API + Streamlit Docker Compose 통합
- [ ]  배포용 Cloud Run 버전 제작


