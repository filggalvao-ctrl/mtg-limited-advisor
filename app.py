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

    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

    cards = []

    artifact_count = 0
    legendary_count = 0
    creature_count = 0

    for line in pool_text.split("\n"):

        line = line.strip()

        if not line:
            continue

        parts = line.split(" ", 1)

        if len(parts) != 2:
            continue

        qty = int(parts[0])
        card_name = parts[1]

        rating = (
            supabase
            .table("trk_ratings")
            .select("*")
            .eq("card_name", card_name)
            .execute()
        )

        metadata = (
            supabase
            .table("card_metadata")
            .select("*")
            .eq("card_name", card_name)
            .execute()
        )

        r = rating.data[0] if rating.data else {}
        m = metadata.data[0] if metadata.data else {}

        is_artifact = bool(
            m.get("is_artifact", False)
        )

        is_legendary = bool(
            m.get("is_legendary", False)
        )

        is_creature = bool(
            m.get("is_creature", False)
        )

        if is_artifact:
            artifact_count += qty

        if is_legendary:
            legendary_count += qty

        if is_creature:
            creature_count += qty

        gih = r.get("gih_wr")

        try:
            gih_numeric = float(
                str(gih).replace("%", "")
            )
        except:
            gih_numeric = 0

        cards.append({

            "Quantity": qty,

            "Card": card_name,

            "GIH WR":
                gih,

            "GIH Numeric":
                gih_numeric,

            "Colors":
                m.get(
                    "colors",
                    ""
                ),

            "Type":
                m.get(
                    "type_line",
                    ""
                ),

            "Artifact":
                is_artifact,

            "Legendary":
                is_legendary,

            "Creature":
                is_creature
        })

    df = pd.DataFrame(cards)

    df = df.sort_values(
        by="GIH Numeric",
        ascending=False
    )

    st.subheader("Pool Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Artifacts",
        artifact_count
    )

    col2.metric(
        "Legendaries",
        legendary_count
    )

    col3.metric(
        "Creatures",
        creature_count
    )

    st.subheader(
        "Best Cards By GIH WR"
    )

    st.dataframe(
        df.drop(
            columns=["GIH Numeric"]
        )
    )
