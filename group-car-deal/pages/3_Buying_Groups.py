from datetime import date, datetime

import streamlit as st

from db import add_buyer, create_group, get_cars, get_groups
from ui.components import render_live_groups, render_section_heading, setup_page
from ui.data import flatten_variants


setup_page("Buying Groups")
city = st.session_state["selected_city"]
role = st.session_state.get("gcd_role", "Buyer")
render_section_heading(f"Buying groups in {city}", "See real saved member counts. Joining a group is not a commitment to buy.", "Together, with no pressure")
render_live_groups(city)

if role == "Buyer":
    st.markdown("### Join a group")
    city_groups = get_groups(city)
    if city_groups:
        group_labels = {f"{group['make']} {group['model']} · {group.get('variant_name') or 'Variant unavailable'} · {group['name']}": group for group in city_groups}
        remembered_group = st.session_state.get("selected_group_id")
        group_labels_list = list(group_labels)
        default_group = next((label for label, group in group_labels.items() if group["id"] == remembered_group), group_labels_list[0])
        with st.form("join_group_form"):
            group_label = st.selectbox("Choose a group", group_labels_list, index=group_labels_list.index(default_group))
            buyer_name = st.text_input("Your name or nickname")
            joined = st.form_submit_button("Join group")
        if joined:
            if not buyer_name.strip():
                st.error("Enter a name or nickname first.")
            elif add_buyer(group_labels[group_label]["id"], buyer_name):
                st.success("You joined the group. This does not commit you to buying the car.")
            else:
                st.info("That name is already in this group. Joining is not a commitment to buy.")
    else:
        st.info("There are no groups in this city yet. You can start one below.")

    st.markdown("### Start a group")
    cars = get_cars()
    rows = flatten_variants(cars)
    variant_labels = {
        f"{row['car'].get('brand') or row['car'].get('make')} {row['car']['model']} · {row['variant'].get('name') or 'Unavailable'}": row
        for row in rows
    }
    preferred = st.session_state.get("preferred_variant")
    preferred_label = next(
        (label for label, row in variant_labels.items() if preferred and row["key"] == preferred["key"]),
        next(iter(variant_labels), None),
    )
    if variant_labels:
        with st.form("start_group_form"):
            variant_label = st.selectbox("Car and exact variant", list(variant_labels), index=list(variant_labels).index(preferred_label))
            group_name = st.text_input("Group name", value=f"{city} car buyers")
            target_size = st.number_input("Group target", min_value=2, max_value=100, value=10, step=1)
            deadline_text = st.text_input("Offer deadline (optional, YYYY-MM-DD)", placeholder="Leave blank if unknown")
            starter_name = st.text_input("Your name or nickname")
            started = st.form_submit_button("Start group")
        if started:
            selected_row = variant_labels[variant_label]
            if not group_name.strip() or not starter_name.strip():
                st.error("Add a group name and your name or nickname.")
            else:
                deadline = None
                if deadline_text.strip():
                    try:
                        deadline = datetime.strptime(deadline_text.strip(), "%Y-%m-%d").date().isoformat()
                    except ValueError:
                        st.error("Write the deadline as YYYY-MM-DD, or leave it blank.")
                if not deadline_text.strip() or deadline:
                    group_id = create_group(
                        selected_row["car"]["id"],
                        group_name.strip(),
                        selected_row["variant"].get("name"),
                        city,
                        int(target_size),
                        deadline,
                    )
                    add_buyer(group_id, starter_name)
                    st.success("Your group is open. Starting or joining never commits anyone to buying.")
else:
    st.info("Dealer view shows group city and member counts only. Buyer names stay private.")
