import sqlite3
import re


def db_rows2dict(cursor, row) -> dict:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_rows_dict(cursor, sql, params) -> list:
    rows = cursor.execute(sql, params).fetchall()
    return rows


def get_row_dict(cursor, sql, params) -> dict:
    rows = cursor.execute(sql, params).fetchone()
    return rows


class Db(object):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = db_rows2dict

    def get_rows(self, sql, params=()) -> list:
        return get_rows_dict(self.conn.cursor(), sql, params)

    def get_row(self, sql, params=()) -> dict:
        return get_row_dict(self.conn.cursor(), sql, params)

    def get_one_val(self, sql, params=()) -> str:
        def find_one_select(x: str) -> str:
            tmp = 'SELECT(.*)FROM'
            return str(re.findall(tmp, x.strip())[0]).strip()
        return get_row_dict(self.conn.cursor(), sql, params).get(find_one_select(sql))

    def exec(self, sql, params=()) -> None:
        self.conn.cursor().execute(sql, params)

    def commit(self):
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()


if __name__ == '__main__':
    pass
