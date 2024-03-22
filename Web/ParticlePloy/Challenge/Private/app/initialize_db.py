import sqlite3


db = sqlite3.connect("app.sqlite3")
db.execute(
    "CREATE TABLE IF NOT EXISTS particles (uuid TEXT, name TEXT, config TEXT, approved BOOLEAN DEFAULT FALSE)"
)
