from FidoSelf import client
from googletrans import Translator
import glob

LANGUAGES = {}

def load_langs():
    for file in glob.glob("FidoSelf/strings/*.json"):
        STRING = open(file, "r").read()
        lang = file.split("/")[-1].split(".")[0]
        STRING = eval(STRING)
        LANGUAGES[lang] = STRING

def get_string(string):
    lang = client.lang
    if not LANGUAGES:
        load_langs()
    if lang in LANGUAGES:
        STRING = LANGUAGES[lang]
        for page in string.split("_"):
            STRING = STRING[page]
        if type(STRING) == str:
            STRING = STRING.replace("{STR}", client.str)
            STRING = STRING.replace("{CMD}", client.cmd)    
        return STRING
    else:
        STRING = LANGUAGES["en"]
        for page in string.split("_"):
            STRING = STRING[page]
        if type(STRING) == str:
            STRING = STRING.replace("{STR}", client.str)
            STRING = STRING.replace("{CMD}", client.cmd)
        translator = Translator()
        dest = lang.lower()
        STRING = translator.translate(STRING, dest=dest)  
        return STRING

def get_buttons(buttons):
    if client.lang in ["fa"]:
        buttons = client.utils.reverse(buttons)
    else:
        buttons = buttons
    return buttons
