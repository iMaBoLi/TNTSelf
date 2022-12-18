from redis import Redis
from self import config
import psycopg2

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
        
    def flushall(self):
        for x in self.keys():
            self.del_key(x)
        return True


class SqlDB:
    def __init__(self):
        self._url = "postgres://fidoself_user:kNsbkuu1VXeJgOnhwpf0tuCDnSFCIC3Y@dpg-ceffufhgp3jk7mhbm63g-a.frankfurt-postgres.render.com/fidoself"
        self._connection = None
        self._cursor = None
        try:
            self._connection = psycopg2.connect(dsn=url)
            self._connection.autocommit = True
            self._cursor = self._connection.cursor()
            self._cursor.execute(
                "CREATE TABLE IF NOT EXISTS Ultroid (ultroidCli varchar(70))"
            )
        except Exception as error:
            print(error)
            print("Invaid SQL Database")
            if self._connection:
                self._connection.close()
            sys.exit()
        self.re_cache()

    @property
    def name(self):
        return "SQL"

    @property
    def usage(self):
        self._cursor.execute(
            "SELECT pg_size_pretty(pg_relation_size('Ultroid')) AS size"
        )
        data = self._cursor.fetchall()
        return int(data[0][0].split()[0])

    def re_cache(self):
        self._cache = {}
        for key in self.keys():
            self._cache.update({key: self.get_key(key)})

    def keys(self):
        self._cursor.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name  = 'ultroid'"
        )  # case sensitive
        data = self._cursor.fetchall()
        return [_[0] for _ in data]

    def ping(self):
        return True

    def get_key(self, variable):
        if variable in self._cache:
            return self._cache[variable]
        get_ = get_data(self, variable)
        self._cache.update({variable: get_})
        return get_

    def get(self, variable):
        try:
            self._cursor.execute(f"SELECT {variable} FROM Ultroid")
        except psycopg2.errors.UndefinedColumn:
            return None
        data = self._cursor.fetchall()
        if not data:
            return None
        if len(data) >= 1:
            for i in data:
                if i[0]:
                    return i[0]

    def set_key(self, key, value):
        try:
            self._cursor.execute(f"ALTER TABLE Ultroid DROP COLUMN IF EXISTS {key}")
        except (psycopg2.errors.UndefinedColumn, psycopg2.errors.SyntaxError):
            pass
        except BaseException as er:
            print(er)
        self._cache.update({key: value})
        self._cursor.execute(f"ALTER TABLE Ultroid ADD {key} TEXT")
        self._cursor.execute(f"INSERT INTO Ultroid ({key}) values (%s)", (str(value),))
        return True

    def del_key(self, key):
        if key in self._cache:
            del self._cache[key]
        try:
            self._cursor.execute(f"ALTER TABLE Ultroid DROP COLUMN {key}")
        except psycopg2.errors.UndefinedColumn:
            return False
        return True

    delete = del_key

    def flushall(self):
        self._cache.clear()
        self._cursor.execute("DROP TABLE Ultroid")
        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS Ultroid (ultroidCli varchar(70))"
        )
        return True

    def rename(self, key1, key2):
        _ = self.get_key(key1)
        if _:
            self.del_key(key1)
            self.set_key(key2, _)
            return 0
        return 1

DB = RedisDB()
DB.s = SqlDB()
