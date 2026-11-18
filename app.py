import streamlit as st
import pandas as pd

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

        qty = int(parts[0])
        name = parts[1]

        total_cards += qty

        cards.append({
            "Quantity": qty,
            "Card": name
        })

    df = pd.DataFrame(cards)

    st.subheader("Pool Summary")

    st.write(f"Unique cards: {len(cards)}")

    st.write(f"Total cards: {total_cards}")

    st.subheader("Parsed Cards")

    st.dataframe(df)
