import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import date
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
            f"Loaded {len(clean_df)} cards"
        )

        st.subheader("Preview")

        st.dataframe(
            clean_df.head(10)
        )

        if st.button("Upload to Supabase"):

            url = st.secrets["SUPABASE_URL"]
            key = st.secrets["SUPABASE_KEY"]

            supabase = create_client(
                url,
                key
            )

            clean_df["snapshot_date"] = str(
                date.today()
            )

            # converter tudo para texto/objeto
            clean_df = clean_df.astype(object)

            # substituir NaN por None
            clean_df = clean_df.where(
                pd.notnull(clean_df),
                None
            )

            st.subheader("Missing Values Check")

            missing = clean_df.isna().sum()

            st.write(
                missing[missing > 0]
            )

            records = clean_df.to_dict(
                orient="records"
            )

            uploaded = 0
            batch_size = 25

            for i in range(
                0,
                len(records),
                batch_size
            ):

                batch = records[
                    i:i + batch_size
                ]

                try:

                    supabase.table(
                        "trk_ratings"
                    ).upsert(
                        batch,
                        on_conflict="card_name"
                    ).execute()

                    uploaded += len(batch)

                except Exception as e:

                    st.error(
                        f"Upload failed: {e}"
                    )

                    st.write(
                        "First record of failing batch:"
                    )

                    st.write(
                        batch[0]
                    )

                    st.stop()

            st.success(
                f"Successfully uploaded {uploaded} records"
            )

    except Exception as e:

        st.error(
            f"CSV Parsing Error: {e}"
        )
