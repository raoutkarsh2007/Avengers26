from html import escape

import streamlit as st

from db import get_group_details, get_groups, init_db
from pricing import calculate_on_road_price
from ui.data import comparison_item, demo_label, estimate_for_city, get_cities, value_or_unavailable
from ui.theme import COLORS


NAV_LINKS = [
    ("Explore Cars", "pages/1_Explore_Cars.py", "Explore Cars"),
    ("Buying Groups", "pages/3_Buying_Groups.py", "Buying Groups"),
    ("Compare", "pages/2_Compare.py", "Compare"),
    ("How It Works", "#how-it-works", "How It Works"),
]
MOBILE_PAGES = {
    "Home · GroupDiive": "app.py",
    "Explore Cars": "pages/1_Explore_Cars.py",
    "Buying Groups": "pages/3_Buying_Groups.py",
    "Compare": "pages/2_Compare.py",
    "Dealer Offers": "pages/4_Dealer_Offers.py",
    "AI Helper": "pages/5_AI_Helper.py",
    "Dealer Portal": "pages/6_Dealer_Portal.py",
    "About Data": "pages/7_About_Data.py",
}


def setup_page(section="Home"):
    st.set_page_config(
        page_title="GroupDiive",
        page_icon="🚘",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    from ui.theme import apply_theme

    init_db()
    apply_theme()
    render_header(section)
    render_comparison_tray()


def render_header(active_section="Home"):
    try:
        cities = get_cities()
    except Exception:
        cities = []
    if not cities:
        cities = ["Unavailable"]

    saved_city = st.session_state.get("selected_city")
    if saved_city not in cities:
        try:
            group = get_group_details()
            saved_city = group["city"] if group and group["city"] in cities else cities[0]
        except Exception:
            saved_city = cities[0]
        st.session_state["selected_city"] = saved_city

    with st.container(key="gcd-header"):
        brand_row = st.columns([2.4, 1.2], vertical_alignment="center")
        with brand_row[0]:
            st.markdown(
                "<a href='/' class='gcd-brand' aria-label='GroupDiive home'><span class='gcd-brand-mark'>G</span>"
                "<span class='gcd-brand-name'>GroupDiive</span></a>",
                unsafe_allow_html=True,
            )
        with brand_row[1]:
            live_indicator(st.session_state.get("selected_city", cities[0]))

        with st.container(key="gcd-desktop-nav"):
            nav_columns = st.columns(4)
            for column, (label, destination, section) in zip(nav_columns, NAV_LINKS):
                if destination.startswith("#"):
                    href = destination if active_section == "Home" else f"/{destination}"
                    column.markdown(f"<a href='{href}'>{label}</a>", unsafe_allow_html=True)
                elif active_section == section:
                    column.markdown(f"<div class='gcd-nav-active' aria-current='page'>{label}</div>", unsafe_allow_html=True)
                else:
                    column.page_link(destination, label=label)

        with st.container(key="gcd-mobile-nav"):
            mobile_columns = st.columns([4, 1], vertical_alignment="bottom")
            mobile_page = mobile_columns[0].selectbox(
                "Navigate",
                list(MOBILE_PAGES),
                key="gcd_mobile_page",
            )
            if mobile_columns[1].button("Go", key="gcd_mobile_go", width="stretch"):
                st.switch_page(MOBILE_PAGES[mobile_page])

        with st.container(key="gcd-controls"):
            control_columns = st.columns(3, vertical_alignment="bottom")
            control_columns[0].selectbox("City", cities, key="selected_city")
            control_columns[1].radio(
                "Mode", ["Buyer", "Dealer"], horizontal=True, key="gcd_role"
            )
            if st.session_state.get("gcd_role", "Buyer") == "Buyer":
                if control_columns[2].button(
                    "Start a group", key="header_start_group", width="stretch", type="primary"
                ):
                    st.switch_page("pages/3_Buying_Groups.py")
            else:
                if control_columns[2].button(
                    "Dealer portal", key="header_dealer_portal", width="stretch", type="primary"
                ):
                    st.switch_page("pages/6_Dealer_Portal.py")
        st.markdown("<hr style='border:0;border-top:1px solid var(--gcd-line);margin:.5rem 0 1.2rem'>", unsafe_allow_html=True)


@st.fragment(run_every="10s")
def live_indicator(city):
    try:
        get_groups(city)
    except Exception:
        st.markdown("<span class='gcd-offline'>● Offline</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='gcd-live'>● Live</span> <span class='gcd-muted'>10-second database refresh</span>", unsafe_allow_html=True)


def render_hero_car():
    hero = """
    <div class="scene" id="scene" role="img" aria-label="A locally drawn car on a layered forest-green road">
      <div class="sun"></div><div class="ridge ridge-back"></div><div class="ridge ridge-front"></div>
      <div class="road"><span class="road-line"></span></div>
      <svg class="car" id="car" viewBox="0 0 1000 450" aria-hidden="true">
        <defs>
                    <linearGradient id="body" x1="0" x2="1" y1="0" y2="1"><stop stop-color="{CAR_BODY_LIGHT}"/><stop offset=".55" stop-color="{GREEN_SOFT}"/><stop offset="1" stop-color="{GREEN}"/></linearGradient>
                    <linearGradient id="glass" x1="0" x2="1"><stop stop-color="{FOREST}"/><stop offset="1" stop-color="{CHARCOAL}"/></linearGradient>
        </defs>
                <ellipse cx="500" cy="370" rx="385" ry="34" fill="{CAR_DARK}" opacity=".48"/>
        <path d="M170 300 Q190 245 280 230 L370 130 Q410 91 500 91 L675 105 Q730 113 775 173 L849 220 Q895 244 905 300 L889 334 L130 334Z" fill="url(#body)"/>
        <path d="M325 218 L403 137 Q423 120 472 120 L486 218Z" fill="url(#glass)"/>
        <path d="M505 120 L660 132 Q704 139 741 192 L752 218 L505 218Z" fill="url(#glass)"/>
                <path d="M490 120 L493 218" stroke="{GREEN_SOFT}" stroke-width="9"/>
                <path d="M184 286 Q250 270 298 276 L300 319 L152 319Z" fill="{CORAL}"/>
                <path d="M808 260 Q852 270 878 290 L874 319 L820 319Z" fill="{WHITE}"/>
                <path d="M135 320 L895 320 L883 349 L160 349Z" fill="{FOREST}"/>
                <circle cx="300" cy="337" r="70" fill="{CAR_DARK}"/><circle cx="300" cy="337" r="35" fill="{CAR_RIM}"/><circle cx="300" cy="337" r="13" fill="{GREEN}"/>
                <circle cx="740" cy="337" r="70" fill="{CAR_DARK}"/><circle cx="740" cy="337" r="35" fill="{CAR_RIM}"/><circle cx="740" cy="337" r="13" fill="{GREEN}"/>
      </svg>
    </div>
    <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');
            :root{--hero-forest:{FOREST};--hero-green:{GREEN};--hero-green-soft:{GREEN_SOFT};--hero-cream:{CREAM};--hero-white:{WHITE};--hero-charcoal:{CHARCOAL};--hero-accent:{CORAL};--hero-road:{ROAD};--hero-back:{HERO_BACK};--hero-mid:{HERO_MID};--hero-deep:{HERO_DEEP};--hero-ridge-back:{RIDGE_BACK};--hero-ridge-front:{RIDGE_FRONT};--hero-glow:{SUN_GLOW};--hero-shadow:{SHADOW};}
            *{box-sizing:border-box} body{margin:0;background:var(--hero-forest);font-family:'Inter',system-ui,sans-serif}
            .scene{height:360px;position:relative;overflow:hidden;border-radius:18px;background:linear-gradient(150deg,var(--hero-back),var(--hero-mid) 62%,var(--hero-deep));isolation:isolate;animation:scene-in .7s ease both}
            .sun{position:absolute;width:185px;height:185px;right:13%;top:8%;border-radius:50%;background:var(--hero-green-soft);opacity:.82;box-shadow:0 0 70px var(--hero-glow)}
      .ridge{position:absolute;left:-5%;width:115%;bottom:28%;height:48%;border-radius:50% 50% 0 0}
            .ridge-back{background:var(--hero-ridge-back);transform:rotate(-5deg) translateY(28%)}
            .ridge-front{background:var(--hero-ridge-front);transform:rotate(5deg) translateY(43%)}
        .road{position:absolute;left:-10%;right:-10%;height:35%;bottom:-8%;background:var(--hero-road);transform:perspective(220px) rotateX(10deg);border-top:5px solid var(--hero-accent);z-index:1}
            .road-line{position:absolute;left:36%;top:48%;width:30%;border-top:4px dashed var(--hero-cream);opacity:.8}
        .car{position:absolute;width:min(94%,620px);left:50%;top:10%;z-index:2;transform:translateX(-50%);filter:drop-shadow(0 22px 18px var(--hero-shadow));animation:car-float 4s ease-in-out infinite;transform-origin:center}
      @keyframes car-float{0%,100%{translate:0 0;rotate:-1deg}50%{translate:0 -8px;rotate:1deg}}
      @keyframes scene-in{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
    @media(max-width:420px){.scene{height:245px}.car{top:29%;animation:none;transform:translateX(-50%)}.sun{width:125px;height:125px}}
      @media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
    </style>
    <script>
      const scene=document.getElementById('scene');const car=document.getElementById('car');
    if(scene&&car&&!window.matchMedia('(prefers-reduced-motion: reduce)').matches&&window.innerWidth>420){
        scene.addEventListener('pointermove',event=>{const box=scene.getBoundingClientRect();const x=(event.clientX-box.left)/box.width-.5;const y=(event.clientY-box.top)/box.height-.5;car.style.transform=`translateX(calc(-50% + ${x*10}px)) rotate(${x*1.6}deg) translateY(${y*-5}px)`;});
        scene.addEventListener('pointerleave',()=>{car.style.transform='translateX(-50%)';});
      }
    </script>
    """
    hero_tokens = {
        "FOREST": "forest",
        "GREEN": "green",
        "GREEN_SOFT": "green_soft",
        "CREAM": "cream",
        "WHITE": "white",
        "CHARCOAL": "charcoal",
        "CORAL": "coral",
        "ROAD": "road",
        "CAR_BODY_LIGHT": "car_body_light",
        "CAR_DARK": "car_dark",
        "CAR_RIM": "car_rim",
        "HERO_BACK": "hero_green_back",
        "HERO_MID": "hero_green_mid",
        "HERO_DEEP": "hero_green_deep",
        "RIDGE_BACK": "hero_ridge_back",
        "RIDGE_FRONT": "hero_ridge_front",
        "SUN_GLOW": "sun_glow",
        "SHADOW": "shadow_deep",
    }
    for placeholder, token in hero_tokens.items():
        hero = hero.replace("{" + placeholder + "}", COLORS[token])
    st.iframe(
        hero,
        width="stretch",
        height=370,
        alt="Locally drawn car with gentle motion on a layered green road",
    )


def render_section_heading(title, description=None, eyebrow=None):
    eyebrow_html = f"<div class='gcd-eyebrow'>{escape(eyebrow)}</div>" if eyebrow else ""
    description_html = f"<p class='gcd-muted'>{escape(description)}</p>" if description else ""
    st.markdown(
        f"<div class='gcd-section-head'><div>{eyebrow_html}<h2>{escape(title)}</h2>{description_html}</div></div>",
        unsafe_allow_html=True,
    )


def render_empty_state(title, message):
    st.markdown(
        f"<div class='gcd-empty'><div class='gcd-eyebrow'>Nothing here yet</div>"
        f"<h3>{escape(title)}</h3><p>{escape(message)}</p></div>",
        unsafe_allow_html=True,
    )


def render_error_state(title, message):
    st.error(f"{title}: {message}")


def render_car_card(car, variant, city, index=0, actions=True):
    item = comparison_item(car, variant, index)
    key = item["key"].replace(":", "-")
    label = f"{item['brand']} {item['model']} · {item['variant']}"
    ex_showroom = item["ex_showroom_price_inr"]
    on_road = estimate_for_city(ex_showroom, city)
    with st.container(border=True, key=f"car-card-{key}"):
        st.markdown(
            "<div class='gcd-car-visual'><svg viewBox='0 0 320 120' role='img' aria-label='Simple local car illustration'>"
            f"<path d='M38 78 54 52q5-9 20-12l28-23h99l30 25 36 10q16 4 20 18v19H35z' fill='{COLORS['green_soft']}'/>"
            f"<path d='m111 24-24 19h85V24zm87 0v19h38l-23-19z' fill='{COLORS['forest']}'/>"
            f"<circle cx='91' cy='89' r='19' fill='{COLORS['car_dark']}'/><circle cx='235' cy='89' r='19' fill='{COLORS['car_dark']}'/>"
            f"<circle cx='91' cy='89' r='8' fill='{COLORS['car_rim']}'/><circle cx='235' cy='89' r='8' fill='{COLORS['car_rim']}'/>"
            "</svg></div>",
            unsafe_allow_html=True,
        )
        st.markdown(f"<span class='gcd-demo-pill'>DEMO DATA</span><div class='gcd-card-title'>{escape(label)}</div>", unsafe_allow_html=True)
        st.caption(f"{value_or_unavailable(car.get('body_type'))} · {value_or_unavailable(variant.get('fuel'))} · {value_or_unavailable(variant.get('transmission'))}")
        price_cols = st.columns(2)
        price_cols[0].markdown(f"<div class='gcd-muted'>Ex-showroom</div><div class='gcd-price'>{'₹' + format(ex_showroom, ',') if ex_showroom is not None else 'Unavailable'}</div>", unsafe_allow_html=True)
        price_cols[1].markdown(f"<div class='gcd-muted'>Indicative on-road · demo estimate</div><div class='gcd-price'>{'₹' + format(on_road, ',') if on_road is not None else 'Unavailable'}</div>", unsafe_allow_html=True)
        spec_cols = st.columns(2)
        spec_cols[0].caption(f"Mileage / range: {value_or_unavailable(variant.get('mileage_or_ev_range'))}")
        spec_cols[1].caption(f"Seats: {value_or_unavailable(variant.get('seating'))}")
        st.caption("Source: Demo data · Last updated: Unavailable")
        if actions:
            action_cols = st.columns(3)
            if action_cols[0].button("Compare", key=f"compare-{key}", width="stretch"):
                selected = st.session_state.setdefault("compare_variants", [])
                if any(entry["key"] == item["key"] for entry in selected):
                    st.info("This variant is already selected.")
                elif len(selected) >= 4:
                    st.warning("Choose no more than four cars to compare.")
                else:
                    selected.append(item)
                    st.rerun()
            if st.session_state.get("gcd_role", "Buyer") == "Buyer":
                if action_cols[1].button("Join group", key=f"join-{key}", width="stretch", type="primary"):
                    st.session_state["preferred_variant"] = item
                    st.switch_page("pages/3_Buying_Groups.py")
                if action_cols[2].button("Start group", key=f"start-{key}", width="stretch", type="primary"):
                    st.session_state["preferred_variant"] = item
                    st.session_state["start_group_form"] = True
                    st.switch_page("pages/3_Buying_Groups.py")


def render_group_card(group, can_join=True):
    title = f"{value_or_unavailable(group.get('make'))} {value_or_unavailable(group.get('model'))}"
    variant = value_or_unavailable(group.get("variant_name"))
    target = group.get("target_size") or 0
    members = group.get("buyer_count") or 0
    count_label = f"{members} members" + (f" / {target}" if target else "")
    source = str(group.get("source_type", "Demo data"))
    badge = "Demo data" if "demo" in source.lower() else "Buyer-created"
    with st.container(border=True, key=f"group-card-{group['id']}"):
        st.markdown(f"<span class='gcd-demo-pill'>{escape(badge.upper())}</span><div class='gcd-card-title'>{escape(title)}</div>", unsafe_allow_html=True)
        st.write(f"Variant: {variant}")
        st.write(f"City: {escape(value_or_unavailable(group.get('city')))}")
        st.write(f"Members: {count_label}")
        if target:
            st.progress(min(members / target, 1.0), text=f"{members} of {target} members")
        else:
            st.caption("Group target: Unavailable")
        st.caption(f"Status: {escape(value_or_unavailable(group.get('status')))} · Offers: {group.get('offer_count', 0)}")
        st.caption(f"Offer deadline: {escape(value_or_unavailable(group.get('deadline')))}")
        if can_join and st.session_state.get("gcd_role", "Buyer") == "Buyer" and st.button("Join group", key=f"join-group-{group['id']}", width="stretch", type="primary"):
            st.session_state["selected_group_id"] = group["id"]
            st.switch_page("pages/3_Buying_Groups.py")


@st.fragment(run_every="10s")
def render_live_groups(city, limit=None):
    try:
        groups = get_groups(city)
    except Exception:
        st.markdown("<span class='gcd-offline'>● Offline</span>", unsafe_allow_html=True)
        st.warning("Group counts could not be refreshed. Try again in a moment.")
        return

    st.markdown("<span class='gcd-live'>● Live</span> <span class='gcd-muted'>Counts refresh every 10 seconds from SQLite.</span>", unsafe_allow_html=True)
    if not groups:
        render_empty_state("No groups in this city yet", "Start a group for the car and variant you want. Joining does not commit you to buy.")
        return

    visible_groups = groups[:limit] if limit else groups
    columns = st.columns(min(len(visible_groups), 3))
    for index, group in enumerate(visible_groups):
        with columns[index % len(columns)]:
            render_group_card(group)


def render_offer_card(quote):
    label = demo_label(quote)
    price_keys = ("ex_showroom", "discount", "insurance", "rto", "accessories", "other_charges")
    total = calculate_on_road_price(**{field: quote[field] for field in price_keys})
    if quote.get("is_verified"):
        badge_class = "gcd-verified-pill"
    elif quote.get("source_type") == "Demo data":
        badge_class = "gcd-demo-pill"
    else:
        badge_class = "gcd-submission-pill"
    with st.container(border=True):
        st.markdown(f"<span class='gcd-status-pill {badge_class}'>{escape(label.upper())}</span><div class='gcd-card-title'>{escape(quote['dealer_name'])}</div>", unsafe_allow_html=True)
        if quote.get("ex_showroom") is None or quote["ex_showroom"] <= 0:
            st.warning("Incomplete quote record. The price is unavailable until a valid ex-showroom amount is entered.")
            st.caption("Saved as demo data; not a verified dealer offer.")
            return
        st.markdown(f"<div class='gcd-muted'>Ex-showroom</div><div class='gcd-price'>₹{quote['ex_showroom']:,.0f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='gcd-muted'>On-road total</div><div class='gcd-price'>₹{total:,.0f}</div>", unsafe_allow_html=True)
        detail_cols = st.columns(2)
        details = [
            ("Discount", quote.get("discount")),
            ("RTO / registration", quote.get("rto")),
            ("Insurance", quote.get("insurance")),
            ("Accessories", quote.get("accessories")),
            ("Other charges", quote.get("other_charges")),
            ("Delivery estimate", f"{quote['delivery_estimate_days']} days" if quote.get("delivery_estimate_days") else None),
            ("Quote valid until", quote.get("valid_until")),
            ("Optional add-ons", ", ".join(quote.get("optional_addons", [])) or None),
        ]
        for index, (name, value) in enumerate(details):
            detail_cols[index % 2].markdown(f"<div class='gcd-spec'><b>{escape(name)}</b><span>{escape(value_or_unavailable(value))}</span></div>", unsafe_allow_html=True)


def open_comparison_dialog():
    selected = st.session_state.get("compare_variants", [])
    if not selected:
        st.info("Choose two to four variants first.")
        return
    show_comparison_dialog()


@st.dialog("Compare cars", width="large")
def show_comparison_dialog():
    selected = st.session_state.get("compare_variants", [])
    if len(selected) < 2:
        st.info("Choose at least two variants to compare.")
        return
    columns = {f"{item['brand']} {item['model']}\n{item['variant']}": item for item in selected}
    specs = [
        ("Body type", "body_type"),
        ("Fuel", "fuel"),
        ("Transmission", "transmission"),
        ("Seats", "seating"),
        ("Boot space", "boot_space_l"),
        ("Mileage / range", "mileage_or_ev_range"),
        ("Engine / power / torque", "engine_power_torque"),
        ("Battery / motor", "battery_motor"),
        ("Safety rating", "safety_rating"),
        ("Ex-showroom", "ex_showroom_price_inr"),
    ]
    rows = []
    for label, field in specs:
        rows.append({"Specification": label, **{name: value_or_unavailable(item.get(field)) for name, item in columns.items()}})
    st.table(rows)
    st.caption("Catalog prices are demo data. On-road estimates depend on city and local charges.")


def render_comparison_tray():
    selected = st.session_state.setdefault("compare_variants", [])
    if not selected:
        return
    with st.container(border=True, key="comparison-tray"):
        count = len(selected)
        st.markdown(f"<div class='gcd-card-title'>Compare cars · {count} selected</div>", unsafe_allow_html=True)
        item_cols = st.columns(min(count, 4) + 1)
        for index, item in enumerate(selected):
            item_cols[index].caption(f"{item['brand']} {item['model']} · {item['variant']}")
            if item_cols[index].button("Remove", key=f"remove-compare-{item['key']}"):
                st.session_state["compare_variants"] = [entry for entry in selected if entry["key"] != item["key"]]
                st.rerun()
        if item_cols[-1].button("Clear", key="clear-compare"):
            st.session_state["compare_variants"] = []
            st.rerun()
        if st.button("Compare Cars", key="compare-tray-open", disabled=count < 2, width="stretch", type="primary"):
            open_comparison_dialog()


def render_footer():
    st.markdown(
        "<footer class='gcd-footer'><div class='gcd-brand-name'>GroupDiive</div>"
        "<p>Prices and dealer offers depend on local quotes and availability. "
        "Demo data is shown clearly; verify details before making a decision.</p>"
        "<p>Joining a group is not a commitment to buy.</p></footer>",
        unsafe_allow_html=True,
    )
    footer_links = st.columns(4)
    for column, destination, label in zip(
        footer_links,
        (
            "pages/1_Explore_Cars.py",
            "pages/3_Buying_Groups.py",
            "pages/6_Dealer_Portal.py",
            "pages/7_About_Data.py",
        ),
        ("Explore cars", "Buying groups", "Dealer portal", "About data"),
    ):
        column.page_link(destination, label=label)
