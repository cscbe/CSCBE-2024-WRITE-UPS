import sqlite3

DATABASE = "../app/app.sqlite3"

con = sqlite3.connect(DATABASE)
con.row_factory = sqlite3.Row


def query_db(query, args=(), one=False):
    cur = con.execute(query, args)
    rv = cur.fetchall()
    con.commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_all_particles():
    return query_db("SELECT * FROM particles")


def get_unapproved_particles():
    return query_db("SELECT * FROM particles WHERE approved = FALSE")


def mark_particle_approved(uuid):
    query_db("UPDATE particles SET approved = TRUE WHERE uuid = ?", (uuid,))
