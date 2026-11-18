import streamlit as st
import pandas as pd
from supabase import create_client

st.title("MTG Limited Advisor")

uploaded_file = st.file_uploader(
    "Upload 17Lands Ratings CSV",
    type=["csv"]
)

if uploaded_file:

    try:

        df = pd.read_csv(
            uploaded_file,
            on_bad_lines="skip"
        )

        column_map = {
            "Name": "card_name",
            "Color": "color",
            "Rarity": "rarity",
            "# Seen": "seen_count",
            "ALSA": "alsa",
            "# Picked": "picked_count",
            "ATA": "ata",
            "# GP": "games_played",
            "% GP": "gp_percent",
            "GP WR": "gp_wr",
            "# OH": "oh_count",
            "OH WR": "oh_wr",
            "# GD": "gd_count",
            "GD WR": "gd_wr",
            "# GIH": "gih_count",
            "GIH WR": "gih_wr",
            "# GNS": "gns_count",
            "GNS WR": "gns_wr",
            "IIH": "iih"
        }

        df = df.rename(columns=column_map)

        columns_to_keep = [
            "card_name",
            "color",
            "rarity",
            "seen_count",
            "alsa",
            "picked_count",
            "ata",
            "games_played",
            "gp_percent",
            "gp_wr",
            "oh_count",
            "oh_wr",
            "gd_count",
            "gd_wr",
            "gih_count",
            "gih_wr",
            "gns_count",
            "gns_wr",
            "iih"
        ]

        clean_df = df[columns_to_keep]

        st.success(
            
