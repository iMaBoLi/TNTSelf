from mega import Mega
import json
import os

Mega = Mega().login("FidoSelf@yahoo.com", "@F2022Sf")

MEGA_DATABASE_URL = None

class FidoDB:
    def __init__(self):
        self.recreate()
        fdata = open("FidoSelf/DataBase.json", "r")
        return fdata

    def recreate(self):
        file = Mega.find("DataBase.json")
        if not file:
            fdata = open("FidoSelf/DataBase.json", "w")
            json.dump({}, fdata, indent=6)
            fdata.close()
            Mega.upload("FidoSelf/DataBase.json")
        if not os.path.exists("FidoSelf/DataBase.json"):
            file = Mega.find("DataBase.json")
            Mega.download(file, "./FidoSelf")
    
    def reload(self):
        file = Mega.find("DataBase.json")
        Mega.delete(file[0])
        Mega.upload("FidoSelf/DataBase.json")   
    
    def set_key(self, key, value):
        fdata = open("FidoSelf/DataBase.json", "r")
        fdata.update({key: value})
        newdata = open("FidoSelf/DataBase.json", "w")
        json.dump(fdata, newdata, indent=6)
        fdata.close()
        newdata.close()
        self.reload()

    def del_key(self, key):
        fdata = open("FidoSelf/DataBase.json", "r")
        del fdata[key]
        newdata = open("FidoSelf/DataBase.json", "w")
        json.dump(fdata, newdata, indent=6)
        fdata.close()
        newdata.close()
        self.reload()

    def get_key(self, key):
        fdata = open("FidoSelf/DataBase.json", "r")
        gkey = fdata[key]
        fdata.close()
        return gkey

    def clean(self):
        fdata = open("FidoSelf/DataBase.json", "w")
        json.dump({}, fdata, indent=6)
        fdata.close()
        self.reload()

DB = FidoDB()
