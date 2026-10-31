import csv
import json
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from db import init_db, save_car


JSON_FIELDS = ("fuel_types", "model_years_available", "variants")
REQUIRED_COLUMNS = {"brand", "model", "body_type", "fuel_types", "variants"}
VARIANT_FIELDS = {
    "name",
    "ex_showroom_price_inr",
    "fuel",
    "transmission",
    "mileage_or_ev_range",
    "engine_power_torque",
    "battery_motor",
    "seating",
    "boot_space_l",
    "safety_rating",
    "key_features",
}


def parse_json_cell(row, field_name, row_number):
    value = row.get(field_name, "").strip()
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"CSV row {row_number}: {field_name} must contain valid JSON."
        ) from error


def read_car_csv(csv_path):
    """Read local car rows; list and variant columns must contain JSON."""
    with Path(csv_path).open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError("CSV is missing columns: " + ", ".join(sorted(missing)))

        cars = []
        for row_number, row in enumerate(reader, start=2):
            car = {
                "brand": row["brand"].strip(),
                "model": row["model"].strip(),
                "body_type": row["body_type"].strip() or None,
                "launch_year": int(row["launch_year"]) if row.get("launch_year", "").strip() else None,
                "data_source": "sample",
            }
            for field_name in JSON_FIELDS:
                car[field_name] = parse_json_cell(row, field_name, row_number)
            if not car["brand"] or not car["model"] or not car["body_type"]:
                raise ValueError(
                    f"CSV row {row_number}: brand, model, and body_type are required."
                )
            if (
                not isinstance(car["fuel_types"], list)
                or not car["fuel_types"]
                or not isinstance(car["variants"], list)
                or not car["variants"]
            ):
                raise ValueError(
                    f"CSV row {row_number}: fuel_types and variants must be non-empty JSON lists."
                )
            if car["model_years_available"] is not None and not isinstance(
                car["model_years_available"], list
            ):
                raise ValueError(
                    f"CSV row {row_number}: model_years_available must be a JSON list or blank."
                )
            for variant in car["variants"]:
                if not isinstance(variant, dict) or not VARIANT_FIELDS <= variant.keys():
                    raise ValueError(
                        f"CSV row {row_number}: each variant must include all variant fields."
                    )
                if not isinstance(variant["key_features"], list):
                    raise ValueError(
                        f"CSV row {row_number}: variant key_features must be a JSON list."
                    )
            cars.append(car)
    return cars


def import_cars(csv_path):
    cars = read_car_csv(csv_path)
    init_db()
    for car in cars:
        save_car(car)
    return len(cars)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Use: python data/import_cars.py path/to/cars.csv")
    imported = import_cars(sys.argv[1])
    print(f"Imported {imported} local sample cars.")
