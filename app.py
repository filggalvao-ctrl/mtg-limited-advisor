import streamlit as st

st.title("MTG Limited Advisor")

pool_text = st.text_area(
    "Paste Pool Here",
    height=400
)

if st.button("Analyze"):
    st.write("Pool received")
    st.code(pool_text)
