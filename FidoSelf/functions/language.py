from FidoSelf import client

MAINSTRINGS = {
    "EN": {
        "wait": "^{STR} Please Wait . . .$", 
        "On": "Actived",
        "Off": "DeActived",
    },
    "FA": {
        "wait": "^{STR} لطفا صبر کنید . . .$", 
        "On": "فعال شد",
        "Off": "غیر فعال شد",
    }
}

def get_string(string, STRINGS=None, LANG="EN"):
    lang = client.LANG or LANG
    if STRINGS:
        STRING = STRINGS[lang][string]
    else:
        STRING = MAINSTRINGS[lang][string]
    REPLACES = {
        "{STR}": client.STR,
        "{CMD}": client.CMD,
        "^": "**",
        "$": "**",
    }
    for replace in REPLACES:
        STRING = STRING.replace(replace, REPLACES[replace])
    return STRING
