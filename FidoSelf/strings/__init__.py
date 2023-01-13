from FidoSelf import client
from googletrans import Translator

LANGUAGES = {}
MAINLANGS = ["en", "fa"]
OTHERLANGS = ["ar", "fr", "it", "ru", "ko"]

def load_langs():
    for main in MAINLANGS:
        file = f"FidoSelf/strings/{main}.json"
        STRING = open(file, "r").read()
        STRING = eval(STRING)
        LANGUAGES[main] = STRING
        client.LOGS.info(f"• Language ( {main} ) Successfuly Added From File!")
    for dest in OTHERLANGS:
        translator = Translator()
        Main = LANGUAGES["en"]
        NewLang = {}
        for obj in Main:
            if isinstance(obj, dict):
                newlist = {}
                for key in obj:
                    trjome = translator.translate(obj[key], dest=dest)  
                    newlist.update({key: trjome.text})
                NewLang.update({obj: newlist})
            elif isinstance(obj, str):
                trjome = translator.translate(Main[obj], dest=dest)  
                NewLang.update({obj: trjome.text})
        LANGUAGES.update({dest: NewLang})
        client.LOGS.info(f"• Language ( {dest} ) Successfuly Added By Translate!")

def get_string(string):
    lang = client.lang
    STRING = LANGUAGES[lang]
    for page in string.split("_"):
        STRING = STRING[page]
    STRING = eval(STRING)
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
