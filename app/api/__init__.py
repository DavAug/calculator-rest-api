import os
import sqlite3 as sql

from .calculator import calculate, get_schema  # noqa
from .models import submit_to_db, get_history  # noqa


def init_history_database(testing):
    """
    Creates a SQLite3 database which stores submitted
    requests and responses and returns its filename.

    :param testing: A boolean flag that indicates whether this is a test
        initialisation.
    :type testing: bool

    :rtype: str
    """
    db = 'test.db' if testing else 'database.db'
    if os.path.exists(db):
        # Database exist already
        return db

    # Create database
    try:
        with sql.connect(db) as con:
            cur = con.cursor()
            cur.execute(
                "CREATE TABLE history( "
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "expression TEXT NOT NULL, "
                "result TEXT NOT NULL)")
            con.commit()
    finally:
        con.close()

    return db
