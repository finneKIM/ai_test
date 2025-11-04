import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 백엔드 Fastapi 서버 주소
BASE_URL = "http://127.0.0.1:8000"

st.title("한국어 감정 분석 웹앱 (koBERT 기반)")
st.write("문장을 입력하면 koBERT 모델이 감정을 예측해줍니다.")
st.markdown("---")

# 사용자 입력
user_input = st.text_area("문장을 입력하세요", "오늘 하루가 너무 즐거워요!")

# 버튼 클릭 시 예측 요청
if st.button("감정 분석하기"):
    if not user_input.strip():
        st.warning("문장을 입력해주세요")
    else:
        with st.spinner("모델이 감정을 분석 중입니다🔍"):
            # FastAPI 서버에 post 요청 보내기
            response = requests.post(f"{BASE_URL}/predict",
                                     json={"text": user_input})
            
            # 응답처리
            if response.status_code == 200:
                result = response.json()
                st.success(f"예측된 감정: **{result['sentiment']}**")

                # --------확률 시각화1번 : altair 사용
                probs = result["probabilities"]
                df = pd.DataFrame(list(probs.items()), 
                                  columns=["감정", "확률"])
                st.bar_chart(df.set_index("감정"))

                
                # --------확률 시각화 2번 : matplotlib 사용
                # # Matplotlib의 폰트 매니저를 사용하여 폰트 설정
                # plt.rcParams['font.family'] = 'NanumGothic'
                # # 마이너스 부호 깨짐 방지
                # plt.rcParams['axes.unicode_minus'] = False
                # fig, ax = plt.subplots()
                # ax.bar(df["감정"], df["확률"])
                # ax.set_xlabel("감정")
                # ax.set_ylabel("확률")
                # ax.set_ylim(0,1)
                # st.pyplot(fig)

            else:
                st.error(f"오류 발생 : {response.text}")