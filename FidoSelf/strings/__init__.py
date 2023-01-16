from FidoSelf import client
from googletrans import Translator
from googletrans.constants import LANGUAGES as LANGS

LANGUAGES = {}
MAINLANGS = ["en", "fa"]

def load_langs():
    for main in MAINLANGS:
        file = f"FidoSelf/strings/{main}.json"
        STRING = open(file, "r").read()
        STRING = eval(STRING)
        LANGUAGES[main] = STRING
        client.LOGS.info(f"• Language ( {main} ) Successfuly Added!")

RMSTRS = {
    "\n": "{LI_NE}",
    "?": "{SO_AL}",
    ".": "{NOGH_TE}",
}

def translate(text, lang):
    translator = Translator()
    for STR in RMSTRS:
        text = text.replace(STR, RMSTRS[STR]) 
    trjome = translator.translate(text, dest=lang) 
    trtext = trjome.text
    for STR in RMSTRS:
        trtext = trtext.replace(RMSTRS[STR], STR)  
    return trtext

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
                trtext = translate(result[key], dest)
                newlist.update({key: trtext})
            NewLang.update({object: newlist})
        elif isinstance(result, str):
            trtext = translate(result, dest)
            NewLang.update({object: trtext})
    LANGUAGES.update({dest: NewLang})
    return mode

def get_string(string):
    lang = client.lang
    try:
        STRING = LANGUAGES[lang]
        for page in string.split("_"):
            STRING = STRING[page]
        if isinstance(STRING, str):
            STRING = STRING.replace("{STR}", client.str)
            STRING = STRING.replace("{CMD}", client.cmd)
        return STRING
    except Exception as e:
        client.loop.create_task(client.send_message("me", str(e)))
        STRING = LANGUAGES["en"]
        for page in string.split("_"):
            STRING = STRING[page]
        if isinstance(STRING, str):
            STRING = translate(STRING, lang)
            STRING = STRING.replace("{STR}", client.str)
            STRING = STRING.replace("{CMD}", client.cmd)
        return STRING

def get_buttons(buttons):
    if client.lang in ["fa", "ar"]:
        buttons = client.utils.reverse(buttons)
    else:
        buttons = buttons
    return buttons
