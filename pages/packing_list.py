import polars as pl
import streamlit as st

from py.db import get_people, get_packing_list, sync_packing_list

st.title("Packing List 🎒", text_alignment="center")

try:
    people = get_people()
except Exception as e:
    st.error(f"Could not connect to database: {e}")
    st.stop()

if not people:
    st.info("No people found in packing_list table.")
    st.stop()

traveler = st.selectbox("Who's packing?", options=people)

try:
    records = get_packing_list(traveler)
except Exception as e:
    st.error(f"Could not load packing list: {e}")
    st.stop()

df = pl.DataFrame(records, schema={"item": pl.String, "packed": pl.Boolean})

edited = st.data_editor(
    df,
    column_config={
        "item": st.column_config.TextColumn("Item"),
        "packed": st.column_config.CheckboxColumn("Packed"),
    },
    num_rows="dynamic",
    hide_index=True,
    use_container_width=True,
)

if st.button("Save Changes", type="primary"):
    try:
        sync_packing_list(traveler, edited.to_dicts())
        st.success("Saved!")
    except Exception as e:
        st.error(f"Save failed: {e}")
