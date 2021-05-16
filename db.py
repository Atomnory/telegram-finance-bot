from typing import Dict, List
import psycopg2
from services import config

con = psycopg2.connect(database=config.database,
                       user=config.user,
                       password=config.password,
                       host=config.host,
                       port=config.port)
cur = con.cursor()


def insert_to_db(table: str, column_values: Dict) -> None:
    columns = ', '.join(column_values.keys())
    val = list(column_values.values())

    cur.executemany(f"INSERT INTO {table} ({columns}) "
                    f"VALUES(%s, %s, %s, %s, %s, %s);",
                    (val, ))
    con.commit()


def fetchall_from_db(table: str, columns: List[str]) -> List[Dict]:
    columns_joined = ', '.join(columns)
    cur.execute(f'SELECT {columns_joined} FROM {table};')
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
    cur.execute(f'DELETE FROM {table} WHERE id={row_id};')
    con.commit()


def get_cursor():
    return cur


def _init_db():
    """ Initialize database by createdb.sql settings. """
    with open('createdb.sql', 'r') as f:
        sql = f.read()
    cur.execute(sql)
    con.commit()


def check_db_exists():
    """ Check database exists. If not exist initialize one."""
    cur.execute("SELECT * FROM information_schema.tables WHERE table_name='expense';")
    table_exists = cur.fetchall()
    if not table_exists:
        _init_db()


check_db_exists()
