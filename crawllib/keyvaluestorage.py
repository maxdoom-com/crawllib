from .database import Database

class KeyValueStorage(Database):
    """A simple key-value storage.

    Create a store:
    db.create("Tests", "foo", "bar", "blub")

    Drop a store:
    db.drop("Tests")

    Store key/value pairs:
    db.store("Tests", "test-1-2-3", {"foo":1, "bar":2, "blub":3})
    db.store("Tests", "test-1-2-3", {"foo":3, "bar":2, "blub":1})
    db.store("Tests", "test-1-2-3 A", {"foo":1, "bar":2, "blub":3})

    Remove an entry:
    db.remove("Tests", "test-1-2-3 A")
    
    Print a record:
    print(db.get("Tests", "test-1-2-3"))

    Get all entries:
    for entry in db.all(self, store):
        print(entry)

    Clear a store:
    db.empty("Tests")
    """

    def drop(self, store):
        self.execute(f"""DROP TABLE IF EXISTS {store}""")
        self.commit()

    def create(self, store, *fields):
        _fields = ", ".join(fields)
        self.execute(f"""CREATE TABLE IF NOT EXISTS {store} ( key UNIQUE PRIMARY KEY, {_fields} )""")
        self.commit()

    def store(self, store, key, data):
        entry = self.get(store, key)
        if entry:
            _placeholders = ", ".join([ f"{k}=:{k}" for k in data.keys() ])
            data['key'] = key
            self.execute(f"""UPDATE {store} SET {_placeholders} WHERE key=:key""", data)
        else:
            _fields = ", ".join([ k for k in data.keys() ])
            _placeholders = ", ".join([ f":{k}" for k in data.keys() ])
            data['key'] = key
            self.execute(f"""INSERT INTO {store} (key, {_fields}) VALUES (:key, {_placeholders})""", data)
        self.commit()
        return self.get(store, key)

    def remove(self, store, key):
        self.execute(f"""DELETE FROM {store} WHERE key=:key""", { "key": key })
        self.commit()

    def empty(self, store):
        self.execute(f"""DELETE FROM {store}""", {})
        self.commit()

    def get(self, store, key):
        return self.first(f"""SELECT * FROM {store} WHERE key=:key""", { "key": key })

    def all(self, store):
        return self.select(f"SELECT * FROM {store}")

    def filter(self, store, constraints):
        where = []
        for key in constraints.keys():
            where.append( f"{key}=:{key}" )
        where = " AND ".join(where)
        return self.select(f"SELECT * FROM {store} WHERE {where}", constraints)
