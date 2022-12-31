from FidoSelf import client

def get_string(string):
    lang = client.DB.get_key("LANGUAGE") or "en"
    STRS = open(f"FidoSelf/strings/{str(lang)}.yml", "r").read()
    STRING = eval(STRS)
    for page in string.split("_"):
        STRING = STRING[page]
    newstr = STRING
    if type(newstr) == str:
        newstr = newstr.replace("{STR}", client.str)
        newstr = newstr.replace("{CMD}", client.cmd)    
    return newstr
