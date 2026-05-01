import polars as pl
import streamlit as st

st.title("Meal Plan 🍔", text_alignment="center")

st.markdown(
    """
    ## Forks Night 1
      - Burgers w/ cheese, pickles, and tomatoes
      - Hotdogs
      - Beer

    ## Forks Night 2
      - Fajitas with:
        - Grilled mexican chicken
        - Grilled onions and peppers
        - Black beans
      - Chips & salsa

    ## Forks Night 3
      - Teriyaki marinated salmon
      - Mac and cheese
      - Corn on the cob or asparagus
    """
)