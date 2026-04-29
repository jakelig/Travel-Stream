import re

import requests
import streamlit as st


@st.cache_data(ttl=3600)
def _fetch_meta(url: str) -> dict:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    meta = {}
    for m in re.finditer(r'<meta property="og:(\w+)" content="([^"]*)"', resp.text):
        meta[m.group(1)] = m.group(2).replace("&amp;", "&")
    return meta


def render_listing(name: str, url: str) -> None:
    try:
        meta = _fetch_meta(url)
    except Exception:
        meta = {}
    with st.container(border=True):
        if "image" in meta:
            st.image(meta["image"], use_container_width=True)
        st.markdown(f"### {meta.get('title', name)}")
        if "description" in meta:
            st.markdown(meta["description"])
        st.link_button("View on Airbnb", url)
