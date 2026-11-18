import streamlit as st
import pandas as pd

st.title("MTG Limited Advisor")

uploaded_file = st.file_uploader(
    "Upload card-ratings CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(
        uploaded_file,
        on_bad_lines="skip"
    )

    column_map = {
        "Name": "card_name",
        "Color": "color",
        "Rarity": "rarity",
        "# GP": "games_played",
        "% GP": "gp_percent",
        "GP WR": "gp_wr",
        "GIH WR": "gih_wr",
        "GNS WR": "gns_wr",
        "IIH": "iih"
    }

    df = df.rename(columns=column_map)

    columns_to_keep = [
        "card_name",
        "color",
        "rarity",
        "games_played",
        "gp_percent",
        "gp_wr",
        "gih_wr",
        "gns_wr",
        "iih"
    ]

    clean_df = df[columns_to_keep]

    st.success(
        f"Loaded {len(clean_df)} cards"
    )

    st.subheader("Clean Ratings Table")

    st.dataframe(clean_df)
