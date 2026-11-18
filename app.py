import streamlit as st
import pandas as pd
from supabase import create_client

st.title("MTG Limited Advisor")

uploaded_file = st.file_uploader(
    "Upload 17Lands Ratings CSV",
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

    clean_df = df[list(column_map.values())]

    st.success(
        f"Loaded {len(clean_df)} cards"
    )

    st.dataframe(clean_df.head(10))

    if st.button("Upload to Supabase"):

        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]

        supabase = create_client(url, key)

        clean_df["snapshot_date"] = "2026-11-18"

        records = clean_df.to_dict(
            orient="records"
        )

        batch_size = 50

        total_uploaded = 0

        for i in range(
            0,
            len(records),
            batch_size
        ):

            batch = records[i:i + batch_size]

            supabase.table(
                "trk_ratings"
            ).insert(batch).execute()

            total_uploaded += len(batch)

        st.success(
            f"Uploaded {total_uploaded} cards"
        )
