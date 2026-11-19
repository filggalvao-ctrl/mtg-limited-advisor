import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(
    page_title="MTG Limited Advisor",
    page_icon="🧙",
    layout="wide"
)

st.title("MTG Limited Advisor")

pool_text = st.text_area(
    "Paste Pool",
    height=400
)

COLOR_NAMES = {
    "W": "⚪ White",
    "U": "🔵 Blue",
    "B": "⚫ Black",
    "R": "🔴 Red",
    "G": "🟢 Green"
}


def get_tier(gih):

    try:

        v = float(
            str(gih).replace(
                "%",
                ""
            )
        )

        if v >= 60:
            return "S"

        if v >= 58:
            return "A"

        if v >= 55:
            return "B"

        if v >= 52:
            return "C"

        return "D"

    except:

        return "D"


def tier_score(tier):

    scores = {
        "S": 5,
        "A": 3,
        "B": 2,
        "C": 1,
        "D": 0
    }

    return scores.get(
        tier,
        0
    )


if st.button("Analyze Pool"):

    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

    color_cards = {
        "W": [],
        "U": [],
        "B": [],
        "R": [],
        "G": []
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

        card_name = parts[1]

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

        metadata = (
            meta_result.data[0]
            if meta_result.data
            else {}
        )

        gih = rating.get(
            "gih_wr",
            0
        )

        try:

            gih_num = float(
                str(gih).replace(
                    "%",
                    ""
                )
            )

        except:

            gih_num = 0

        tier = get_tier(
            gih_num
        )

        colors = metadata.get(
            "colors",
            ""
        )

        card_data = {

            "Card":
                card_name,

            "GIH":
                gih_num,

            "Tier":
                tier
        }

        if colors:

            split_colors = colors.split(",")

            for color in split_colors:

                if color in color_cards:

                    color_cards[
                        color
                    ].append(
                        card_data
                    )

    st.header(
        "Pool Power Map"
    )

    summary_rows = []

    for color, cards in color_cards.items():

        s = len(
            [
                c
                for c in cards
                if c["Tier"] == "S"
            ]
        )

        a = len(
            [
                c
                for c in cards
                if c["Tier"] == "A"
            ]
        )

        b = len(
            [
                c
                for c in cards
                if c["Tier"] == "B"
            ]
        )

        power_score = sum(
            tier_score(
                c["Tier"]
            )
            for c in cards
        )

        premium_count = (
            s + a + b
        )

        summary_rows.append({

            "Color":
                COLOR_NAMES[
                    color
                ],

            "Premium":
                premium_count,

            "Power Score":
                power_score,

            "S":
                s,

            "A":
                a,

            "B":
                b
        })

    summary_df = pd.DataFrame(
        summary_rows
    )

    summary_df = summary_df.sort_values(
        by="Power Score",
        ascending=False
    )

    st.dataframe(
        summary_df,
        hide_index=True
    )

    st.header(
        "Top Cards By Color"
    )

    for color, cards in color_cards.items():

        if len(cards) == 0:
            continue

        color_df = pd.DataFrame(
            cards
        )

        color_df = color_df.sort_values(
            by="GIH",
            ascending=False
        )

        color_df = color_df[
            color_df["Tier"] != "D"
        ]

        if len(color_df) == 0:
            continue

        st.subheader(
            COLOR_NAMES[color]
        )

        st.dataframe(
            color_df,
            hide_index=True,
            use_container_width=True
        )
