import streamlit as st
import pandas as pd

st.title("MTG Limited Advisor")

st.subheader("17Lands CSV Inspector")

uploaded_file = st.file_uploader(
    "Upload card-ratings CSV",
    type=["csv"]
)

if uploaded_file:

    try:

        df = pd.read_csv(
            uploaded_file,
            on_bad_lines="skip"
        )

        st.success(
            f"Loaded {len(df)} rows"
        )

        st.subheader("Detected Columns")

        st.write(df.columns.tolist())

        st.subheader("Preview")

        st.dataframe(df.head(20))

    except Exception as e:

        st.error(str(e))
