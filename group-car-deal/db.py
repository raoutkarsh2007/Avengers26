import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path


DB_PATH = Path(__file__).with_name("group_car_deal.db")


@contextmanager
def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def init_db():
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY,
                make TEXT NOT NULL,
                model TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS dealers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                city TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                car_id INTEGER NOT NULL REFERENCES cars(id),
                city TEXT NOT NULL,
                target_size INTEGER NOT NULL,
                variant_name TEXT,
                status TEXT NOT NULL DEFAULT 'Unavailable',
                deadline TEXT,
                source_type TEXT NOT NULL DEFAULT 'Demo data'
            );
            CREATE TABLE IF NOT EXISTS buyers (
                id INTEGER PRIMARY KEY,
                group_id INTEGER NOT NULL REFERENCES groups(id),
                name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY,
                group_id INTEGER NOT NULL REFERENCES groups(id),
                dealer_id INTEGER NOT NULL REFERENCES dealers(id),
                ex_showroom REAL NOT NULL,
                discount REAL NOT NULL,
                insurance REAL NOT NULL,
                rto REAL NOT NULL,
                accessories REAL NOT NULL,
                other_charges REAL NOT NULL,
                source_type TEXT NOT NULL DEFAULT 'Demo data',
                is_verified INTEGER NOT NULL DEFAULT 0,
                delivery_estimate_days INTEGER,
                valid_until TEXT,
                optional_addons_json TEXT NOT NULL DEFAULT '[]',
                UNIQUE(group_id, dealer_id)
            );
            """
        )
        car_columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(cars)")
        }
        new_columns = {
            "brand": "TEXT",
            "body_type": "TEXT",
            "fuel_types_json": "TEXT NOT NULL DEFAULT '[]'",
            "launch_year": "INTEGER",
            "model_years_json": "TEXT NOT NULL DEFAULT '[]'",
            "variants_json": "TEXT NOT NULL DEFAULT '[]'",
            "data_source": "TEXT NOT NULL DEFAULT 'sample'",
        }
        for column_name, column_type in new_columns.items():
            if column_name not in car_columns:
                connection.execute(
                    f"ALTER TABLE cars ADD COLUMN {column_name} {column_type}"
                )
        additions = {
            "groups": {
                "variant_name": "TEXT",
                "status": "TEXT NOT NULL DEFAULT 'Unavailable'",
                "deadline": "TEXT",
                "source_type": "TEXT NOT NULL DEFAULT 'Demo data'",
            },
            "quotes": {
                "source_type": "TEXT NOT NULL DEFAULT 'Demo data'",
                "is_verified": "INTEGER NOT NULL DEFAULT 0",
                "delivery_estimate_days": "INTEGER",
                "valid_until": "TEXT",
                "optional_addons_json": "TEXT NOT NULL DEFAULT '[]'",
            },
        }
        for table_name, columns in additions.items():
            current_columns = {
                row["name"]
                for row in connection.execute(f"PRAGMA table_info({table_name})")
            }
            for column_name, column_type in columns.items():
                if column_name not in current_columns:
                    connection.execute(
                        f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
                    )
        connection.execute(
            """
            UPDATE groups SET status = 'Unavailable'
            WHERE source_type = 'Demo data' AND status = 'Open'
            """
        )


def save_car(car):
    """Add or update one catalog car while keeping existing car IDs."""
    with get_connection() as connection:
        car_id = car.get("id")
        if car_id is None:
            existing = connection.execute(
                "SELECT id FROM cars WHERE make = ? AND model = ? ORDER BY id LIMIT 1",
                (car["brand"], car["model"]),
            ).fetchone()
            if existing:
                car_id = existing["id"]

        connection.execute(
            """
            INSERT INTO cars (
                id, make, model, brand, body_type, fuel_types_json, launch_year,
                model_years_json, variants_json, data_source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                make = excluded.make,
                model = excluded.model,
                brand = excluded.brand,
                body_type = excluded.body_type,
                fuel_types_json = excluded.fuel_types_json,
                launch_year = excluded.launch_year,
                model_years_json = excluded.model_years_json,
                variants_json = excluded.variants_json,
                data_source = excluded.data_source
            """,
            (
                car_id,
                car["brand"],
                car["model"],
                car["brand"],
                car.get("body_type"),
                json.dumps(car.get("fuel_types")),
                car.get("launch_year"),
                json.dumps(car.get("model_years_available")),
                json.dumps(car.get("variants")),
                car.get("data_source", "sample"),
            ),
        )


def get_cars():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM cars ORDER BY id"
        ).fetchall()
    cars = []
    for row in rows:
        car = dict(row)
        car["brand"] = car["brand"] or car["make"]
        car["fuel_types"] = json.loads(car.pop("fuel_types_json"))
        car["model_years_available"] = json.loads(car.pop("model_years_json"))
        car["variants"] = json.loads(car.pop("variants_json"))
        cars.append(car)
    return cars


def get_group_details(group_id=1):
    with get_connection() as connection:
        row = connection.execute(
            """
                 SELECT groups.id, groups.name, groups.city, groups.target_size,
                     groups.variant_name, groups.status, groups.deadline,
                     cars.make, cars.model, COUNT(buyers.id) AS buyer_count
            FROM groups
            JOIN cars ON cars.id = groups.car_id
            LEFT JOIN buyers ON buyers.group_id = groups.id
            WHERE groups.id = ?
            GROUP BY groups.id
            """,
            (group_id,),
        ).fetchone()
    return dict(row) if row else None


def get_groups(city=None):
    query = """
        SELECT groups.id, groups.name, groups.city, groups.target_size,
             groups.car_id, groups.variant_name, groups.status, groups.deadline,
             groups.source_type,
               cars.make, cars.model,
               COUNT(DISTINCT buyers.id) AS buyer_count,
               COUNT(DISTINCT quotes.id) AS offer_count
        FROM groups
        JOIN cars ON cars.id = groups.car_id
        LEFT JOIN buyers ON buyers.group_id = groups.id
        LEFT JOIN quotes ON quotes.group_id = groups.id
    """
    parameters = ()
    if city:
        query += " WHERE groups.city = ?"
        parameters = (city,)
    query += " GROUP BY groups.id ORDER BY groups.id DESC"
    with get_connection() as connection:
        rows = connection.execute(query, parameters).fetchall()
    return [dict(row) for row in rows]


def create_group(
    car_id,
    name,
    variant_name,
    city,
    target_size,
    deadline=None,
    source_type="Buyer-created",
):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO groups (
                name, car_id, city, target_size, variant_name, status, deadline,
                source_type
            ) VALUES (?, ?, ?, ?, ?, 'Open', ?, ?)
            """,
            (name, car_id, city, target_size, variant_name, deadline, source_type),
        )
        return cursor.lastrowid


