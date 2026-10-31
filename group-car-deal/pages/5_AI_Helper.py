import streamlit as st

from ui.assistant import assistant_panel
from ui.components import render_section_heading, setup_page


setup_page("AI Helper")
city = st.session_state["selected_city"]
render_section_heading("Ask about the data on this page", "The local Ollama model only receives the car and offer data you select.", "AI helper")
st.info("The AI does not calculate prices or browse websites. It says when a detail is unavailable. Answers are generated locally and may still need checking.")
assistant_panel(city)
