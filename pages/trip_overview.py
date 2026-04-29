import polars as pl
import streamlit as st
import yaml

from py.airbnb import render_listing

st.title("Washington State 🧛‍♂️", text_alignment="center")

df = pl.read_csv("data/itinerary.csv").with_columns(
    (pl.col('day') + " - " + pl.col('date')).alias('day')
)

days_ordered = (
    df.select(["day_number", "day"])
    .unique()
    .sort("day_number")
    .get_column("day")
    .to_list()
)

st.subheader("Itinerary")
selected_day = st.selectbox("Select a day", options=days_ordered, index=0)

day_df = (
    df.filter(pl.col("day") == selected_day)
    .sort("event_num")
    .select(["event", "time", "apple_maps", "website"])
    .rename({
        "event": "Event",
        "time": "Time",
        "apple_maps": "Apple Maps",
        "website": "Website",
    })
)

st.dataframe(
    day_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Apple Maps": st.column_config.LinkColumn(
            "Apple Maps",
            display_text="Navigate",
        ),
        "Website": st.column_config.LinkColumn(
            "Website",
            display_text=None,
        ),
    },
)

with open("data/details.yaml") as f:
    details = yaml.safe_load(f)

st.subheader("Airbnbs")
airbnbs = details["airbnbs"]
tabs = st.tabs(list(airbnbs.keys()))
for tab, (name, url) in zip(tabs, airbnbs.items()):
    with tab:
        render_listing(name, url)

st.subheader("Trip Tracklist")
st.iframe("embed/playlist.html")