def get_dealers():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, name, city FROM dealers ORDER BY id"
        ).fetchall()
    return [dict(row) for row in rows]


def get_buyers(group_id=1):
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT name FROM buyers WHERE group_id = ? ORDER BY name",
            (group_id,),
        ).fetchall()
    return [row["name"] for row in rows]


def add_buyer(group_id, name):
    """Add a name to the group unless it is blank or already used."""
    buyer_name = name.strip()
    if not buyer_name:
        return False

    with get_connection() as connection:
        existing = connection.execute(
            """
            SELECT id FROM buyers
            WHERE group_id = ? AND LOWER(name) = LOWER(?)
            """,
            (group_id, buyer_name),
        ).fetchone()
        if existing:
            return False
        connection.execute(
            "INSERT INTO buyers (group_id, name) VALUES (?, ?)",
            (group_id, buyer_name),
        )
    return True


def get_quotes(group_id=1):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT quotes.*, dealers.name AS dealer_name
            FROM quotes
            JOIN dealers ON dealers.id = quotes.dealer_id
            WHERE quotes.group_id = ?
            ORDER BY dealers.id
            """,
            (group_id,),
        ).fetchall()
    quotes = []
    for row in rows:
        quote = dict(row)
        quote["optional_addons"] = json.loads(quote.pop("optional_addons_json"))
        quotes.append(quote)
    return quotes


def save_quote(
    group_id,
    dealer_id,
    ex_showroom,
    discount,
    insurance,
    rto,
    accessories,
    other_charges,
    source_type="Demo data",
    is_verified=False,
    delivery_estimate_days=None,
    valid_until=None,
    optional_addons=None,
):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO quotes (
                group_id, dealer_id, ex_showroom, discount, insurance,
                rto, accessories, other_charges, source_type, is_verified,
                delivery_estimate_days, valid_until, optional_addons_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(group_id, dealer_id) DO UPDATE SET
                ex_showroom = excluded.ex_showroom,
                discount = excluded.discount,
                insurance = excluded.insurance,
                rto = excluded.rto,
                accessories = excluded.accessories,
                other_charges = excluded.other_charges,
                source_type = excluded.source_type,
                is_verified = excluded.is_verified,
                delivery_estimate_days = excluded.delivery_estimate_days,
                valid_until = excluded.valid_until,
                optional_addons_json = excluded.optional_addons_json
            """,
            (
                group_id,
                dealer_id,
                ex_showroom,
                discount,
                insurance,
                rto,
                accessories,
                other_charges,
                source_type,
                int(is_verified),
                delivery_estimate_days,
                valid_until,
                json.dumps(optional_addons or []),
            ),
        )
