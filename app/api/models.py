import sqlite3 as sql


def submit_to_db(db, expression, result):
    """
    Registers the expression-result pair to an SQLite3 database.

    :param db: SQLite3 database filename.
    :type db: str
    :param expression: Expression.
    :type expression: str
    :param result: Evaluated expression.
    :type result: str
    """
    print(expression)
    try:
        with sql.connect(db) as con:
            cur = con.cursor()
            cur.execute(
                'INSERT INTO history(expression, result) '
                'VALUES ("%s", "%s")' % (expression, result))
            con.commit()
    finally:
        con.close()


def get_history(db):
    """
    Returns all entries in the SQLite3 database.

    :param db: SQLite3 database filename.
    :type db: str
    """
    history = []
    try:
        with sql.connect(db) as con:
            cur = con.cursor()
            for row in cur.execute(
                    "SELECT id, expression, result "
                    "FROM history ORDER BY id DESC"):
                print(row)
                history.append({
                    'id': row[0], 'expression': row[1], 'result': row[2]})
    finally:
        con.close()

    return history
