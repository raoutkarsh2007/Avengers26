import streamlit as st

from db import get_dealers, get_groups, get_quotes
from ui.components import render_empty_state, render_group_card, render_offer_card, render_section_heading, setup_page


setup_page("Dealer Portal")
city = st.session_state["selected_city"]
role = st.session_state.get("gcd_role", "Buyer")
render_section_heading("Dealer portal", "See local group demand without exposing buyer names.", "Dealer workspace")
if role != "Dealer":
    st.info("Switch the top-bar mode to Dealer to view this portal.")
else:
    st.caption("Buyer names and personal details are private. This page shows only group city, member counts, and quote records.")
    dealers = get_dealers()
    if not dealers:
        render_empty_state("No dealership records", "Add an actual dealership record before using the portal.")
    else:
        dealer_by_name = {dealer["name"]: dealer for dealer in dealers}
        selected_name = st.selectbox("Dealership", list(dealer_by_name))
        selected_dealer = dealer_by_name[selected_name]
        st.markdown(f"### Groups in {city}")
        groups = get_groups(city)
        if groups:
            for group in groups:
                render_group_card(group, can_join=False)
        else:
            render_empty_state("No group records for this city", "Group cards appear when buyers create them.")

        st.markdown("### Your saved quotes")
        saved_quotes = []
        for group in groups:
            saved_quotes.extend(
                quote
                for quote in get_quotes(group["id"])
                if quote["dealer_id"] == selected_dealer["id"]
            )
        if saved_quotes:
            quote_columns = st.columns(min(len(saved_quotes), 3))
            for column, quote in zip(quote_columns, saved_quotes):
                with column:
                    render_offer_card(quote)
        else:
            render_empty_state("No quotes from this dealership in this city", "A saved quote will appear here after submission.")
        st.page_link("pages/4_Dealer_Offers.py", label="Submit or update a dealer quote")
