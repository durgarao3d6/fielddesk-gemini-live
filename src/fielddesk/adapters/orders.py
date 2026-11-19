import sqlite3
from contextlib import closing


class SQLiteOrders:
    def __init__(self, path):
        self.path = path

    def save(self, order):
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id TEXT PRIMARY KEY,
                    asset TEXT NOT NULL,
                    symptom TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            db.execute(
                "INSERT INTO orders(id, asset, symptom) VALUES (?, ?, ?) "
                "ON CONFLICT(id) DO NOTHING",
                (order["id"], order["asset"], order["symptom"]),
            )
        return {"created": True, **order}
