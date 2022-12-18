from redis import Redis
from self import config
import psycopg2
import sys

def get_data(self, key):
    data = self.get(str(key))
    if data:
        try:
            data = eval(data)
        except BaseException:
            pass
    return data

class RedisDB:
    def __init__(self):
        URL = (config.REDIS_URL).split(":")[0]
        PORT = (config.REDIS_URL).split(":")[-1]
        self.db = Redis(
                host=URL,
                password=config.REDIS_PASSWORD,
                port=int(PORT),
                decode_responses=True,
                socket_timeout=5,
                retry_on_timeout=True,
            )
        self.set = self.db.set
        self.get = self.db.get
        self.keys = self.db.keys
        self.ping = self.db.ping
        self.delete = self.db.delete
        self.recache()

    def recache(self):
        self.cache = {}
        for keys in self.keys():
            self.cache.update({keys: self.get_key(keys)})

    @property
    def name(self):
        return "Redis"

    @property
    def usage(self):
        allusage = 0
        for x in self.keys():
            usage = self.db.memory_usage(x)
            allusage += usage
        return allusage

    def set_key(self, key, value):
        value = str(value)
        try:
            value = eval(value)
        except BaseException:
            pass
        self.cache.update({key: value})
        return self.set(str(key), str(value))

    def get_key(self, key):
        if key in self.cache:
            return self.cache[key]
        get = get_data(self, key)
        self.cache.update({key: get})
        return get

    def del_key(self, key):
        if key in self.cache:
            del self.cache[key]
        return bool(self.delete(str(key)))
        
    def clean(self):
        for x in self.keys():
            self.del_key(x)
        return True

class SqlDB:
    def __init__(self, dbname="FidoSelf"):
        self.url = config.SQL_URL
        self.dbname = dbname
        self.connection = psycopg2.connect(dsn=self.url)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {dbname} ()")
        self.re_cache()

    @property
    def name(self):
        return "SQL"

    @property
    def usage(self):
        self.cursor.execute(f"SELECT pg_size_pretty(pg_relation_size('{self.dbname}')) AS size")
        data = self.cursor.fetchall()
        return int(data[0][0].split()[0])

    def re_cache(self):
        self.cache = {}
        for key in self.keys():
            self.cache.update({key: self.get_key(key)})

    def keys(self):
        self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name  = '{self.dbname}'")
        data = self.cursor.fetchall()
        return [key[0] for key in data]

    def get_key(self, variable):
        if variable in self.cache:
            return self.cache[variable]
        get = get_data(self, variable)
        self.cache.update({variable: get})
        return get

    def get(self, variable):
        try:
            self.cursor.execute(f"SELECT {variable} FROM {self.dbname}")
        except psycopg2.errors.UndefinedColumn:
            return None
        data = self.cursor.fetchall()
        if not data:
            return None
        if len(data) >= 1:
            for i in data:
                if i[0]:
                    return i[0]

    def set_key(self, key, value):
        try:
            self.cursor.execute(f"ALTER TABLE {self.dbname} DROP COLUMN IF EXISTS {key}")
        except (psycopg2.errors.UndefinedColumn, psycopg2.errors.SyntaxError):
            pass
        except BaseException as er:
            print(er)
        self.cache.update({key: value})
        self.cursor.execute(f"ALTER TABLE {self.dbname} ADD {key} TEXT")
        self.cursor.execute(f"INSERT INTO {self.dbname} ({key}) values ({str(value)})")
        return True

    def del_key(self, key):
        if key in self.cache:
            del self.cache[key]
        try:
            self.cursor.execute(f"ALTER TABLE {self.dbname} DROP COLUMN {key}")
        except psycopg2.errors.UndefinedColumn:
            return False
        return True

    def clean(self):
        self.cache.clear()
        self.cursor.execute(f"DROP TABLE {self.dbname}")
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.dbname} ()")
        return True

DB = RedisDB()
DB.s = SqlDB()
