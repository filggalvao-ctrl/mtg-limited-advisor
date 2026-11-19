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

        score = float(
            str(gih).replace(
                "%",
                ""
            )
        )

        if score >= 60:
            return "S"

        if score >= 58:
            return "A"

        if score >= 55:
            return "B"

        if score >= 52:
            return "C"

        return "D"

    except:

        return "D"


def premium_count(cards):

    count = 0

    for card in cards:

        if card["Tier"] in [
            "S",
            "A",
            "B"
        ]:
            count += 1

    return count


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

        entry = {

            "Card":
                card_name,

            "GIH":
                gih_num,

            "Tier":
                tier
        }

        if colors:

            for color in colors.split(","):

                if color in color_cards:

                    color_cards[
                        color
                    ].append(
                        entry
                    )

    st.header(
        "Pool Power Overview"
    )

    summary_rows = []

    for color, cards in color_cards.items():

        if len(cards) == 0:
            continue

        cards_sorted = sorted(
            cards,
            key=lambda x: x["GIH"],
            reverse=True
        )

        best_three = cards_sorted[:3]

        top_cards = " | ".join(
            [
                f"{c['Card']} ({c['GIH']:.1f})"
                for c in best_three
            ]
        )

        summary_rows.append({
            "Color":
                COLOR_NAMES[color],

            "Premium":
                premium_count(cards),

            "Best Cards":
                top_cards
        })

    summary_df = pd.DataFrame(
        summary_rows
    )

    summary_df = summary_df.sort_values(
        by="Premium",
        ascending=False
    )

    st.dataframe(
        summary_df,
        hide_index=True,
        use_container_width=True
    )

    st.header(
        "Detailed Color Breakdown"
    )

    cols = st.columns(5)

    ordered_colors = [
        "W",
        "U",
        "B",
        "R",
        "G"
    ]

    for idx, color in enumerate(
        ordered_colors
    ):

        cards = color_cards[color]

        if len(cards) == 0:
            continue

        cards_df = pd.DataFrame(
            cards
        )

        cards_df = cards_df.sort_values(
            by="GIH",
            ascending=False
        )

        cards_df = cards_df[
            cards_df["Tier"] != "D"
        ]

        with cols[idx]:

            st.subheader(
                COLOR_NAMES[color]
            )

            st.metric(
                "Premium",
                premium_count(
                    cards
                )
            )

            st.dataframe(
                cards_df[
                    [
                        "Card",
                        "GIH",
                        "Tier"
                    ]
                ],
                hide_index=True,
                use_container_width=True
            )
