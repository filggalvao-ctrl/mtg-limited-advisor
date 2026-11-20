import streamlit as st
import pandas as pd
from supabase import create_client
from itertools import combinations

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
    "COLORLESS": "⚙️ Colorless",
    "LANDS": "🏞️ Lands",
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
        "COLORLESS": [],
        "LANDS": [],
        "MULTI": []
    }

    pair_rewards = {}

    mono_strength = {
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
        try:
        
            quantity = int(
                parts[0]
            )
        
        except:

            quantity = 1
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
            "Qty": quantity,
            "GIH": gih_display,
            "Tier": tier,
            "GIH_Num": gih_num,
            "Colors": colors
        }

        if not colors:

            if metadata.get("is_land"):
                color_cards[
                    "LANDS"
                ].append(
                    entry
                )

            else:
                color_cards[
                    "COLORLESS"
                ].append(
                    entry
                )

        else:

            split_colors = [
                c.strip()
                for c in colors.split(",")
                if c.strip()
            ]

            # Multicolor
            if len(split_colors) > 1:

                color_cards[
                    "MULTI"
                ].append(
                    entry
                )
                if len(split_colors) == 2:
                    pair_key = ",".join(
                        sorted(
                            split_colors
                        )
                    )
    
                    if pair_key not in pair_rewards:
    
                        pair_rewards[
                            pair_key
                        ] = []
    
                    pair_rewards[
                        pair_key
                    ].append(
                        entry
                    )

            # Monocolor
            elif len(split_colors) == 1:

                color = split_colors[0]

                if color in color_cards:

                    color_cards[
                        color
                    ].append(
                        entry
                    )

                    if (
                        gih_num
                        is not None
                        and tier in [
                            "S",
                            "A",
                            "B"
                        ]
                    ):

                        mono_strength[
                            color
                        ] += gih_num

    # --------------------------------
    # POOL POWER OVERVIEW
    # --------------------------------

    st.header(
        "Pool Power Overview"
    )

    summary_rows = []

    for color, cards in color_cards.items():

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

        premium_df = cards_df[
            cards_df["Tier"].isin(
                ["S", "A", "B"]
            )
        ]

        premium_count = premium_df[
            "Qty"
        ].sum()

        premium_strength = round(
            (
                premium_df[
                    "GIH_Sort"
                ]   
                *
                premium_df[
                    "Qty"
                ]
            ).sum(),
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

    # --------------------------------
    # CANDIDATE COLOR PAIRS
    # --------------------------------

    st.header(
        "Candidate Color Pairs"
    )

    pair_rows = []

    for pair, cards in pair_rewards.items():

        c1, c2 = pair.split(",")

        reward_strength = 0

        premiums = 0

        for card in cards:

            if (
                card["GIH_Num"]
                is not None
                and card["Tier"] in [
                    "S",
                    "A",
                    "B"
                ]
            ):

                reward_strength += (
                    card["GIH_Num"]
                    *
                    card["Qty"]
                )

                premiums += (
                    card["Qty"]
                )

        total_score = (
            mono_strength.get(
                c1,
                0
            )
            +
            mono_strength.get(
                c2,
                0
            )
            +
            reward_strength
        )

        pair_rows.append({

            "Pair":
                pair,

            "Premiums":
                premiums,

            "Reward Strength":
                round(
                    reward_strength,
                    1
                ),

            "Total Pair Score":
                round(
                    total_score,
                    1
                ),

            "Key Cards":
                ", ".join(
                    [
                        c["Card"]
                        for c in cards
                    ]
                )
        })

    if pair_rows:

        pair_df = pd.DataFrame(
            pair_rows
        )

        pair_df = pair_df.sort_values(
            by="Total Pair Score",
            ascending=False
        )

        st.dataframe(
            pair_df,
            hide_index=True,
            use_container_width=True
        )

    # --------------------------------
    # MULTICOLOR REWARDS
    # --------------------------------

    st.header(
        "🌈 Multicolor Rewards"
    )

    reward_rows = []

    for pair, cards in pair_rewards.items():

        strength = 0

        premiums = 0

        for c in cards:

            if (
                c["Tier"]
                in ["S", "A", "B"]
            ):

                premiums += (
                    c["Qty"]
                )

                if c["GIH_Num"]:

                    strength += (
                        c["GIH_Num"]
                        *
                        c["Qty"]
                    )

        reward_rows.append({

            "Pair":
                pair,

            "Premiums":
                premiums,

            "Premium Strength":
                round(
                    strength,
                    1
                ),

            "Best Cards":
                ", ".join(
                    [
                        c["Card"]
                        for c in cards
                    ]
                )
        })

    reward_df = pd.DataFrame(
        reward_rows
    )

    reward_df = reward_df.sort_values(
        by="Premium Strength",
        ascending=False
    )

    st.dataframe(
        reward_df,
        hide_index=True,
        use_container_width=True
    )

    # --------------------------------
    # DETAILED COLOR BREAKDOWN
    # --------------------------------

    st.header(
        "Detailed Color Breakdown"
    )

    ordered_colors = [
        "W",
        "U",
        "B",
        "R",
        "G",
        "COLORLESS",
        "LANDS",
        "MULTI"
    ]

    cols = st.columns(8)

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

            if color == "MULTI":

                st.dataframe(
                    cards_df[
                        [
                            "Card",
                            "Colors",
                            "GIH",
                            "Tier"
                        ]
                    ],
                    hide_index=True,
                    use_container_width=True
                )

            else:

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
