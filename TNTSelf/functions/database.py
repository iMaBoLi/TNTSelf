import os

class DATABASE:
    def __init__(self, userid):
        self.userid = userid
        self.dbname = "../tmp/TNTDB.json"
        self.cache = {}
        self.re_data()

    def get_data(self):
        if os.path.isfile(self.dbname):
            with open(self.dbname, "r") as dbdata:
                data = eval(dbdata.read())
        else:
            data = {}
            with open(self.dbname, "w") as dbfile:
                dbfile.write(str(data))
        return data

    def re_data(self):
        data = self.get_data()
        if self.userid not in data:
            data.update({self.userid: {}})
            self.save(data)
        self.cache = data

    def set_key(self, key, value):
        data = self.cache
        data[self.userid].update({key: value})
        return self.save(data)
        
    def del_key(self, key):
        data = self.cache
        if key in data[self.userid]:
            del data[self.userid][key]
            return self.save(data)
            
    def get_key(self, key):
        if key in self.cache[self.userid]:
            return self.cache[self.userid].get(key)
        
    def save(self, data):
        with open(self.dbname, "w") as dbfile:
            dbfile.write(str(data))
        self.re_data()
        return True