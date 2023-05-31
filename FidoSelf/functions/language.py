from FidoSelf import client

MAINSTRINGS = {}

def ADDSTRINGS():
    files = ["EN.json", "FA.json"]
    for file in files:
        STRINGS = open(file, "r").read()
        STRINGS = eval(STRINGS)
        MAINSTRINGS += STRINGS

def get_string(string, STRINGS=None, LANG=None):
    lang = LANG or client.LANG
    if STRINGS:
        STRING = STRINGS[lang][string]
    else:
        if not MAINSTRINGS:
            ADDSTRINGS()
        STRING = MAINSTRINGS[string]
    REPLACES = {
        "{STR}": client.STR,
        "{CMD}": client.CMD,
    }
    for replace in REPLACES:
        STRING = STRING.replace(replace, REPLACES[replace])
    return STRING
