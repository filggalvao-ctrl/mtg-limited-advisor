import streamlit as st

st.title("MTG Limited Advisor")

pool_text = st.text_area(
    "Paste Pool Here",
    height=400
)

if st.button("Analyze"):

    lines = pool_text.strip().split("\n")

    cards = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        cards.append(line)

    st.subheader("Pool Summary")

    st.write(f"Cards detected: {len(cards)}")

    st.subheader("Cards")

    for card in cards:
        st.write(card)
