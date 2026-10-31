import streamlit as st


# Shared palette. Dark green is reserved for white-on-green buttons and headings.
COLORS = {
    "forest": "#1F5E3B",
    "forest_light": "#286B45",
    "green": "#2E8B57",
    "green_soft": "#5FBF8A",
    "green_pale": "#E8F5EC",
    "cream": "#FAFBF8",
    "cream_deep": "#F0F4EF",
    "charcoal": "#18231C",
    "muted": "#46564C",
    "coral": "#B13B29",
    "coral_light": "#FBE5DF",
    "demo_text": "#732E22",
    "submission_text": "#3E4B43",
    "white": "#FFFFFF",
    "line": "#6D7D72",
    "road": "#27332C",
    "car_dark": "#0F2118",
    "car_rim": "#DCE5DD",
    "hero_green_back": "#286B45",
    "hero_green_mid": "#1F5E3B",
    "hero_green_deep": "#17492F",
    "hero_ridge_back": "#5B9A72",
    "hero_ridge_front": "#3A7954",
    "car_body_light": "#FAFBF8",
    "shadow": "rgba(24, 35, 28, .12)",
    "shadow_deep": "rgba(24, 35, 28, .20)",
    "sun_glow": "rgba(95, 191, 138, .34)",
}


def apply_theme():
    """Apply the shared palette, Google fonts, button states, and focus styles."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');
        :root {{
            --gcd-forest: {COLORS['forest']};
            --gcd-forest-light: {COLORS['forest_light']};
            --gcd-green: {COLORS['green']};
            --gcd-green-soft: {COLORS['green_soft']};
            --gcd-green-pale: {COLORS['green_pale']};
            --gcd-cream: {COLORS['cream']};
            --gcd-cream-deep: {COLORS['cream_deep']};
            --gcd-charcoal: {COLORS['charcoal']};
            --gcd-muted: {COLORS['muted']};
            --gcd-coral: {COLORS['coral']};
            --gcd-coral-light: {COLORS['coral_light']};
            --gcd-demo-text: {COLORS['demo_text']};
            --gcd-submission-text: {COLORS['submission_text']};
            --gcd-white: {COLORS['white']};
            --gcd-line: {COLORS['line']};
            --gcd-road: {COLORS['road']};
            --gcd-font-heading: 'Manrope', system-ui, sans-serif;
            --gcd-font-body: 'Inter', system-ui, sans-serif;
            --gcd-shadow: {COLORS['shadow']};
            --gcd-shadow-deep: {COLORS['shadow_deep']};
        }}
        html, body, [data-testid="stAppViewContainer"] {{
            color: var(--gcd-charcoal);
            font-family: var(--gcd-font-body) !important;
        }}
        [data-testid="stAppViewContainer"] {{ background: var(--gcd-cream); }}
        [data-testid="stHeader"] {{ background: transparent; }}
        [data-testid="stSidebarNav"] {{ display:none !important; }}
        [data-testid="stMainBlockContainer"] {{
            max-width: 1440px;
            padding: 1.2rem clamp(1rem, 3vw, 2.8rem) 6rem;
        }}
        h1, h2, h3, h4, h5, h6, .gcd-brand-name, .gcd-brand-mark,
        .gcd-card-title, .gcd-hero-copy h1 {{
            color: var(--gcd-forest) !important;
            font-family: var(--gcd-font-heading) !important;
            letter-spacing: 0 !important;
        }}
        h1 {{ font-size: 4.2rem !important; line-height: 1.02 !important; }}
        h2 {{ font-size: 2.6rem !important; }}
        p, label, li, input, textarea, select, button, table, th, td,
        [data-testid="stCaptionContainer"], [data-testid="stMarkdownContainer"] {{
            color: var(--gcd-charcoal);
            font-family: var(--gcd-font-body) !important;
        }}
        a {{ color: var(--gcd-forest) !important; font-family: var(--gcd-font-body) !important; }}
        a:focus-visible, button:focus-visible, input:focus-visible,
        textarea:focus-visible, [role="radio"]:focus-visible,
        [role="combobox"]:focus-visible {{
            outline: 3px solid var(--gcd-coral) !important;
            outline-offset: 3px !important;
        }}

        :is(.stButton > button[kind="primary"], [data-testid="stBaseButton-primary"],
            [data-testid="stFormSubmitButton"] button) {{
            border: 1px solid var(--gcd-forest) !important;
            border-radius: 10px !important;
            background: var(--gcd-forest) !important;
            color: var(--gcd-white) !important;
            font-weight: 700 !important;
            transition: transform 160ms ease, box-shadow 160ms ease, background 160ms ease;
        }}
        :is(.stButton > button[kind="primary"], [data-testid="stBaseButton-primary"],
            [data-testid="stFormSubmitButton"] button) * {{
            color: var(--gcd-white) !important;
            font-family: var(--gcd-font-body) !important;
        }}
        :is(.stButton > button[kind="primary"], [data-testid="stBaseButton-primary"],
            [data-testid="stFormSubmitButton"] button):is(:hover, :focus, :focus-visible) {{
            border-color: var(--gcd-forest-light) !important;
            background: var(--gcd-forest-light) !important;
            color: var(--gcd-white) !important;
            box-shadow: 0 8px 18px var(--gcd-shadow-deep);
            transform: translateY(-1px);
        }}
        :is(.stButton > button[kind="primary"], [data-testid="stBaseButton-primary"],
            [data-testid="stFormSubmitButton"] button):is(:hover, :focus, :focus-visible) * {{
            color: var(--gcd-white) !important;
        }}
        :is(.stButton > button[kind="primary"], [data-testid="stBaseButton-primary"],
            [data-testid="stFormSubmitButton"] button):disabled {{
            background: var(--gcd-forest-light) !important;
            color: var(--gcd-white) !important;
            opacity: 1 !important;
            cursor: not-allowed;
        }}
        :is(.stButton > button[kind="primary"], [data-testid="stBaseButton-primary"],
            [data-testid="stFormSubmitButton"] button):disabled * {{ color: var(--gcd-white) !important; }}

        :is(.stButton > button[kind="secondary"], .stButton > button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]),
            [data-testid="stBaseButton-secondary"], [data-testid="stPageLink"] a,
            [data-testid="stPageLink-NavLink"], [data-testid="stLinkButton"],
            [data-testid="stLinkButton"] a, [data-testid="stDownloadButton"] button) {{
            border: 1px solid var(--gcd-forest-light) !important;
            border-radius: 10px !important;
            background: var(--gcd-white) !important;
            color: var(--gcd-charcoal) !important;
            font-weight: 650 !important;
            transition: transform 160ms ease, box-shadow 160ms ease, background 160ms ease;
        }}
        :is(.stButton > button[kind="secondary"], .stButton > button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]),
            [data-testid="stBaseButton-secondary"], [data-testid="stPageLink"] a,
            [data-testid="stPageLink-NavLink"], [data-testid="stLinkButton"],
            [data-testid="stLinkButton"] a, [data-testid="stDownloadButton"] button) * {{
            color: var(--gcd-charcoal) !important;
            font-family: var(--gcd-font-body) !important;
        }}
        :is(.stButton > button[kind="secondary"], .stButton > button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]),
            [data-testid="stBaseButton-secondary"], [data-testid="stPageLink"] a,
            [data-testid="stPageLink-NavLink"], [data-testid="stLinkButton"],
            [data-testid="stLinkButton"] a, [data-testid="stDownloadButton"] button):is(:hover, :focus, :focus-visible) {{
            border-color: var(--gcd-forest) !important;
            background: var(--gcd-green-pale) !important;
            color: var(--gcd-charcoal) !important;
            box-shadow: 0 6px 16px var(--gcd-shadow);
        }}
        :is(.stButton > button[kind="secondary"], .stButton > button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]),
            [data-testid="stBaseButton-secondary"], [data-testid="stPageLink"] a,
            [data-testid="stPageLink-NavLink"], [data-testid="stLinkButton"],
            [data-testid="stLinkButton"] a, [data-testid="stDownloadButton"] button):is(:hover, :focus, :focus-visible) * {{
            color: var(--gcd-charcoal) !important;
        }}
        :is(.stButton > button[kind="secondary"], .stButton > button:not([kind="primary"]),
            [data-testid="stBaseButton-secondary"], [data-testid="stPageLink"] a,
            [data-testid="stPageLink-NavLink"], [data-testid="stLinkButton"],
            [data-testid="stLinkButton"] a, [data-testid="stDownloadButton"] button):disabled {{
            background: var(--gcd-cream-deep) !important;
            color: var(--gcd-charcoal) !important;
            opacity: 1 !important;
            cursor: not-allowed;
        }}
        :is(.stButton > button[kind="secondary"], .stButton > button:not([kind="primary"]),
            [data-testid="stBaseButton-secondary"], [data-testid="stPageLink"] a,
            [data-testid="stPageLink-NavLink"], [data-testid="stLinkButton"],
            [data-testid="stLinkButton"] a, [data-testid="stDownloadButton"] button):disabled * {{
            color: var(--gcd-charcoal) !important;
        }}

        [data-testid="stVerticalBlockBorderWrapper"] {{
            border-color: var(--gcd-line) !important;
            border-radius: 12px !important;
            background: var(--gcd-white);
            box-shadow: 0 8px 28px var(--gcd-shadow);
        }}
        [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input,
        [data-testid="stDateInput"] input {{ border-radius: 8px; }}
        [data-testid="stProgressBar"] > div > div {{ background: var(--gcd-coral); }}
        .gcd-brand {{ display:flex; align-items:center; gap:.65rem; min-height:3rem; text-decoration:none !important; }}
        .gcd-brand-mark {{
            width:2.35rem; height:2.35rem; border-radius:50%; display:grid;
            place-items:center; background:var(--gcd-forest); color:var(--gcd-white);
            font-size:1.3rem; font-weight:800;
        }}
        .gcd-brand-name {{ color:var(--gcd-forest); font-weight:800; font-size:1.05rem; }}
        .gcd-nav-active {{ color:var(--gcd-forest); font-weight:800; border-bottom:3px solid var(--gcd-coral); padding:.55rem .2rem; }}
        .gcd-eyebrow {{ color:var(--gcd-forest); font-size:.76rem; font-weight:800; text-transform:uppercase; }}
        .gcd-demo-pill, .gcd-status-pill {{
            display:inline-block; padding:.25rem .55rem; border-radius:999px;
            font-weight:700; font-size:.72rem; letter-spacing:.02em;
        }}
        .gcd-demo-pill {{ background:var(--gcd-coral-light); color:var(--gcd-demo-text); }}
        .gcd-verified-pill {{ background:var(--gcd-green-pale); color:var(--gcd-forest); }}
        .gcd-submission-pill {{ background:var(--gcd-cream-deep); color:var(--gcd-submission-text); }}
        .gcd-live {{ color:var(--gcd-forest); font-weight:800; }}
        .gcd-offline {{ color:var(--gcd-coral); font-weight:800; }}
        .gcd-muted {{ color:var(--gcd-muted); font-size:.88rem; }}
        .gcd-price {{ color:var(--gcd-forest); font-size:1.35rem; font-weight:800; }}
        .gcd-hero-copy {{
            background:var(--gcd-forest); color:var(--gcd-white); border-radius:18px;
            padding:clamp(1.5rem,4vw,3rem); min-height:100%; animation:gcd-rise-in 650ms ease both;
        }}
        .gcd-hero-copy h1, .gcd-hero-copy p {{ color:var(--gcd-white) !important; }}
        .gcd-hero-copy .gcd-hero-eyebrow {{ color:var(--gcd-white) !important; }}
        .gcd-hero-copy .gcd-hero-accent {{ color:var(--gcd-white) !important; text-decoration:underline; text-decoration-color:var(--gcd-coral); text-decoration-thickness:.12em; text-underline-offset:.12em; }}
        .gcd-section {{ padding:2.4rem 0 1.2rem; }}
        .gcd-section-head {{ display:flex; align-items:end; justify-content:space-between; gap:1rem; }}
        .gcd-card-title {{ color:var(--gcd-forest); font-size:1.2rem; font-weight:800; }}
        .gcd-spec-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.4rem 1rem; }}
        .gcd-spec {{ border-bottom:1px solid var(--gcd-line); padding:.45rem 0; }}
        .gcd-spec b {{ display:block; font-size:.73rem; color:var(--gcd-muted); text-transform:uppercase; }}
        .gcd-spec span {{ color:var(--gcd-charcoal); }}
        .gcd-footer {{ margin-top:3rem; padding:2rem; border-radius:14px; background:var(--gcd-forest); color:var(--gcd-white); }}
        .gcd-footer p, .gcd-footer a {{ color:var(--gcd-white) !important; }}
        .gcd-footer .gcd-brand-name {{ color:var(--gcd-white) !important; }}
        .st-key-comparison-tray {{
            position:sticky; bottom:1rem; z-index:50; padding:.5rem;
            border:2px solid var(--gcd-forest); border-radius:14px;
            box-shadow:0 12px 36px var(--gcd-shadow-deep); background:var(--gcd-white);
        }}
        .st-key-gcd-mobile-nav {{ display:none; }}
        @keyframes gcd-rise-in {{ from {{ opacity:0; transform:translateY(14px); }} to {{ opacity:1; transform:translateY(0); }} }}
        @media (max-width: 900px) {{
            [data-testid="stMainBlockContainer"] {{ padding-inline:1rem; }}
            h1 {{ font-size:3.2rem !important; }}
            h2 {{ font-size:2.2rem !important; }}
        }}
        @media (max-width: 640px) {{
            h1 {{ font-size:2.25rem !important; }}
            h2 {{ font-size:1.8rem !important; }}
            .gcd-section {{ padding-top:1.4rem; }}
            .gcd-footer {{ padding:1.25rem; }}
            .st-key-gcd-header .st-key-gcd-desktop-nav {{ display:none !important; }}
            .st-key-gcd-mobile-nav {{ display:block !important; }}
            .st-key-gcd-controls [data-testid="stHorizontalBlock"] {{
                display:grid !important;
                grid-template-columns:repeat(2,minmax(0,1fr));
                gap:.2rem .8rem;
            }}
            .st-key-gcd-controls [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
                width:auto !important; min-width:0 !important; flex:none !important;
            }}
            .st-key-gcd-controls [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(3) {{ grid-column:1 / -1; }}
        }}
        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{ scroll-behavior:auto !important; animation-duration:.01ms !important; transition-duration:.01ms !important; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
