# GroupDiive UI Brief

## Product

GroupDiive is a responsive group car-buying app for India. It helps people explore a local car catalog, compare exact variants, find or start a buyer group, and review itemized dealer offers. Joining a group is not a commitment to buy.

## Brand and appearance

Use the exact visible app name **GroupDiive** in the logo, page title, navigation, and footer. Use a fresh green, clean off-white, charcoal text, and one coral accent. Use Manrope for headings and Inter for body text, with system font fallbacks. Buttons must have readable nested text, clear primary and secondary states, and visible keyboard focus.

## Main experience

The Home page has a compact header, city and Buyer/Dealer controls, an animated local car illustration, and previews for discovery, comparison, buying groups, dealer offers, and the AI helper. Separate Streamlit pages provide Explore Cars, Compare, Buying Groups, Dealer Offers, AI Helper, Dealer Portal, and About Data.

Use a local SVG/CSS car illustration, not remote vehicle images. Desktop motion may respond to pointer movement; small screens and reduced-motion preferences use a static version. Streamlit cannot provide true scroll-linked parallax inside an embedded scene.

## Data and trust

Use the existing SQLite database, local JSON catalog, pricing functions, and Ollama helper. Do not scrape websites or invent car details, prices, buyers, groups, dealers, offers, availability, or savings. Clearly identify demo records. Display unavailable values as Unavailable. Keep price calculations in Python, never in the AI. Verified offers must be visibly distinct from demo and unverified offers.

Live group counts come from SQLite refreshes. Show Live only after a successful refresh, otherwise Offline. Dealer pages show city and member counts, never buyer names. The AI receives only selected catalog and quote records, states when data is missing, and remains optional when Ollama is unavailable.

## Layout and accessibility

Use responsive layouts, readable contrast, keyboard focus, labeled inputs, useful empty/error/success states, and clear form validation. Keep the existing project structure and working features; make database changes additive.
