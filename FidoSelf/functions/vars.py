from FidoSelf import client
from FidoSelf.functions.helper import convert_date
from datetime import datetime
import random

FONTS = {
    1: "0,1,2,3,4,5,6,7,8,9",
    2: "０,１,２,３,４,５,６,７,８,９",
    3: "⓿,➊,➋,➌,➍,➎,➏,➐,➑,➒",
    4: "⓪,①,②,③,④,⑤,⑥,⑦,⑧,⑨",
    5: "𝟘,𝟙,𝟚,𝟛,𝟜,𝟝,𝟞,𝟟,𝟠,𝟡",
    6: "𝟬,𝟭,𝟮,𝟯,𝟰,𝟱,𝟲,𝟳,𝟴,𝟵",
    7: "𝟎,𝟏,𝟐,𝟑,𝟒,𝟓,𝟔,𝟕,𝟖,𝟗",
    8: "𝟢,𝟣,𝟤,𝟥,𝟦,𝟧,𝟨,𝟩,𝟪,𝟫",
    9: "₀,₁,₂,₃,₄,₅,₆,₇,₈,₉",
    10: "⁰,¹,²,³,⁴,⁵,⁶,⁷,⁸,⁹",
    11: "𝟶,𝟷,𝟸,𝟹,𝟺,𝟻,𝟼,𝟽,𝟾,𝟿",
    12: "⒪,⑴,⑵,⑶,⑷,⑸,⑹,⑺,⑻,⑼",
}

HEARTS = ["❤️", "💙", "💛", "💚", "🧡", "💜", "🖤", "🤍", "❣", "💕", "💞", "💔", "💗", "💖"]
COLORS = ["black", "white", "blue", "red", "yellow", "green", "purple", "orange", "brown", "pink", "gold", "fuchsia", "lime", "aqua", "skyblue", "gray"]

def create_font(newtime, timefont):
    if str(timefont) == "random2":
        for par in newtime:
            rfont = random.randint(1, len(FONTS))
            if par not in [":", "/"]:
                nfont = FONTS[int(rfont)].split(",")[int(par)]
                newtime = newtime.replace(par, nfont)
    else:
        if str(timefont) == "random":
            timefont = random.randint(1, len(FONTS))
        for par in newtime:
            if par not in [":", "/"]:
                nfont = FONTS[int(timefont)].split(",")[int(par)]
                newtime = newtime.replace(par, nfont)
    return newtime

async def get_vars(event):
    time = datetime.now()
    cdate = convert_date(int(time.strftime("%Y")), int(time.strftime("%m")), int(time.strftime("%d")))
    Vars = {
        "TIME": time.strftime("%H:%M"),
        "DATE": str(cdate[0]) + "/" + str(cdate[1]) + "/" + str(cdate[2]),
        "DAY": cdate[2],
        "MONTH": cdate[1],
        "YEAR": cdate[0],
        "HOUR": time.strftime("%H"),
        "MIN": time.strftime("%M"),
        "SEC": time.strftime("%S"),
     }
    timefont = client.DB.get_key("TIME_FONT") or 1
    NewVars = {}
    for Var in Vars:
        NewVars.update({"F" + str(Var): create_font(str(Vars[Var]), str(timefont))})
    Vars.update(NewVars)
    Vars.update({
        "STRDAY": time.strftime("%A"),
        "STRMONTH": time.strftime("%B"),
        })
    Vars.update({"HEART": random.choice(HEARTS)})
    emojies = client.DB.get_key("EMOJIES") or []
    if emojies:
        Vars.update({"EMOJI": random.choice(emojies)})
    if event:
        user = await event.get_sender()
        Vars.update({"FIRSTNAME": user.first_name})
        Vars.update({"LASTNAME": user.last_name})
        Vars.update({"USERNAME": user.username})
        me = await event.client.get_me()
        Vars.update({"MYFIRSTNAME": me.first_name})
        Vars.update({"MYLASTNAME": me.last_name})
        Vars.update({"MYUSERNAME": me.username})
        chat = await event.get_chat()
        Vars.update({"CHATTITLE": chat.title})
        Vars.update({"CHATUSERNAME": chat.username})
    return Vars

async def add_vars(text, event=None):
    Vars = await get_vars(event)
    for Var in Vars:
        text = text.replace("{" + str(Var) + "}", str(Vars[Var]))
    return text
