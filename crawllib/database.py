import sqlite3

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def dict_factory(cursor, row):
    d = dotdict()
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Database:
    
    def __init__(self, filename):
        self._db = sqlite3.connect(filename)
        self._db.row_factory = dict_factory


    def select(self, query, args={}):
        cur = self._db.cursor()
        cur.execute(query, args)
        return cur.fetchall()


    def first(self, query, args={}):
        cur = self._db.cursor()
        cur.execute(query, args)
        return cur.fetchone()


    def execute(self, query, args={}):
        cur = self._db.cursor()
        cur.execute(query, args)
        self.commit()


    def executescript(self, query):
        cur = self._db.cursor()
        cur.executescript(query)
        self.commit()


    def commit(self):
        self._db.commit()
