import sqlite3
from flask import g
import json
from uuid import uuid4

DATABASE = "app.sqlite3"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    get_db().commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_all_particles():
    return query_db("SELECT * FROM particles")


def save_particle_config(name, config):
    uuid = str(uuid4())
    query_db(
        "INSERT INTO particles (uuid, name, config) VALUES (?, ?, ?)",
        (uuid, name, config),
        True,
    )
    return uuid


def get_particle_config(uuid):
    return query_db("SELECT * FROM particles WHERE uuid = ?", (uuid,), True)
