from FidoSelf import client

MAINSTRINGS = {
    "EN": {
        "wait": "^{STR} Please Wait . . .$", 
    },
    "FA": {
        "wait": "^{STR} لطفا صبر کنید . . .$", 
    }
}

def get_string(STRINGS, string):
    lang = client.lang or "EN"
    if string in MAINSTRINGS[lang]:
        STRING = MAINSTRINGS[lang][string]
    else:
        STRING = STRINGS[lang][string]
    REPLACES = {
        "{STR}": client.STR,
        "{CMD}": client.CMD,
        "^": "**",
        "$": "**",
    }
    for replace in REPLACES:
        STRING = STRING.replace(replace, REPLACES[replace])
    return STRING
