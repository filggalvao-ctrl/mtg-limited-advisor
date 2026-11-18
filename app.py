import streamlit as st
import requests
import pandas as pd

st.title("MTG Limited Advisor")

st.subheader("TRK Set Import")

if st.button("Load Star Trek Set"):

    all_cards = []

    url = "https://api.scryfall.com/cards/search?q=set%3Atrk"

    progress = st.empty()

    while url:

        progress.write(f"Loading: {url}")

        response = requests.get(url)

        data = response.json()

        for card in data["data"]:

            all_cards.append({
                "name": card.get("name"),
                "mana_cost": card.get("mana_cost"),
                "mana_value": card.get("cmc"),
                "colors": ",".join(card.get("colors", [])),
                "type_line": card.get("type_line"),
                "rarity": card.get("rarity"),
                "power": card.get("power"),
                "toughness": card.get("toughness"),
                "oracle_text": card.get("oracle_text")
            })

        if data.get("has_more"):
            url = data.get("next_page")
        else:
            url = None

    df = pd.DataFrame(all_cards)

    st.success(
        f"Loaded {len(df)} cards from Star Trek Set"
    )

    st.dataframe(df.head(20))

    csv = df.to_csv(index=False)

    st.download_button(
        "Download TRK CSV",
        csv,
        "TRK_cards.csv",
        "text/csv"
    )
