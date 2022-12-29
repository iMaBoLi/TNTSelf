from FidoSelf import client
from FidoSelf.functions.helper import convert_date
from datetime import datetime
import datetime as date
import random
import os

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

def get_vars():
    fatime = datetime.now()
    entime = datetime.now(date.timezone.utc)
    cdate = convert_date(int(entime.strftime("%Y")), int(entime.strftime("%m")), int(entime.strftime("%d")))
    timefont = client.DB.get_key("TIME_FONT") or 1
    VARS = {
        "ENSTRDAY": entime.strftime("%A"),
        "ENSTRMONTH": entime.strftime("B"),
        "FADAY": cdate[2],
        "FAMONTH": cdate[1],
        "FAYEAR": cdate[0],
        "FADATE": cdate[0] + "/" + cdate[1] + "/" + cdate[2],
        "FATIMES": fatime.strftime("%H:%M"),
        "FASEC": fatime.strftime("%S"),
        "FAMIN": fatime.strftime("%M"),
        "FAHOUR": fatime.strftime("%H"),
        "ENSTRDAY": entime.strftime("%A"),
        "ENSTRMONTH": entime.strftime("%B"),
        "ENDAY": entime.strftime("%d"),
        "ENMONTH": entime.strftime("%m"),
        "ENYEAR": entime.strftime("%Y"),
        "ENDATE": entime.strftime("%F").replace("-", "/"),
        "ENTIMES": entime.strftime("%H:%M"),
        "ENSEC": entime.strftime("%S"),
        "ENMIN": entime.strftime("%M"),
        "ENHOUR": entime.strftime("%H"),
     }
    NewVars = {}
    for Var in Vars:
        NewVars.update({"F-" + str(Var): create_font(Vars[Var], timefont)})
    Vars += NewVars
    Vars.update({"HEART": random.choice(HEARTS)})
    return VARS
