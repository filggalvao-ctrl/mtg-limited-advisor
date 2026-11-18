import streamlit as st
import pandas as pd
import requests
from supabase import create_client

st.title("Star Trek Metadata Importer")

if st.button("Load TRK Set"):

    cards = []

    next_url = (
        "https://api.scryfall.com/cards/search?q=set%3Atrk"
    )

    while next_url:

        response = requests.get(
            next_url,
            headers={
                "User-Agent":
                "mtg-limited-advisor"
            }
        )

        data = response.json()

        for card in data["data"]:

            type_line = card.get(
                "type_line",
                ""
            )

            cards.append({

                "card_name":
                    card.get("name"),

                "mana_cost":
                    card.get("mana_cost"),

                "mana_value":
                    card.get("cmc"),

                "colors":
                    ",".join(
                        card.get(
                            "colors",
                            []
                        )
                    ),

                "type_line":
                    type_line,

                "rarity":
                    card.get("rarity"),

                "power":
                    card.get("power"),

                "toughness":
                    card.get("toughness"),

                "oracle_text":
                    card.get("oracle_text"),

                "is_creature":
                    "Creature" in type_line,

                "is_artifact":
                    "Artifact" in type_line,

                "is_land":
                    "Land" in type_line,

                "is_legendary":
                    "Legendary" in type_line
            })

        if data.get("has_more"):
            next_url = data.get(
                "next_page"
            )
        else:
            next_url = None

    st.success(
        f"Found {len(cards)} cards"
    )

    st.dataframe(
        pd.DataFrame(cards).head(20)
    )

    st.session_state["cards"] = cards


if "cards" in st.session_state:

    if st.button(
        "Upload Metadata To Supabase"
    ):

        url = st.secrets[
            "SUPABASE_URL"
        ]

        key = st.secrets[
            "SUPABASE_KEY"
        ]

        supabase = create_client(
            url,
            key
        )

        cards = st.session_state[
            "cards"
        ]

        uploaded = 0

        batch_size = 25

        for i in range(
            0,
            len(cards),
            batch_size
        ):

            batch = cards[
                i:i + batch_size
            ]

            try:

                supabase.table(
                    "card_metadata"
                ).upsert(
                    batch
                ).execute()

                uploaded += len(
                    batch
                )

            except Exception as e:

                st.error(
                    f"Upload failed: {e}"
                )

                st.write(
                    batch[0]
                )

                st.stop()

        st.success(
            f"Successfully uploaded {uploaded} cards"
        )
