import streamlit as st

from db import get_cars, get_groups, get_quotes
from ui.assistant import show_assistant_dialog
from ui.components import (
    open_comparison_dialog,
    render_car_card,
    render_empty_state,
    render_footer,
    render_hero_car,
    render_live_groups,
    render_offer_card,
    render_section_heading,
    setup_page,
)
from ui.data import flatten_variants


setup_page("Home")
city = st.session_state["selected_city"]
cars = get_cars()
variants = flatten_variants(cars)

hero_copy, hero_art = st.columns([1.05, 1], vertical_alignment="center")
with hero_copy:
    st.markdown(
        "<div class='gcd-hero-copy'><div class='gcd-eyebrow gcd-hero-eyebrow'>BUY TOGETHER · INDIA</div>"
        "<h1>Better car deals<br><span class='gcd-hero-accent'>start together.</span></h1>"
        "<p>Find your car, gather a local group, and compare itemized dealer offers before you decide.</p></div>",
        unsafe_allow_html=True,
    )
with hero_art:
    render_hero_car()

search_col, search_button_col = st.columns([5, 1.25], vertical_alignment="bottom")
with search_col:
    search_text = st.text_input(
        "Search make, model, or variant",
        placeholder="Try Nexon, Creta, or an exact variant",
        key="home_search",
    )
with search_button_col:
    if st.button("Explore cars", key="home_search_button", width="stretch", type="primary"):
        st.session_state["explore_search"] = search_text
        st.switch_page("pages/1_Explore_Cars.py")

st.markdown("<div id='car-discovery' class='gcd-section'></div>", unsafe_allow_html=True)
render_section_heading(
    "Find your next car",
    "Browse exact variants. Prices and specifications are clearly marked as demo data.",
    "Car discovery",
)
search_lower = search_text.strip().lower()
preview_variants = [
    row
    for row in variants
    if not search_lower
    or search_lower
    in " ".join(
        [
            str(row["car"].get("brand", "")),
            str(row["car"].get("model", "")),
            str(row["variant"].get("name", "")),
        ]
    ).lower()
][:3]
if preview_variants:
    car_columns = st.columns(len(preview_variants))
    for column, row in zip(car_columns, preview_variants):
        index = int(row["key"].split(":")[1])
        with column:
            render_car_card(row["car"], row["variant"], city, index)
else:
    render_empty_state("No matching demo variants", "Try a different make, model, or variant name.")
st.page_link("pages/1_Explore_Cars.py", label="Explore the full catalog")

st.markdown("<div id='comparison' class='gcd-section'></div>", unsafe_allow_html=True)
render_section_heading(
    "Compare before you choose",
    "Put two to four exact variants side by side, including their listed prices and specs.",
    "Comparison",
)
selected = st.session_state.get("compare_variants", [])
if selected:
    st.caption(f"{len(selected)} variant(s) in your comparison tray.")
    if st.button("Open comparison", key="home_open_compare"):
        open_comparison_dialog()
else:
    render_empty_state("Your comparison is ready when you are", "Choose Compare on a car card to add a variant here.")
st.page_link("pages/2_Compare.py", label="Go to Compare")

st.markdown("<div id='buying-groups' class='gcd-section'></div>", unsafe_allow_html=True)
render_section_heading(
    f"Buy together in {city}",
    "Member counts come from the database and refresh every ten seconds.",
    "Buying groups",
)
render_live_groups(city, limit=3)
st.page_link("pages/3_Buying_Groups.py", label="See all buying groups")

st.markdown("<div id='dealer-offers' class='gcd-section'></div>", unsafe_allow_html=True)
render_section_heading(
    "Dealer offers, item by item",
    "See ex-showroom separately from the calculated on-road total. Demo offers are never shown as verified.",
    "Dealer offers",
)
city_groups = get_groups(city)
if city_groups:
    offer_group = city_groups[0]
    quotes = get_quotes(offer_group["id"])
    if quotes:
        offer_columns = st.columns(min(len(quotes), 3))
        for column, quote in zip(offer_columns, quotes[:3]):
            with column:
                render_offer_card(quote)
    else:
        render_empty_state("No offers for this group yet", "A dealer quote will appear here after one is submitted.")
else:
    render_empty_state("No dealer quotes for this city yet", "Groups and quotes appear here when the database has them.")
st.page_link("pages/4_Dealer_Offers.py", label="Compare dealer offers")

st.markdown("<div id='ai-helper' class='gcd-section'></div>", unsafe_allow_html=True)
render_section_heading(
    "Questions about a car or quote?",
    "The local AI uses only the catalog and offer data you choose. It says when details are unavailable.",
    "AI helper",
)
if st.button("Ask the GroupDiive helper", key="home_ai_open", type="primary"):
    show_assistant_dialog(city)
st.page_link("pages/5_AI_Helper.py", label="Open the AI helper")

st.markdown("<div id='how-it-works' class='gcd-section'></div>", unsafe_allow_html=True)
render_section_heading(
    "How group buying works",
    "Joining a group is not a commitment to buy.",
    "Three simple steps",
)
steps = st.columns(3)
for column, number, title, copy in zip(
    steps,
    ("01", "02", "03"),
    ("Choose a variant", "Join or start a group", "Compare dealer quotes"),
    (
        "Pick a car and exact variant from the local catalog.",
        "Bring interested buyers in the same city together.",
        "Review each item and decide for yourself.",
    ),
):
    with column:
        st.markdown(f"<div class='gcd-eyebrow'>{number}</div><h3>{title}</h3><p>{copy}</p>", unsafe_allow_html=True)

render_footer()
st.caption("Motion note: the hero responds to pointer movement and uses CSS entrance motion. Streamlit cannot read scroll position inside this embedded scene; mobile and reduced-motion users get a static car illustration.")
