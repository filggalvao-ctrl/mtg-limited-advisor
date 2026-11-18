import streamlit as st

st.set_page_config(
    page_title="MTG Limited Advisor",
    page_icon="🧙",
    layout="wide"
)

st.title("MTG Limited Advisor")

st.markdown(
    """
    Welcome to the MTG Limited Advisor project.

    Current Modules:

    - 17Lands Ratings Import
    - Scryfall Metadata Import
    - Pool Analysis (coming soon)
    """
)

st.divider()

st.subheader("Project Status")

st.success(
    "17Lands ratings loaded into Supabase"
)

st.info(
    "336 card ratings stored in trk_ratings"
)

st.warning(
    "card_metadata still empty"
)
