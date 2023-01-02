from FidoSelf import client
from googletrans import Translator
import glob
import os

LANGUAGES = {}

def load_langs():
    langs = ["en", "fa", "fr"]
    for lang in langs:
        file = f"FidoSelf/strings/{lang}.yml"
        if os.path.exists(file):
            STRING = open(file, "r").read()
            STRING = eval(STRING)
            LANGUAGES[lang] = STRING
        else:
            STRING = open("FidoSelf/strings/en.yml", "r").read()           
            STRING = eval(STRING) 
            translator = Translator()
            trjome = translator.translate(STRING, dest=lang.lower())
            STRING = str(trjome.text)
            open(f"FidoSelf/strings/{lang}.yml", "w").write(STRING)
            #LANGUAGES[lang] = STRING

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
