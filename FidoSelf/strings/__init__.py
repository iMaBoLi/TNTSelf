from FidoSelf import client
import glob

LANGUAGES = {}

for file in glob.glob("FidoSelf/strings/*.json"):
    STRING = open(file, "r").read()
    lang = file.split("/")[-1].split(".")[0]
    LANGUAGES[lang] = STRING

def get_string(string):
    lang = client.lang
    STRING = LANGUAGES[lang]
    for page in string.split("_"):
        STRING = STRING[page]
    if type(STRING) == str:
        STRING = STRING.replace("{STR}", client.str)
        STRING = STRING.replace("{CMD}", client.cmd)    
    return STRING

def get_buttons(buttons):
    if client.lang == "fa":
        buttons = client.utils.reverse(buttons)
    elif client.lang == "en":
        buttons = buttons
    return buttons
