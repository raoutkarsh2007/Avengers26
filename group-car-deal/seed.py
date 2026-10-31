from data.load_cars import load_car_catalog
from db import get_connection, init_db, save_quote


DEALER_ROWS = [
    (1, "Harbor Motors", "Mumbai"),
    (2, "Mumbai Auto Hub", "Mumbai"),
    (3, "Western Wheels", "Mumbai"),
]
GROUP_ID = 1


init_db()
car_count = load_car_catalog()
with get_connection() as connection:
    connection.executemany(
        "INSERT OR IGNORE INTO dealers (id, name, city) VALUES (?, ?, ?)",
        DEALER_ROWS,
    )
    connection.execute(
        """
        INSERT OR IGNORE INTO groups (id, name, car_id, city, target_size)
        VALUES (?, ?, ?, ?, ?)
        """,
        (GROUP_ID, "Mumbai Nexon Buyers", 1, "Mumbai", 20),
    )
    connection.executemany(
        "INSERT OR IGNORE INTO buyers (id, group_id, name) VALUES (?, ?, ?)",
        [
            (buyer_id, GROUP_ID, f"Buyer {buyer_id}")
            for buyer_id in range(1, 15)
        ],
    )

DEMO_QUOTES = [
    (1, 1000000, 25000, 45000, 125000, 8000, 2000),
    (2, 1000000, 35000, 53000, 125000, 12000, 5000),
    (3, 1000000, 20000, 40000, 120000, 5000, 0),
]
for dealer_id, ex_showroom, discount, insurance, rto, accessories, other_charges in DEMO_QUOTES:
    save_quote(
        GROUP_ID,
        dealer_id,
        ex_showroom,
        discount,
        insurance,
        rto,
        accessories,
        other_charges,
    )

print(
    f"Demo data is ready: {car_count} cars, 3 dealers, "
    "14 of 20 buyers, and 3 offers."
)
