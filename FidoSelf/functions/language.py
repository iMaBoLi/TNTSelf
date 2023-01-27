from FidoSelf import client

MAINSTRINGS = {
    "EN": {
        "wait": "^{STR} Please Wait . . .$", 
    },
    "FA": {
        "wait": "^{STR} لطفا صبر کنید . . .$", 
    }
}

def get_string(string, STRINGS=None):
    lang = client.LANG or "EN"
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
