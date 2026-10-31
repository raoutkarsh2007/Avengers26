import streamlit as st

from db import get_cars, get_dealers, get_groups, get_quotes
from ui.components import render_section_heading, setup_page
from ui.data import flatten_variants


setup_page("About Data")
city = st.session_state["selected_city"]
render_section_heading("About the data", "Know what is a sample, what was entered, and what is unavailable.", "Data and trust")

cars = get_cars()
variants = flatten_variants(cars)
groups = get_groups(city)
dealers = get_dealers()
quotes = [quote for group in groups for quote in get_quotes(group["id"])]

st.markdown("### Local car catalog")
st.write(f"Cars in the local catalog: {len(cars)}")
st.write(f"Exact variants listed: {len(variants)}")
st.info("The included catalog is demo data loaded from data/cars.json. Last-updated date: Unavailable. No website is scraped by this app.")
st.markdown("### Offers and groups")
st.write(f"Dealer records in SQLite: {len(dealers)}")
st.write(f"Groups in {city}: {len(groups)}")
st.write(f"Quote records for those groups: {len(quotes)}")
st.caption("Seeded quotes are labeled Demo data. Quotes entered through the demo dealer form are labeled unverified. No offer is called verified unless the database explicitly says it is verified.")
st.markdown("### Missing details")
st.write("If a car specification, date, delivery estimate, or quote item is missing, the app shows Unavailable. Missing values are not filled with guesses.")
st.markdown("### Estimate note")
st.write("On-road estimates are calculated in pricing.py using the editable sample state rates in config/india_locations.json. Real registration, tax, insurance, and dealer charges can differ.")
st.markdown("### Privacy note")
st.write("Dealer views show group city and member counts only. Buyer names are not shown in the dealer portal.")
