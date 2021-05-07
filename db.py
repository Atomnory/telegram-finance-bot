import os
from typing import Dict, List

import sqlite3

con = sqlite3.connect(os.path.join('db', 'budget.db'))
cur = con.cursor()


def insert_to_db(table: str, column_values: Dict) -> None:
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ', '.join('?' * len(column_values.keys()))
    cur.executemany(
        f'INSERT INTO {table}'
        f'({columns})'
        f'VALUES ({placeholders})',
        values
    )
    con.commit()


def fetchall_from_db(table: str, columns: List[str]) -> List[Dict]:
    columns_joined = ', '.join(columns)
    cur.execute(f'SELECT {columns_joined} FROM {table}')
    rows = cur.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def delete_from_db(table: str, row_id: int) -> None:
    row_id = int(row_id)  # TODO: ??? int -> int
    cur.execute(f'DELETE FROM {table} WHERE id={row_id}')
    con.commit()


def get_cursor():
    return cur


def _init_db():
    """ Initialize database by createdb.sql settings. """
    with open('createdb.sql', 'r') as f:
        sql = f.read()
    cur.executescript(sql)
    con.commit()


def check_db_exists():
    """ Check database exists. If not exist initialize one."""
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expense'")
    table_exists = cur.fetchall()
    if not table_exists:
        _init_db()


check_db_exists()
