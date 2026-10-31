import streamlit as st

from db import get_cars, get_groups, get_quotes
from llm import AssistantError, OllamaUnavailable, ask_about_catalog
from pricing import calculate_on_road_price


def _get_assistant_context(car_id, group_id, city):
    cars = get_cars()
    selected_car = next((car for car in cars if car["id"] == car_id), None)
    if selected_car is None:
        raise ValueError("That car is not in the local catalog.")

    groups = get_groups(city)
    selected_group = next(
        (group for group in groups if group["id"] == group_id),
        None,
    )
    quotes = get_quotes(group_id) if selected_group else []
    catalog_context = [
        {
            "brand": selected_car.get("brand") or selected_car.get("make"),
            "model": selected_car.get("model"),
            "body_type": selected_car.get("body_type"),
            "fuel_types": selected_car.get("fuel_types"),
            "data_source": "Demo data" if selected_car.get("data_source") == "sample" else selected_car.get("data_source"),
            "variants": selected_car.get("variants", []),
        }
    ]
    quote_context = []
    for quote in quotes:
        quote_data = {
            "dealer": quote.get("dealer_name"),
            "source": quote.get("source_type", "Demo data"),
            "verified": bool(quote.get("is_verified")),
            "delivery_estimate_days": quote.get("delivery_estimate_days"),
            "valid_until": quote.get("valid_until"),
        }
        if quote.get("ex_showroom") is None or quote["ex_showroom"] <= 0:
            quote_data["quote_status"] = "Incomplete; prices unavailable"
            quote_data.update(
                {
                    "ex_showroom": None,
                    "discount": None,
                    "registration": None,
                    "insurance": None,
                    "accessories": None,
                    "other_charges": None,
                    "on_road_total": None,
                }
            )
        else:
            quote_data["quote_status"] = "Itemized quote"
            quote_data.update(
                {
                    "ex_showroom": quote["ex_showroom"],
                    "discount": quote["discount"],
                    "registration": quote["rto"],
                    "insurance": quote["insurance"],
                    "accessories": quote["accessories"],
                    "other_charges": quote["other_charges"],
                    "on_road_total": calculate_on_road_price(
                        ex_showroom=quote["ex_showroom"],
                        discount=quote["discount"],
                        rto=quote["rto"],
                        insurance=quote["insurance"],
                        accessories=quote["accessories"],
                        other_charges=quote["other_charges"],
                    ),
                }
            )
        quote_context.append(quote_data)
    return catalog_context, quote_context


def answer_with_project_data(question, car_id, group_id, city):
    catalog, quotes = _get_assistant_context(car_id, group_id, city)
    return ask_about_catalog(question, catalog, quotes)


def _render_ai_response(question, car_id, group_id, city):
    try:
        with st.spinner("Checking the local car and quote data..."):
            answer = answer_with_project_data(question, car_id, group_id, city)
    except OllamaUnavailable as error:
        st.warning(f"AI unavailable: {error}")
    except AssistantError as error:
        st.error(f"AI error: {error}")
    except Exception:
        st.error("The car data could not be loaded. Please try again.")
    else:
        st.success("Answer based on the selected catalog and quote data")
        st.write(answer)


def assistant_panel(city):
    cars = get_cars()
    if not cars:
        st.info("No local catalog data is available yet.")
        return

    groups = get_groups(city)
    car_labels = {
        f"{car.get('brand') or car.get('make')} {car['model']}": car["id"]
        for car in cars
    }
    car_label = st.selectbox("Car data to use", list(car_labels), key="assistant_car")
    group_labels = {"No group or quote data": None}
    group_labels.update(
        {
            f"{group['name']} · {group['city']} · group {group['id']}": group["id"]
            for group in groups
        }
    )
    group_label = st.selectbox(
        "Group offers to include",
        list(group_labels),
        key="assistant_group",
    )
    with st.form("assistant_question_form"):
        question = st.text_input(
            "Ask about this car or its selected offers",
            placeholder="What should I check in this quote?",
        )
        submitted = st.form_submit_button("Ask the local AI")
    if submitted:
        if not question.strip():
            st.error("Type a question first.")
        else:
            _render_ai_response(
                question,
                car_labels[car_label],
                group_labels[group_label],
                city,
            )


@st.dialog("Ask the GroupDiive helper", width="large")
def show_assistant_dialog(city):
    st.caption("The AI sees only the car and offer data you choose here. Missing information is reported as unavailable.")
    assistant_panel(city)
