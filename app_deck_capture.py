import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="MTG Limited Advisor - Deck Capture",
    page_icon="📋",
    layout="wide"
)

st.title("MTG Limited Advisor - Deck Capture")

# --------------------------------------------------
# SUPABASE
# --------------------------------------------------

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def parse_card_list(text):
    """
    Converts:

    2 Kirk, Commanding Officer

    into

    {
        "Kirk, Commanding Officer": 2
    }

    Ignores:
    Deck
    Sideboard
    """

    cards = {}

    if not text:
        return cards

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        if line.lower() in [
            "deck",
            "sideboard"
        ]:
            continue

        parts = line.split(
            " ",
            1
        )

        if len(parts) != 2:
            continue

        try:

            qty = int(
                parts[0]
            )

        except:

            continue

        card_name = parts[1].strip()

        cards[card_name] = (
            cards.get(
                card_name,
                0
            )
            + qty
        )

    return cards


def calculate_deck_power(cards_dict):

    if not cards_dict:
        return 0

    total_power = 0

    for card_name, qty in cards_dict.items():

        result = (
            supabase
            .table("trk_ratings")
            .select(
                "gih_wr"
            )
            .eq(
                "card_name",
                card_name
            )
            .execute()
        )

        if not result.data:
            continue

        gih = result.data[0].get(
            "gih_wr"
        )

        try:

            gih_num = float(
                str(gih).replace(
                    "%",
                    ""
                )
            )

            total_power += (
                gih_num
                * qty
            )

        except:
            pass

    return round(
        total_power,
        1
    )


def generate_event_name():

    result = (
        supabase
        .table("deck_events")
        .select(
            "id"
        )
        .execute()
    )

    next_id = (
        len(result.data)
        + 1
    )

    return (
        f"Star Trek Sealed #{next_id:03d}"
    )

# --------------------------------------------------
# UI
# --------------------------------------------------

pool_text = st.text_area(
    "Pool",
    height=300
)

draftsim_text = st.text_area(
    "Draftsim Recommendation",
    height=300
)

player_text = st.text_area(
    "Player Final Deck",
    height=300
)

col1, col2 = st.columns(2)

with col1:

    wins = st.number_input(
        "Wins",
        min_value=0,
        max_value=7,
        value=0
    )

with col2:

    losses = st.number_input(
        "Losses",
        min_value=0,
        max_value=10,
        value=0
    )

draftsim_score = st.number_input(
    "Draftsim Score",
    min_value=0.0,
    max_value=10.0,
    value=0.0,
    step=0.1
)

notes = st.text_area(
    "Notes",
    height=150
)

# --------------------------------------------------
# PREVIEW
# --------------------------------------------------

if st.button(
    "Preview Event"
):

    pool_cards = parse_card_list(
        pool_text
    )

    draftsim_cards = parse_card_list(
        draftsim_text
    )

    player_cards = parse_card_list(
        player_text
    )

    draftsim_power = (
        calculate_deck_power(
            draftsim_cards
        )
    )

    player_power = (
        calculate_deck_power(
            player_cards
        )
    )

    st.subheader(
        "Power Comparison"
    )

    st.metric(
        "Draftsim Deck Power",
        draftsim_power
    )

    st.metric(
        "Player Deck Power",
        player_power
    )

    st.write(
        f"Pool Cards: {sum(pool_cards.values())}"
    )

    st.write(
        f"Draftsim Cards: {sum(draftsim_cards.values())}"
    )

    st.write(
        f"Player Cards: {sum(player_cards.values())}"
    )

# --------------------------------------------------
# SAVE EVENT
# --------------------------------------------------

if st.button(
    "Save Event"
):

    event_name = (
        generate_event_name()
    )

    pool_cards = parse_card_list(
        pool_text
    )

    draftsim_cards = parse_card_list(
        draftsim_text
    )

    player_cards = parse_card_list(
        player_text
    )

    draftsim_power = (
        calculate_deck_power(
            draftsim_cards
        )
    )

    player_power = (
        calculate_deck_power(
            player_cards
        )
    )

    try:

        # --------------------------------------
        # POOL
        # --------------------------------------

        pool_record = (
            supabase
            .table("pools")
            .insert({
                "pool_name":
                    event_name,
                "source":
                    "17lands",
                "pool_text":
                    pool_text
            })
            .execute()
        )

        pool_id = (
            pool_record
            .data[0]["id"]
        )

        # --------------------------------------
        # POOL CARDS
        # --------------------------------------

        pool_rows = []

        for card_name, qty in pool_cards.items():

            pool_rows.append({
                "pool_id":
                    pool_id,
                "card_name":
                    card_name,
                "quantity":
                    qty
            })

        if pool_rows:

            (
                supabase
                .table(
                    "pool_cards"
                )
                .insert(
                    pool_rows
                )
                .execute()
            )

        # --------------------------------------
        # EVENT
        # --------------------------------------

        event_record = (
            supabase
            .table(
                "deck_events"
            )
            .insert({
                "pool_id":
                    pool_id,
                "event_name":
                    event_name,
                "draftsim_score":
                    draftsim_score,
                "draftsim_deck_text":
                    draftsim_text,
                "player_deck_text":
                    player_text,
                "draftsim_deck_power":
                    draftsim_power,
                "player_deck_power":
                    player_power,
                "result_wins":
                    wins,
                "result_losses":
                    losses,
                "notes":
                    notes
            })
            .execute()
        )

        event_id = (
            event_record
            .data[0]["id"]
        )

        # --------------------------------------
        # DRAFTSIM CARDS
        # --------------------------------------

        draftsim_rows = []

        for card_name, qty in draftsim_cards.items():

            draftsim_rows.append({
                "deck_event_id":
                    event_id,
                "deck_type":
                    "draftsim",
                "card_name":
                    card_name,
                "quantity":
                    qty
            })

        if draftsim_rows:

            (
                supabase
                .table(
                    "deck_lists"
                )
                .insert(
                    draftsim_rows
                )
                .execute()
            )

        # --------------------------------------
        # PLAYER CARDS
        # --------------------------------------

        player_rows = []

        for card_name, qty in player_cards.items():

            player_rows.append({
                "deck_event_id":
                    event_id,
                "deck_type":
                    "player",
                "card_name":
                    card_name,
                "quantity":
                    qty
            })

        if player_rows:

            (
                supabase
                .table(
                    "deck_lists"
                )
                .insert(
                    player_rows
                )
                .execute()
            )

        st.success(
            f"{event_name} saved successfully"
        )

        st.write(
            f"Draftsim Power: {draftsim_power}"
        )

        st.write(
            f"Player Power: {player_power}"
        )

    except Exception as e:

        st.error(
            f"Error: {e}"
        )
