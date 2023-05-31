from FidoSelf import client

def get_string(string, STRINGS=None, LANG=None):
    lang = LANG or client.LANG
    if STRINGS:
        STRING = STRINGS[lang][string]
    else:
        langfile = lang + ".json"
        MAINSTRINGS = open("FidoSelf/languages" + langfile, "r").read()
        MAINSTRINGS = eval(MAINSTRINGS)
        STRING = MAINSTRINGS[string]
    REPLACES = {
        "{STR}": client.STR,
        "{CMD}": client.CMD,
    }
    for replace in REPLACES:
        STRING = STRING.replace(replace, REPLACES[replace])
    return STRING
