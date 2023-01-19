from FidoSelf import client

REPLACES = {
    "{STR}": client.STR,
    "{CMD}": client.CMD,
}

def get_string(STRINGS, string):
    lang = client.lang or "EN"
    STRING = STRINGS[lang][string]
    for replace in REPLACES:
        STRING = STRING.replace(replace, REPLACES[replace])
    return STRING
