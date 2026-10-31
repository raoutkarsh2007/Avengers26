import json
from pathlib import Path

from db import get_cars
from pricing import calculate_on_road_price, estimate_state_charges, load_location_config



def get_cities():
    config = load_location_config()
    return sorted({city for location in config["locations"] for city in location["cities"]})


def flatten_variants(cars=None):
    rows = []
    for car in cars if cars is not None else get_cars():
        for index, variant in enumerate(car.get("variants", [])):
            rows.append(
                {
                    "key": f"{car['id']}:{index}",
                    "car": car,
                    "variant": variant,
                }
            )
    return rows


def value_or_unavailable(value, suffix=""):
    if value is None or value == "":
        return "Unavailable"
    return f"{value}{suffix}"


def demo_label(record):
    source = str(record.get("data_source") or record.get("source_type") or "").lower()
    if "verified" in source or record.get("is_verified"):
        return "Verified dealer offer"
    if "demo" in source or source == "sample":
        return "Demo data"
    return "Unverified dealer submission"


def estimate_for_city(ex_showroom, city):
    if ex_showroom is None:
        return None
    config = load_location_config()
    location = next(
        (item for item in config["locations"] if city in item["cities"]),
        None,
    )
    if location is None:
        return None
    charges = estimate_state_charges(ex_showroom, location["state"], config)
    return calculate_on_road_price(
        ex_showroom=ex_showroom,
        rto=charges["rto"],
        insurance=charges["insurance"],
    )


def comparison_item(car, variant, index):
    return {
        "key": f"{car['id']}:{index}",
        "brand": car.get("brand") or car.get("make"),
        "model": car.get("model"),
        "variant": variant.get("name"),
        "body_type": car.get("body_type"),
        "fuel": variant.get("fuel"),
        "transmission": variant.get("transmission"),
        "seating": variant.get("seating"),
        "boot_space_l": variant.get("boot_space_l"),
        "mileage_or_ev_range": variant.get("mileage_or_ev_range"),
        "engine_power_torque": variant.get("engine_power_torque"),
        "battery_motor": variant.get("battery_motor"),
        "safety_rating": variant.get("safety_rating"),
        "ex_showroom_price_inr": variant.get("ex_showroom_price_inr"),
        "key_features": variant.get("key_features", []),
        "data_source": car.get("data_source", "sample"),
    }
