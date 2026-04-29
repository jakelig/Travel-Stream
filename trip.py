import streamlit as st

st.set_page_config(page_title="Washington State", page_icon="🧛‍♂️", layout="centered")
pg = st.navigation([
    st.Page("pages/trip_overview.py", title="Trip Overview 🧛‍♂️"),
    st.Page("pages/packing_list.py", title="Packing List 🎒")
])
pg.run()
