from FidoSelf import client

def get_string(STRINGS, string):
    lang = client.lang or "EN"
    STRING = STRINGS[lang][string]
    REPLACES = {
        "{STR}": client.STR,
        "{CMD}": client.CMD,
    }
    for replace in REPLACES:
        STRING = STRING.replace(replace, REPLACES[replace])
    return STRING
