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
    "G": "🟢 Green",
    "ARTIFACT": "⚙️ Artifacts",
    "MULTI": "🌈 Multicolor"
}


def get_tier(gih):

    if gih is None:
        return "N/A"

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

        return "N/A"


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
        "G": [],
        "ARTIFACT": [],
        "MULTI": []
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

        raw_gih = rating.get(
            "gih_wr"
        )

        try:

            gih_num = float(
                str(raw_gih).replace(
                    "%",
                    ""
                )
            )

            gih_display = round(
                gih_num,
                1
            )

        except:

            gih_num = None
            gih_display = "N/A"

        tier = get_tier(
            raw_gih
        )

        colors = metadata.get(
            "colors",
            ""
        )

        entry = {
            "Card": card_name,
            "GIH": gih_display,
            "Tier": tier,
            "GIH_Num": gih_num
        }

        # ------------------------
        # CLASSIFICATION
        # ------------------------

        if not colors:

            color_cards[
                "ARTIFACT"
            ].append(
                entry
            )

        else:

            split_colors = [
                c.strip()
                for c in colors.split(",")
                if c.strip()
            ]

            if len(split_colors) > 1:

                color_cards[
                    "MULTI"
                ].append(
                    entry
                )

            else:

                single_color = split_colors[0]

                if single_color in color_cards:

                    color_cards[
                        single_color
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

        cards_df = pd.DataFrame(cards)

        cards_df["GIH_Sort"] = cards_df[
            "GIH_Num"
        ].fillna(-1)

        cards_df = cards_df.sort_values(
            by="GIH_Sort",
            ascending=False
        )

        premium_df = cards_df[
            cards_df["Tier"].isin(
                ["S", "A", "B"]
            )
        ]

        premium_count = len(
            premium_df
        )

        premium_strength = round(
            premium_df[
                "GIH_Sort"
            ].sum(),
            1
        )

        best_three = cards_df.head(3)

        top_cards = " | ".join(
            [
                f"{row['Card']} ({row['GIH']})"
                for _, row
                in best_three.iterrows()
            ]
        )

        summary_rows.append({

            "Color":
                COLOR_NAMES[
                    color
                ],

            "Premium":
                premium_count,

            "Premium Strength":
                premium_strength,

            "Best Cards":
                top_cards
        })

    summary_df = pd.DataFrame(
        summary_rows
    )

    summary_df = summary_df.sort_values(
        by="Premium Strength",
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

    ordered_colors = [
        "W",
        "U",
        "B",
        "R",
        "G",
        "ARTIFACT",
        "MULTI"
    ]

    cols = st.columns(7)

    for idx, color in enumerate(
        ordered_colors
    ):

        cards = color_cards[color]

        if len(cards) == 0:
            continue

        cards_df = pd.DataFrame(
            cards
        )

        cards_df["GIH_Sort"] = cards_df[
            "GIH_Num"
        ].fillna(-1)

        cards_df = cards_df.sort_values(
            by="GIH_Sort",
            ascending=False
        )

        premium_count = len(
            cards_df[
                cards_df["Tier"].isin(
                    ["S", "A", "B"]
                )
            ]
        )

        with cols[idx]:

            st.subheader(
                COLOR_NAMES[color]
            )

            st.metric(
                "Premium",
                premium_count
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
