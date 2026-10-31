import json
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from db import init_db, save_car


CATALOG_PATH = Path(__file__).with_name("cars.json")


def load_car_catalog(catalog_path=CATALOG_PATH):
    """Copy the local JSON car list into SQLite."""
    with Path(catalog_path).open(encoding="utf-8") as catalog_file:
        cars = json.load(catalog_file)

    if not isinstance(cars, list):
        raise ValueError("The car catalog must be a JSON list.")

    init_db()
    for car in cars:
        if car.get("data_source") != "sample":
            raise ValueError(f"{car.get('model', 'A car')} must use sample data.")
        save_car(car)

    return len(cars)


if __name__ == "__main__":
    count = load_car_catalog()
    print(f"Loaded {count} sample cars into SQLite.")
