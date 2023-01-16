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

REMOVEDSTRS = {
    "\n": "{LINE}",
    "?": "{SOAL}",
}

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
                ttext = result[key]
                for tr in REMOVEDSTRS:
                    ttext = ttext.replace(tr, REMOVEDSTRS[tr]) 
                trjome = translator.translate(ttext, dest=dest)  
                ntext = trjome.text
                for tr in REMOVEDSTRS:
                    ntext = ntext.replace(REMOVEDSTRS[tr], tr) 
                newlist.update({key: ntext})
            NewLang.update({object: newlist})
        elif isinstance(result, str):
            ttext = result
            for tr in REMOVEDSTRS:
                ttext = ttext.replace(tr, REMOVEDSTRS[tr]) 
            trjome = translator.translate(result, dest=dest) 
            ntext = trjome.text
            for tr in REMOVEDSTRS:
                ntext = ntext.replace(REMOVEDSTRS[tr], tr)  
            NewLang.update({object: ntext})
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
