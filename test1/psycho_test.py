import streamlit as st

st.title("심리 테스트")
st.text("간단한 심리 테스트, 시작!")

## switch_pages
if st.button("내 MBTI 알아보기"):
    st.switch_page('pages/내 MBTI 알아보기.py')

if st.button("나의 별자리는?!"):
    st.switch_page('pages/내 별자리 찾기.py')
