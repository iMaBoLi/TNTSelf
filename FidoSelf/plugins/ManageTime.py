from FidoSelf import client
from telethon import functions, types
from PIL import Image, ImageDraw, ImageFont, ImageColor
from datetime import datetime
import aiocron
import random
import re
import os
os.system("pip install pycron")
import pycron

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

def create_font(newtime, font):
    for par in newtime:
        if par != ":":
            nfont = FONTS[int(font)].split(",")[int(par)].replace("⃣⃣", "⃣").replace("⃣⃣⃣", "⃣")
            newtime = newtime.replace(par, nfont)
    return newtime

async def namechanger():
    timefont = client.DB.get_key("TIME_FONT") or 1
    if str(timefont) == "random":
        timefont = random.randint(1, len(FONTS))
    newtime = datetime.now().strftime("%H:%M")
    time = create_font(newtime, timefont)
    NAMES = client.DB.get_key("NAMES") or []
    nmode = client.DB.get_key("NAME_MODE") or "off"
    while nmode == "on" and NAMES:
        if pycron.is_now('*/1 * * * *'): 
            chname = random.choice(NAMES).format(TIME=time, HEART=random.choice(HEARTS))
            try:
                await client(functions.account.UpdateProfileRequest(first_name=str(chname)))
            except:
                try:
                    await client(functions.account.UpdateProfileRequest(first_name="‌", last_name=str(chname)))
                except:
                    pass
            await client.send_message(client.backch, "Name Changed!")

async def namechangeruu():
    timefont = client.DB.get_key("TIME_FONT") or 1
    if str(timefont) == "random":
        timefont = random.randint(1, len(FONTS))
    newtime = datetime.now().strftime("%H:%M")
    time = create_font(newtime, timefont)
    NAMES = client.DB.get_key("NAMES") or []
    nmode = client.DB.get_key("NAME_MODE") or "off"
    if nmode == "on" and NAMES:
        chname = random.choice(NAMES).format(TIME=time, HEART=random.choice(HEARTS))
        try:
            await client(functions.account.UpdateProfileRequest(first_name=str(chname)))
        except:
            try:
                await client(functions.account.UpdateProfileRequest(first_name="‌", last_name=str(chname)))
            except:
                pass
    await client.send_message(client.backch, "Name Changed!")

async def biochanger():
    timefont = client.DB.get_key("TIME_FONT") or 1
    if str(timefont) == "random":
        timefont = random.randint(1, len(FONTS))
    newtime = datetime.now().strftime("%H:%M")
    time = create_font(newtime, timefont)
    BIOS = client.DB.get_key("BIOS") or []
    bmode = client.DB.get_key("BIO_MODE") or "off"
    if bmode == "on" and BIOS:
        chbio = random.choice(BIOS).format(TIME=time, HEART=random.choice(HEARTS))
        try:
            await client(functions.account.UpdateProfileRequest(about=str(chbio)))
        except:
            pass
    await client.send_message(client.backch, "Bio Changed!")

async def photochanger():
    time = datetime.now().strftime("%H:%M")
    PHOTOS = client.DB.get_key("PHOTOS") or {}
    FONTS = client.DB.get_key("FONTS") or {}
    TEXTS = client.DB.get_key("TEXT_TIMES") or []
    phmode = client.DB.get_key("PHOTO_MODE") or "off"
    if phmode == "on" and PHOTOS and TEXTS and FONTS:
        phname = random.choice(list(PHOTOS.keys()))
        phinfo = PHOTOS[phname]
        getphoto = await client.get_messages(int(phinfo["chat_id"]), ids=int(phinfo["msg_id"]))
        PHOTO = await getphoto.download_media()
        TEXT = random.choice(TEXTS).format(TIME=time)
        sizes = {"vsmall":20, "small":35, "medium":50, "big":70, "vbig":90}
        SIZE = sizes[phinfo["size"]]
        COLOR = info["color"]
        if COLOR == "random":
            COLOR = random.choice(COLORS)
        COLOR = ImageColor.getrgb(COLOR)
        img = Image.open(PHOTO)
        width, height = img.size
        if width > 640: width = 640
        if height > 640: height = 640
        ffont = info["font"]
        if ffont == "random":
            ffont = random.choice(list(FONTS.keys())) 
        getfont = await client.get_messages(FONTS[ffont]["chat_id"], ids=int(FONTS[ffont]["msg_id"]))
        ffont = await getfont.download_media()
        FONT = ImageFont.truetype(ffont, size)
        draw = ImageDraw.Draw(img)
        twidth, theight = draw.textsize(TEXT, font=FONT)
        newwidth, newheight = (width - twidth) / 2, (height - theight) / 2
        if phinfo["where"] == "↖️":
            newwidth, newheight = 20, 20
        elif phinfo["where"] == "⬆️":
            newwidth, newheight = (width - twidth) / 2, 20
        elif phinfo["where"] == "↗️":
            newwidth, newheight = (width - twidth) - 20, 20
        elif phinfo["where"] == "⬅️":
            newwidth, newheight = 20, (height - theight) /2
        elif phinfo["where"] == "➡️":
            newwidth, newheight = (width - twidth) - 20, (height - theight) / 2
        elif phinfo["where"] == "↙️":
            newwidth, newheight = 20, (height - theight) - 20
        elif phinfo["where"] == "⬇️":
            newwidth, newheight = (width - twidth) / 2, (height - theight) - 20
        elif phinfo["where"] == "↘️":
            newwidth, newheight = (width - twidth) - 20, (height - theight) - 20
        draw.text((newwidth, newheight), TEXT, COLOR, font=FONT, align=str(info["align"]))
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

client.loop.create_task(namechanger())
