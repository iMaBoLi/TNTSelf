from FidoSelf import client
import json

def get_string(string):
    lang = client.DB.get_key("LANGUAGE") or "en"
    STRS = open(f"FidoSelf/strings/{str(lang)}.txt", "r").read()
    STRS = json.loads(STRS)
    plugin = str(string.split("_")[0])
    count = str(string.split("_")[1])
    newstr = STRS[plugin][count]
    return newstr
