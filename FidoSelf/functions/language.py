from FidoSelf import client

MAINSTRINGS = {}

def ADDSTRINGS():
    MAINSTRINGS = {}
    files = ["EN.json", "FA.json"]
    for file in files:
        lang = file.split(".")[0]
        STRINGS = open("FidoSelf/languages/" + file, "r").read()
        STRINGS = eval(STRINGS)
        MAINSTRINGS = MAINSTRINGS | {lang: STRINGS}
        return MAINSTRINGS
        
def get_string(string, STRINGS=None, LANG=None):
    global MAINSTRINGS
    lang = LANG or client.LANG
    if STRINGS:
        STRING = STRINGS[lang][string]
    else:
        if not MAINSTRINGS:
            MAINSTRINGS = ADDSTRINGS()
        STRING = MAINSTRINGS[string]
    REPLACES = {
        "{STR}": client.STR,
        "{CMD}": client.CMD,
    }
    for replace in REPLACES:
        STRING = STRING.replace(replace, REPLACES[replace])
    return STRING
