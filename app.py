import streamlit as st
import requests
import json

st.title("MTG Limited Advisor")

if st.button("Test Scryfall"):

    url = "https://api.scryfall.com/cards/search?q=set%3Atrk"

    response = requests.get(
        url,
        headers={
            "User-Agent": "mtg-limited-advisor"
        }
    )

    st.write("Status Code:", response.status_code)

    try:
        data = response.json()

        st.subheader("JSON Response")

        st.json(data)

    except Exception as e:

        st.error(str(e))
