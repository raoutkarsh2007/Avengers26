import streamlit as st

from db import get_cars
from ui.components import render_car_card, render_empty_state, render_section_heading, setup_page
from ui.data import flatten_variants, value_or_unavailable


setup_page("Explore Cars")
city = st.session_state["selected_city"]
cars = get_cars()
variants = flatten_variants(cars)

render_section_heading(
    "Explore the car catalog",
    "Search exact variants and narrow the list by the details that matter to you.",
    "Demo catalog",
)
st.caption("All cars and prices in this local catalog are demo data. City changes on-road estimates and group listings; the catalog does not claim local availability.")

makes = sorted({str(row["car"].get("brand") or row["car"].get("make") or "Unavailable") for row in variants})
filters = st.columns(4)
make = filters[0].selectbox("Make", ["All makes", *makes])
make_rows = [row for row in variants if make == "All makes" or (row["car"].get("brand") or row["car"].get("make")) == make]
models = sorted({str(row["car"].get("model") or "Unavailable") for row in make_rows})
model = filters[1].selectbox("Model", ["All models", *models])
model_rows = [row for row in make_rows if model == "All models" or row["car"].get("model") == model]
variant_names = sorted({str(row["variant"].get("name") or "Unavailable") for row in model_rows})
variant_name = filters[2].selectbox("Exact variant", ["All variants", *variant_names])
body_types = sorted({str(row["car"].get("body_type") or "Unavailable") for row in variants})
body_type = filters[3].selectbox("Body type", ["All body types", *body_types])

more_filters = st.columns(4)
fuels = sorted({str(row["variant"].get("fuel") or "Unavailable") for row in variants})
fuel = more_filters[0].selectbox("Fuel", ["All fuels", *fuels])
transmissions = sorted({str(row["variant"].get("transmission") or "Unavailable") for row in variants})
transmission = more_filters[1].selectbox("Transmission", ["All transmissions", *transmissions])
budget = more_filters[2].slider("Maximum ex-showroom budget", 0, 10000000, 10000000, step=100000, format="₹%d")
search = more_filters[3].text_input("Search make, model, or variant", key="explore_search", placeholder="For example: Nexon")

filtered = []
for row in variants:
    car = row["car"]
    item = row["variant"]
    search_text = " ".join(str(value or "") for value in (car.get("brand"), car.get("model"), item.get("name"))).lower()
    price = item.get("ex_showroom_price_inr")
    if body_type != "All body types" and (car.get("body_type") or "Unavailable") != body_type:
        continue
    if variant_name != "All variants" and (item.get("name") or "Unavailable") != variant_name:
        continue
    if fuel != "All fuels" and (item.get("fuel") or "Unavailable") != fuel:
        continue
    if transmission != "All transmissions" and (item.get("transmission") or "Unavailable") != transmission:
        continue
    if price is None and budget < 10000000:
        continue
    if price is not None and price > budget:
        continue
    if search.strip() and search.strip().lower() not in search_text:
        continue
    filtered.append(row)

st.caption(f"{len(filtered)} demo variant(s) match these filters.")
if not filtered:
    render_empty_state("No variants match", "Clear a filter or try a different search.")
else:
    for start in range(0, len(filtered), 3):
        rows = filtered[start : start + 3]
        columns = st.columns(len(rows))
        for column, row in zip(columns, rows):
            with column:
                variant_index = int(row["key"].split(":")[1])
                render_car_card(row["car"], row["variant"], city, variant_index)
