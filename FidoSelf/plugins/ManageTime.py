from FidoSelf import client
from telethon import functions, types
from PIL import Image, ImageDraw, ImageFont, ImageColor
from datetime import datetime
import aiocron
import random
import os
import re
import requests

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
TIMER = {
    1:{
        1: "🕐",
        2: "🕑",
        3: "🕒",
        4: "🕓",
        5: "🕔",
        6: "🕕",
        7: "🕖",
        8: "🕗",
        9: "🕘",
        10: "🕙",
        11: "🕚",
        12: "🕛"
    },
    2:{
        1: "🕜",
        2: "🕝",
        3: "🕞",
        4: "🕟",
        5: "🕠",
        6: "🕡",
        7: "🕢",
        8: "🕣",
        9: "🕤",
        10: "🕥",
        11: "🕦",
        12: "🕧"
    }
}
HEARTS = ["❤️", "💙", "💛", "💚", "🧡", "💜", "🖤", "🤍", "❣", "💕", "💞", "💔", "💗", "💖"]

COLORS = ["black", "white", "blue", "red", "yellow", "green", "purple", "orange", "brown", "pink", "gold", "fuchsia", "lime", "aqua", "skyblue", "gray"]

def create_font(newtime, font):
    for par in newtime:
        if par != ":":
            nfont = FONTS[int(font)].split(",")[int(par)].replace("⃣⃣", "⃣").replace("⃣⃣⃣", "⃣")
            newtime = newtime.replace(par, nfont)
    return newtime

@aiocron.crontab("*/1 * * * *")
async def timechanger():
    NAMES = client.DB.get_key("NAMES") or []
    BIOS = client.DB.get_key("BIOS") or []
    timefont = client.DB.get_key("TIME_FONT") or 1
    if str(timefont) == "random":
        timefont = random.randint(1, len(FONTS))
    newtime = datetime.now().strftime("%H:%M")
    hours = newtime.split(":")[0]
    mins = newtime.split(":")[1]
    gtimer = hours
    if int(hours) > 12:
        gtimer = int(hours) - 12
    elif hours.startswith("0"):
        gtimer = hours[1:]
    if int(hours) == 0:
        gtimer = 12
    timer = TIMER[2][int(gtimer)] if int(mins) > 29 else TIMER[1][int(gtimer)]
    time = create_font(newtime, timefont)
    hours = create_font(hours, timefont)
    mins = create_font(mins, timefont)
    dateen = datetime.now().strftime("%F").replace("-", "/")
    datefa = client.DB.get_key("DATE_FA") or "-"
    if datefa == "-" or newtime == "00:00":
        datefa = (requests.get("http://api.codebazan.ir/time-date/?json=en").json())["result"]["date"]
        client.DB.set_key("DATE_FA", datefa)
    wname = datetime.now().strftime("%A")
    if client.DB.get_key("NAME_MODE") and client.DB.get_key("NAME_MODE") == "on" and NAMES:
        chname = random.choice(NAMES)
        chname = chname.format(TIME=time, HEART=random.choice(HEARTS), TIMER=timer, HOURS=hours, MINS=mins, DATEEN=dateen, DATEFA=datefa, WEEK=wname)
        try:
            await client(functions.account.UpdateProfileRequest(first_name=str(chname)))
        except:
            try:
                await client(functions.account.UpdateProfileRequest(first_name="‌", last_name=str(chname)))
            except:
                pass
    if client.DB.get_key("BIO_MODE") and client.DB.get_key("BIO_MODE") == "on" and BIOS:
        chbio = random.choice(BIOS)
        chbio = chbio.format(TIME=time, HEART=random.choice(HEARTS), TIMER=timer, HOURS=hours, MINS=mins, DATEEN=dateen, DATEFA=datefa, WEEK=wname)
        try:
            await client(functions.account.UpdateProfileRequest(about=str(chbio)))
        except:
            pass
    PHOTOS = client.DB.get_key("PHOTOS") or {}
    FONTS = client.DB.get_key("FONTS") or {}
    TEXTS = client.DB.get_key("TEXT_TIMES") or []
    if client.DB.get_key("PHOTO_MODE") and client.DB.get_key("PHOTO_MODE") == "on" and PHOTOS and TEXTS and FONTS:
        phname = random.choice(list(PHOTOS.keys()))
        info = PHOTOS[phname] 
        chatid = int(info["chat_id"])
        msgid = int(info["msg_id"])
        get = await client.get_messages(chatid, ids=msgid)
        photo = await get.download_media()
        TEXT = random.choice(TEXTS)
        TEXT = TEXT.format(TIME=newtime, HOURS=hours, MINS=mins, DATEEN=dateen, DATEFA=datefa, WEEK=wname)
        sizes = {"vsmall":20, "small":35, "medium":50, "big":70, "vbig":90}
        size = sizes[info["size"]]
        color = info["color"]
        if color == "random":
            color = random.choice(COLORS)
        color = ImageColor.getrgb(color)
        img = Image.open(photo)
        width, height = img.size
        if width > 640:
            width = 640
        if height > 640:
            height = 640
        ffont = info["font"]
        if ffont == "random":
            ffont = random.choice(list(FONTS.keys()))
        chatid = FONTS[ffont]["chat_id"]
        msgid = FONTS[ffont]["msg_id"]
        get = await client.get_messages(chatid, ids=msgid)
        ffont = await get.download_media()
        font = ImageFont.truetype(ffont, size)
        draw = ImageDraw.Draw(img)
        twidth, theight = draw.textsize(TEXT, font=font)
        newwidth, newheight = (width - twidth) / 2, (height - theight) / 2
        if info["where"] == "↖️":
            newwidth, newheight = 20, 20
        elif info["where"] == "⬆️":
            newwidth, newheight = (width - twidth) / 2, 20
        elif info["where"] == "↗️":
            newwidth, newheight = (width - twidth) - 20, 20
        elif info["where"] == "⬅️":
            newwidth, newheight = 20, (height - theight) /2
        elif info["where"] == "➡️":
            newwidth, newheight = (width - twidth) - 20, (height - theight) / 2
        elif info["where"] == "↙️":
            newwidth, newheight = 20, (height - theight) - 20
        elif info["where"] == "⬇️":
            newwidth, newheight = (width - twidth) / 2, (height - theight) - 20
        elif info["where"] == "↘️":
            newwidth, newheight = (width - twidth) - 20, (height - theight) - 20
        draw.text((newwidth, newheight), TEXT, color, font=font, align=str(info["align"]))
        img.save("NEWPROFILE.jpg")
        try:
            phfile = await client.upload_file("NEWPROFILE.jpg")
            await client(functions.photos.UploadProfilePhotoRequest(file=phfile))
            pphoto = (await client.get_profile_photos("me"))[1]
            await client(functions.photos.DeletePhotosRequest(id=[types.InputPhoto(id=pphoto.id, access_hash=pphoto.access_hash, file_reference=pphoto.file_reference)]))
        except:
            pass
        os.remove("NEWPROFILE.jpg")
        os.remove(photo)
        os.remove(ffont)

timechanger.start()
