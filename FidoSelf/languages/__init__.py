from FidoSelf import client

LANGUAGES = {}
MAINLANGS = ["en", "fa"]

def load_langs():
    for main in MAINLANGS:
        file = f"FidoSelf/languages/{main}.json"
        STRING = open(file, "r").read()
        STRING = eval(STRING)
        LANGUAGES[main] = STRING
        client.LOGS.info(f"• Language ( {main} ) Successfuly Added!")

def get_string(string):
    lang = client.lang
    SRRING = LANGUAGES[lang]
    for page in string.split("_"):
        STRING = STRING[page]
    if isinstance(STRING, str):
        STRING = STRING.replace("{STR}", client.str)
        STRING = STRING.replace("{CMD}", client.cmd)
    return STRING

def get_buttons(buttons):
    if client.lang in ["fa", "ar"]:
        buttons = client.utils.reverse(buttons)
    else:
        buttons = buttons
    return buttons
