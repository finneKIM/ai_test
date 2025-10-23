간단한 심리테스트 웹앱입니다.  
Streamlit을 이용해 제작하였으며, MBTI 검사와 별자리 찾기 기능을 제공합니다.

---

## 프로젝트 구조

```
test1/
│
├── psycho_test.py # 메인 페이지
├── requirements.txt # 필요 패키지
└── pages/
├── 내 MBTI 알아보기.py # MBTI 검사 페이지
└── 내 별자리 찾기.py # 별자리 찾기 페이지
```


---

## 주요 기능

### 1️⃣ 심리테스트 메인
- Streamlit 기반 인터페이스
- 버튼 클릭으로 두 가지 테스트 중 하나 선택
  - `내 MBTI 알아보기`
  - `나의 별자리는?!`

### 2️⃣ MBTI 검사
- 총 4가지 문항으로 간단한 MBTI 결과 도출
- 각 항목은 `st.radio()`로 선택
- `결과보기` 버튼 클릭 시 결과 출력

### 3️⃣ 별자리 찾기
- `st.date_input()`으로 생년월일 선택
- 입력된 월/일에 맞는 별자리 자동 계산 및 표시

---

## 실행 방법

```
# 1. 가상환경 생성 (선택)
python -m venv myenv
source myenv/Scripts/activate  # Windows 기준

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 실행
streamlit run test1/psycho_test.py
```
| 실행 후 터미널에 표시되는 주소 http://localhost:8501 에 접속하면 앱이 실행됩니다.

---

## 기술 스택

| 구분           | 사용 기술              |
| ------------ | ------------------ |
| **언어**       | Python             |
| **웹 프레임워크**  | Streamlit          |
| **라이브러리 관리** | requirements.txt   |
| **인터랙션 요소**  | 버튼, 라디오버튼, 날짜입력 위젯 |


---

## 향후 발전 방향
- MBTI/별자리 결과에 따른 추가 설명 및 이미지 출력
- 사용자 결과 저장 기능 추가
- AI 기반 추천 기능 확장 (예: 성향별 추천 문구 등)

---
© 2025. Made by [finneKIM]
