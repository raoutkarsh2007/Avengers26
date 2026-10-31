import streamlit as st

from db import get_cars
from ui.components import render_empty_state, render_section_heading, render_comparison_tray, setup_page
from ui.data import comparison_item, estimate_for_city, flatten_variants, value_or_unavailable


setup_page("Compare")
city = st.session_state["selected_city"]
render_section_heading("Compare exact variants", "Select two to four cars and scan their differences in one place.", "Comparison")

variants = flatten_variants(get_cars())
labels = {
    f"{row['car'].get('brand') or row['car'].get('make')} {row['car']['model']} · {row['variant'].get('name') or 'Unavailable'}": row
    for row in variants
}
if labels:
    picker_col, button_col = st.columns([4, 1])
    picked = picker_col.selectbox("Choose a car variant", list(labels), key="compare_picker")
    if button_col.button("Add to compare", width="stretch", type="primary"):
        row = labels[picked]
        index = int(row["key"].split(":")[1])
        item = comparison_item(row["car"], row["variant"], index)
        selected = st.session_state.setdefault("compare_variants", [])
        if any(existing["key"] == item["key"] for existing in selected):
            st.info("That exact variant is already selected.")
        elif len(selected) >= 4:
            st.warning("The tray holds up to four variants.")
        else:
            selected.append(item)
            st.rerun()

selected = st.session_state.get("compare_variants", [])
if len(selected) < 2:
    render_empty_state("Pick at least two variants", "Use the selector above or choose Compare on a car card.")
else:
    st.caption("Demo catalog data. An on-road figure is an estimate based on your selected city and the editable state rates.")
    headers = [f"{item['brand']} {item['model']}\n{item['variant']}" for item in selected]
    specs = [
        ("Body type", "body_type"),
        ("Fuel", "fuel"),
        ("Transmission", "transmission"),
        ("Seats", "seating"),
        ("Boot space (L)", "boot_space_l"),
        ("Mileage / range", "mileage_or_ev_range"),
        ("Engine / power / torque", "engine_power_torque"),
        ("Battery / motor", "battery_motor"),
        ("Safety rating", "safety_rating"),
        ("Key features", "key_features"),
        ("Data source", "data_source"),
    ]
    rows = []
    for label, field in specs:
        row = {"Specification": label}
        for header, item in zip(headers, selected):
            value = item.get(field)
            if field == "key_features":
                value = ", ".join(value or []) or None
            if field == "data_source" and value == "sample":
                value = "Demo data"
            row[header] = value_or_unavailable(value)
        rows.append(row)
    for price_label, price_fn in (
        ("Ex-showroom", lambda item: item.get("ex_showroom_price_inr")),
        ("Indicative on-road estimate", lambda item: estimate_for_city(item.get("ex_showroom_price_inr"), city)),
    ):
        row = {"Price (demo)": price_label}
        for header, item in zip(headers, selected):
            value = price_fn(item)
            row[header] = f"₹{value:,.0f}" if value is not None else "Unavailable"
        rows.append(row)
    st.dataframe(rows, hide_index=True, width="stretch")
    st.caption("No prices are calculated by AI. On-road estimates are calculated in pricing.py.")
