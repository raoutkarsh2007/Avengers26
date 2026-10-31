import json
from pathlib import Path


LOCATION_CONFIG_PATH = Path(__file__).parent / "config" / "india_locations.json"


def load_location_config():
    """Read the editable city list and estimate rates."""
    with LOCATION_CONFIG_PATH.open(encoding="utf-8") as config_file:
        return json.load(config_file)


def estimate_state_charges(ex_showroom, state, location_config=None):
    """Estimate RTO and insurance using the selected state's sample rates."""
    config = location_config or load_location_config()
    location = next(
        (item for item in config["locations"] if item["state"] == state),
        None,
    )
    if location is None:
        raise ValueError(f"No estimate rates found for {state}.")

    rto = round(ex_showroom * location["rto_estimate_rate"])
    insurance = round(ex_showroom * location["insurance_estimate_rate"])
    return {
        "rto": rto,
        "insurance": insurance,
        "rto_rate": location["rto_estimate_rate"],
        "insurance_rate": location["insurance_estimate_rate"],
    }


def calculate_on_road_price(
    ex_showroom,
    discount=0,
    insurance=0,
    rto=0,
    accessories=0,
    other_charges=0,
):
    """Add the price parts using normal Python math."""
    return ex_showroom - discount + rto + insurance + accessories + other_charges
