from datetime import datetime

import streamlit as st

from db import get_dealers, get_groups, get_quotes, save_quote
from ui.components import render_empty_state, render_offer_card, render_section_heading, setup_page


setup_page("Dealer Offers")
city = st.session_state["selected_city"]
role = st.session_state.get("gcd_role", "Buyer")
render_section_heading("Dealer offers", "Compare what is included before comparing totals.", "No quote is a promise of availability")

groups = get_groups(city)
if not groups:
    render_empty_state("No groups or offers in this city", "Start a group first. Dealer quotes will appear when the database contains them.")
else:
    group_labels = {f"{group['make']} {group['model']} · {group.get('variant_name') or 'Variant unavailable'} · {group['name']}": group for group in groups}
    remembered = st.session_state.get("selected_group_id")
    default_label = next((label for label, group in group_labels.items() if group["id"] == remembered), next(iter(group_labels)))
    group_label = st.selectbox("Choose a group", list(group_labels), index=list(group_labels).index(default_label))
    selected_group = group_labels[group_label]
    quotes = get_quotes(selected_group["id"])
    if quotes:
        quote_columns = st.columns(min(len(quotes), 3))
        for column, quote in zip(quote_columns, quotes):
            with column:
                render_offer_card(quote)
    else:
        render_empty_state("No dealer quotes yet", "The quote area will fill when a dealer submits an itemized offer.")

    if role == "Dealer":
        st.markdown("### Submit an itemized quote")
        dealers = get_dealers()
        if dealers:
            dealer_names = {dealer["name"]: dealer["id"] for dealer in dealers}
            st.info("This demo portal does not verify dealership identity. New submissions are labeled unverified.")
            with st.form("dealer_quote_form"):
                dealer_name = st.selectbox("Dealership", list(dealer_names))
                price_cols = st.columns(3)
                ex_showroom = price_cols[0].number_input("Ex-showroom", min_value=0.0, step=10000.0)
                discount = price_cols[1].number_input("Discount", min_value=0.0, step=1000.0)
                rto = price_cols[2].number_input("RTO / registration", min_value=0.0, step=1000.0)
                charge_cols = st.columns(3)
                insurance = charge_cols[0].number_input("Insurance", min_value=0.0, step=1000.0)
                accessories = charge_cols[1].number_input("Accessories", min_value=0.0, step=1000.0)
                other_charges = charge_cols[2].number_input("Other charges", min_value=0.0, step=1000.0)
                delivery_days = st.number_input("Delivery estimate in days (optional; use 0 if unknown)", min_value=0, step=1)
                valid_until = st.text_input("Quote valid until (optional, YYYY-MM-DD)")
                addons_text = st.text_input("Optional add-ons (separate with commas)")
                submitted = st.form_submit_button("Submit unverified quote")
            if submitted:
                date_ok = True
                normalized_date = None
                if valid_until.strip():
                    try:
                        normalized_date = datetime.strptime(valid_until.strip(), "%Y-%m-%d").date().isoformat()
                    except ValueError:
                        date_ok = False
                        st.error("Use YYYY-MM-DD for the validity date, or leave it blank.")
                if ex_showroom <= 0:
                    st.error("Ex-showroom price must be greater than zero.")
                elif discount > ex_showroom:
                    st.error("Discount cannot be greater than ex-showroom price.")
                elif date_ok:
                    save_quote(
                        selected_group["id"],
                        dealer_names[dealer_name],
                        ex_showroom,
                        discount,
                        insurance,
                        rto,
                        accessories,
                        other_charges,
                        source_type="Dealer submission",
                        is_verified=False,
                        delivery_estimate_days=delivery_days or None,
                        valid_until=normalized_date,
                        optional_addons=[value.strip() for value in addons_text.split(",") if value.strip()],
                    )
                    st.success("Quote saved and clearly marked as an unverified dealer submission.")
        else:
            st.warning("No dealership records are available in the local database.")
    else:
        st.caption("Dealer quote entry is available in Dealer mode. Demo offers are not verified offers.")
