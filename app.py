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

def get_tier(gih):

    try:
        v = float(str(gih).replace("%", ""))

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

if st.button("Analyze Pool"):

    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

    pool_cards = []

    color_summary = {
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

        rating_result = (
            supabase
            .table("trk_ratings")
            .select("*")
            .eq("card_name", card_name)
            .execute()
        )

        meta_result = (
            supabase
            .table("card_metadata")
            .select("*")
            .eq("card_name", card_name)
            .execute()
        )

        r = (
            rating_result.data[0]
            if rating_result.data
            else {}
        )

        m = (
            meta_result.data[0]
            if meta_result.data
            else {}
        )

        gih = r.get(
            "gih_wr",
            0
        )

        try:
            gih_numeric = float(
                str(gih).replace("%", "")
            )
        except:
            gih_numeric = 0

        colors = m.get(
            "colors",
            ""
        )

        tier = get_tier(gih)

        card_entry = {
            "Card": card_name,
            "GIH": gih_numeric,
            "Tier": tier
        }

        if colors:

            for c in colors.split(","):

                if c in color_summary:

                    color_summary[c].append(
                        card_entry
                    )

        pool_cards.append({
            "Card": card_name,
            "GIH": gih_numeric,
            "Tier": tier,
            "Colors": colors
        })

    st.header("Color Power Map")

    summary_rows = []

    for color, cards in color_summary.items():

        s = len([x for x in cards if x["Tier"] == "S"])
        a = len([x for x in cards if x["Tier"] == "A"])
        b = len([x for x in cards if x["Tier"] == "B"])
        c = len([x for x in cards if x["Tier"] == "C"])
        d = len([x for x in cards if x["Tier"] == "D"])

        summary_rows.append({
            "Color": color,
            "Cards": len(cards),
            "S": s,
            "A": a,
            "B": b,
            "C": c,
            "D": d
        })

    summary_df = pd.DataFrame(
        summary_rows
    )

    st.dataframe(
        summary_df,
        hide_index=True
    )

    st.header("Best Cards By Color")

    color_names = {
        "W": "White",
        "U": "Blue",
        "B": "Black",
        "R": "Red",
        "G": "Green"
    }

    for color, cards in color_summary.items():

        if len(cards) == 0:
            continue

        st.subheader(
            color_names[color]
        )

        color_df = pd.DataFrame(cards)

        color_df = color_df.sort_values(
            by="GIH",
            ascending=False
        )

        st.dataframe(
            color_df,
            hide_index=True
        )
