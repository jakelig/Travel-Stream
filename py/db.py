import streamlit as st
from sqlalchemy import create_engine, text


@st.cache_resource
def _engine():
    return create_engine(
        st.secrets["supabase"]["connection_string"],
        pool_pre_ping=True,
    )


@st.cache_data(ttl=60)
def get_people() -> list[str]:
    with _engine().connect() as conn:
        result = conn.execute(
            text("select distinct traveler from packing_list order by traveler")
        )
        return [r[0] for r in result]


@st.cache_data(ttl=60)
def get_packing_list(traveler: str) -> list[dict]:
    with _engine().connect() as conn:
        result = conn.execute(
            text(
                """
                select  item, packed from packing_list
                where traveler = :traveler order by item
                """
            ),
            {"traveler": traveler},
        )
        return [{"item": r[0], "packed": bool(r[1])} for r in result]


def sync_packing_list(traveler: str, rows: list[dict]) -> None:
    rows = [r for r in rows if r.get("item", "").strip()]
    with _engine().begin() as conn:
        conn.execute(
            text("delete from packing_list where traveler = :traveler"),
            {"traveler": traveler},
        )
        if rows:
            conn.execute(
                text(
                    """
                    insert into packing_list (item, traveler, packed)
                    values (:item, :traveler, :packed)
                    """
                ),
                [{"item": r["item"], "traveler": traveler, "packed": r["packed"]} for r in rows],
            )
    get_packing_list.clear()
