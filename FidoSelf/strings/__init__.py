from FidoSelf import client
from googletrans import Translator
from googletrans.constants import LANGUAGES as LANGS

LANGUAGES = {}

def load_langs():
    for main in ["en", "fa"]:
        file = f"FidoSelf/strings/{main}.json"
        STRING = open(file, "r").read()
        STRING = eval(STRING)
        LANGUAGES[main] = STRING
        client.LOGS.info(f"• Language ( {main} ) Successfuly Added!")
        others = client.DB.get_key("INSTALL_LANGS") or []
        if others:
            for lang in others:
                install_lang(lang)
                client.LOGS.info(f"• Language ( {lang} ) Successfuly Installed!")

def install_lang(dest):
    if dest not in LANGS:
        return "NotFound"
    mode = "Installed"
    if dest in LANGUAGES:
        del LANGUAGES[dest]
        mode = "Updated"
    translator = Translator()
    NewLang = {}
    for object in LANGUAGES["en"]:
        result = LANGUAGES["en"][object]
        if isinstance(result, dict):
            newlist = {}
            for key in result:
                trjome = translator.translate(result[key], dest=dest)  
                newlist.update({key: trjome.text})
            NewLang.update({object: newlist})
        elif isinstance(result, str):
            trjome = translator.translate(result, dest=dest)  
            NewLang.update({object: trjome.text})
    LANGUAGES.update({dest: NewLang})
    return mode

def get_string(string):
    lang = client.lang
    STRING = LANGUAGES[lang]
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
