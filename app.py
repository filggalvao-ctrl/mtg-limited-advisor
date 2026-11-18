import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(
    page_title="MTG Limited Advisor",
    page_icon="🧙"
)

st.title("MTG Limited Advisor")

pool_text = st.text_area(
    "Paste Pool",
    height=400
)

if st.button("Analyze Pool"):

    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]

    supabase = create_client(
        url,
        key
    )

    rows = []

    lines = pool_text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        parts = line.split(
            " ",
            1
        )

        if len(parts) != 2:
            continue

        card_name = parts[1]

        try:

            rating_result = (
                supabase
                .table("trk_ratings")
                .select("*")
                .eq(
                    "card_name",
                    card_name
                )
                .execute()
            )

            meta_result = (
                supabase
                .table("card_metadata")
                .select("*")
                .eq(
                    "card_name",
                    card_name
                )
                .execute()
            )

            rating = (
                rating_result.data[0]
                if rating_result.data
                else {}
            )

            meta = (
                meta_result.data[0]
                if meta_result.data
                else {}
            )

            rows.append({

                "Card":
                    card_name,

                "GIH WR":
                    rating.get(
                        "gih_wr",
                        ""
                    ),

                "Type":
                    meta.get(
                        "type_line",
                        ""
                    ),

                "Colors":
                    meta.get(
                        "colors",
                        ""
                    ),

                "Artifact":
                    meta.get(
                        "is_artifact",
                        False
                    ),

                "Legendary":
                    meta.get(
                        "is_legendary",
                        False
                    )

            })

        except Exception as e:

            st.error(
                f"{card_name}: {e}"
            )

    df = pd.DataFrame(rows)

    st.subheader(
        "Pool Analysis"
    )

    st.dataframe(df)
