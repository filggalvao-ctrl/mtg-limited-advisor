import streamlit as st
import pandas as pd
import requests

st.title("MTG Limited Advisor")

pool_text = st.text_area(
    "Paste Pool Here",
    height=400
)

if st.button("Analyze"):

    cards = []
    total_cards = 0

    lines = pool_text.strip().split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        parts = line.split(" ", 1)

        if len(parts) != 2:
            continue

        try:
            qty = int(parts[0])
        except:
            continue

        name = parts[1]

        total_cards += qty

        url = (
            "https://api.scryfall.com/cards/named"
            f"?exact={name}"
        )

        card_type = "Not Found"
        status_code = "N/A"

        try:

            response = requests.get(url)

            status_code = response.status_code

            if response.status_code == 200:

                data = response.json()

                card_type = data.get(
                    "type_line",
                    "Unknown"
                )

        except Exception as e:

            card_type = f"ERROR: {e}"

        cards.append({
            "Quantity": qty,
            "Card": name,
            "Type": card_type,
            "Status": status_code
        })

    df = pd.DataFrame(cards)

    st.subheader("Pool Summary")

    st.write(f"Unique cards: {len(cards)}")
    st.write(f"Total cards: {total_cards}")

    st.subheader("Parsed Cards")

    st.dataframe(df)
