import json
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
                print(type(dbdata))
                data = eval(dbdata)
        else:
            data = {}
            with open(self.dbname, "w") as dbfile:
                json.dump(data, dbfile, indent=4)
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
            json.dump(data, dbfile, indent=4)
        self.re_data()
        return True