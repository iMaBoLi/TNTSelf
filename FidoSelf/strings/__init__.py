from FidoSelf import client
import glob

LANGUAGES = {}

def load_langs():
    for file in glob.glob("FidoSelf/strings/*.yml"):
        STRS = open(file, "r").read()
        STRING = eval(STRS)
        lang = file.split("/")[-1].split(".")[0]
        LANGUAGES[lang] = STRING

def get_string(string):
    lang = client.lang
    if not LANGUAGES:
        load_langs()
    STRING = LANGUAGES[lang]
    for page in string.split("_"):
        STRING = STRING[page]
    newstr = STRING
    if type(newstr) == str:
        newstr = newstr.replace("{STR}", client.str)
        newstr = newstr.replace("{CMD}", client.cmd)    
    return newstr

def get_buttons(buttons):
    if client.lang == "fa":
        buttons = client.utils.reverse(buttons)
    elif client.lang == "en":
        buttons = buttons
    return buttons
