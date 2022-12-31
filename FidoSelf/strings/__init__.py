from FidoSelf import client
import json

def get_string(string):
    lang = client.DB.get_key("LANGUAGE") or "en"
    STRS = open(f"FidoSelf/strings/{str(lang)}.txt", "r").read()
    STRING = json.loads(STRS)
    for page in string.split("_"):
        STRING = STRING[page]
    newstr = STRING
    if type(newstr) == str:
        newstr = newstr.replace("{STR}", client.str)
        newstr = newstr.replace("{CMD}", client.cmd)    
    return newstr
