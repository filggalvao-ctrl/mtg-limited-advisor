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

    color_scores = {
        "W": 0,
        "U": 0,
        "B": 0,
        "R": 0,
        "G": 0
    }

    for line in pool_text.split("\n"):

        line = line.strip()

        if not line:
            continue

        parts = line.split(
            " ",
            1
        )

        if len(parts) != 2:
            continue

        qty = int(parts[0])

        card_name = parts[1]

        rating = (
            supabase
            .table("trk_ratings")
            .select("*")
            .eq(
                "card_name",
                card_name
            )
            .execute()
        )

        metadata = (
            supabase
            .table("card_metadata")
            .select("*")
            .eq(
                "card_name",
                card_name
            )
            .execute()
        )

        r = (
            rating.data[0]
            if rating.data
            else {}
        )

        m = (
            metadata.data[0]
            if metadata.data
            else {}
        )

        gih = r.get(
            "gih_wr",
            ""
        )

        try:

            gih_numeric = float(
                str(gih).replace(
                    "%",
                    ""
                )
            )

        except:

            gih_numeric = 0

        colors = m.get(
            "colors",
            ""
        )

        if colors:

            split_colors = colors.split(",")

            for c in split_colors:

                if c in color_scores:

                    color_scores[c] += (
                        gih_numeric * qty
                    )

        is_artifact = bool(
            m.get(
                "is_artifact",
                False
            )
        )

        is_legendary = bool(
            m.get(
                "is_legendary",
                False
            )
        )

        is_creature = bool(
            m.get(
                "is_creature",
                False
            )
        )

        if is_artifact:
            artifact_count += qty

        if is_legendary:
            legendary_count += qty

        if is_creature:
            creature_count += qty

        bomb = gih_numeric >= 60

        cards.append({

            "Quantity": qty,

            "Card": card_name,

            "GIH WR": gih,

            "GIH Numeric": gih_numeric,

            "Colors": colors,

            "Type": m.get(
                "type_line",
                ""
            ),

            "Artifact": is_artifact,

            "Legendary": is_legendary,

            "Creature": is_creature,

            "Bomb": bomb
        })

    df = pd.DataFrame(cards)

    df = df.sort_values(
        by="GIH Numeric",
        ascending=False
    )

    st.subheader("Pool Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Artifacts",
        artifact_count
    )

    c2.metric(
        "Legendaries",
        legendary_count
    )

    c3.metric(
        "Creatures",
        creature_count
    )

    st.subheader("Color Strength")

    color_df = pd.DataFrame(
        [
            {
                "Color": k,
                "Score": round(v, 1)
            }
            for k, v
            in color_scores.items()
        ]
    )

    color_df = color_df.sort_values(
        by="Score",
        ascending=False
    )

    st.dataframe(
        color_df,
        hide_index=True
    )

    st.subheader("Potential Bombs")

    bombs = df[
        df["Bomb"] == True
    ][[
        "Card",
        "GIH WR",
        "Colors"
    ]]

    if len(bombs) > 0:

        st.dataframe(
            bombs,
            hide_index=True
        )

    else:

        st.write(
            "No bombs detected."
        )

    st.subheader(
        "Best Cards By GIH WR"
    )

    st.dataframe(
        df.drop(
            columns=[
                "GIH Numeric"
            ]
        ),
        hide_index=True
    )
