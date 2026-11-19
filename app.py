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

        gih = r.get("gih_wr")

        try:
            gih_numeric = float(
                str(gih).replace("%", "")
            )
        except:
            gih_numeric = 0

        colors = m.get("colors", "")

        if colors:

            split_colors = colors.split(",")

            for c in split_colors:

                if c in color_cards:

                    color_cards[c].append({
                        "Card": card_name,
                        "GIH": gih_numeric
                    })

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

            "Creature": is_creature
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

    st.subheader(
        "Power By Color"
    )

    analysis_rows = []

    for color, card_list in color_cards.items():

        if len(card_list) == 0:
            continue

        s_tier = len(
            [x for x in card_list if x["GIH"] >= 60]
        )

        a_tier = len(
            [x for x in card_list if 58 <= x["GIH"] < 60]
        )

        b_tier = len(
            [x for x in card_list if 55 <= x["GIH"] < 58]
        )

        c_tier = len(
            [x for x in card_list if 52 <= x["GIH"] < 55]
        )

        d_tier = len(
            [x for x in card_list if x["GIH"] < 52]
        )

        playable = (
            s_tier +
            a_tier +
            b_tier
        )

        score = (
            s_tier * 10 +
            a_tier * 7 +
            b_tier * 4 +
            c_tier * 2
        )

        analysis_rows.append({

            "Color": color,

            "Score": score,

            "Playable":
                playable,

            "S >60":
                s_tier,

            "A 58-60":
                a_tier,

            "B 55-58":
                b_tier,

            "C 52-55":
                c_tier,

            "D <52":
                d_tier
        })

    analysis_df = pd.DataFrame(
        analysis_rows
    )

    analysis_df = analysis_df.sort_values(
        by="Score",
        ascending=False
    )

    st.dataframe(
        analysis_df,
        hide_index=True
    )

    st.subheader(
        "Top Cards By Color"
    )

    for color, card_list in color_cards.items():

        if len(card_list) == 0:
            continue

        st.markdown(
            f"### {color}"
        )

        temp = pd.DataFrame(
            card_list
        )

        temp = temp.sort_values(
            by="GIH",
            ascending=False
        )

        st.dataframe(
            temp.head(8),
            hide_index=True
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
