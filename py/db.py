import polars as pl
import streamlit as st
from supabase import Client, create_client


@st.cache_resource
def _client() -> Client:
    return create_client(
        st.secrets["supabase"]["url"],
        st.secrets["supabase"]["key"]
    )


@st.cache_data(ttl=60)
def get_people() -> list[str]:
    response = _client().table("packing_list").select("traveler").execute()
    return (
        pl.DataFrame(response.data, schema={"traveler": pl.String})
        .get_column("traveler")
        .unique()
        .sort()
        .to_list()
    )


@st.cache_data(ttl=60)
def get_packing_list(traveler: str) -> pl.DataFrame:
    response = (
        _client()
        .table("packing_list")
        .select("item, packed, traveler")
        .eq("traveler", traveler)
        .order("item")
        .execute()
    )
    return pl.DataFrame(response.data, schema={"item": pl.String, "packed": pl.Boolean})


def sync_packing_list(traveler: str, df: pl.DataFrame) -> None:
    df = df.filter(pl.col("item").str.strip_chars() != "")
    _client().table("packing_list").delete().eq("traveler", traveler).execute()
    if len(df) > 0:
        rows = df.with_columns(pl.lit(traveler).alias("traveler")).to_dicts()
        _client().table("packing_list").insert(rows).execute()
    get_packing_list.clear()
