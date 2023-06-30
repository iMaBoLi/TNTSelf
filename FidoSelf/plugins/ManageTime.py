from FidoSelf import client
from telethon import functions, types
from PIL import Image, ImageDraw, ImageFont, ImageColor
from jdatetime import datetime
import aiocron
import random
import os

def AddVars(text, font=True):
    jtime = datetime.now()
    VARS = {
        "TIME": jtime.strftime("%H:%M"),
        "DATE": jtime.strftime("%Y") + "/" + jtime.strftime("%m") + "/" + jtime.strftime("%d"),
        "DAY": jtime.strftime("%A"),
        "MONTH": jtime.strftime("%B"),
        "HEART": random.choice(client.functions.HEARTS),
    }
    tfont = client.DB.get_key("TIME_FONT") or 1
    for VAR in VARS:
        if font:
            nVAR = client.functions.create_font(VARS[VAR], tfont)
        else:
            nVAR = VARS[VAR]
        text = text.replace(VAR, nVAR)
    return text

async def namechanger():
    NAMES = client.DB.get_key("NAMES")
    nmode = client.DB.get_key("NAME_MODE") or "OFF"
    if nmode == "ON" and NAMES:
        chname = AddVars(random.choice(NAMES))
        try:
            await client(functions.account.UpdateProfileRequest(first_name=str(chname)))
        except:
            pass

async def biochanger():
    BIOS = client.DB.get_key("BIOS")
    bmode = client.DB.get_key("BIO_MODE") or "OFF"
    if bmode == "ON" and BIOS:
        chbio = AddVars(random.choice(BIOS))
        try:
            await client(functions.account.UpdateProfileRequest(about=str(chbio)))
        except:
            pass

def get_photos():
    PHOTOS = client.DB.get_key("PHOTOS") or {}
    phots = []
    for photo in PHOTOS:
        phots.append(photo)
    return phots

def get_where(where, width, height):
    WHERES = {
        "↖️": [20, 20],
        "⬆️": [(width - twidth) / 2, 20],
        "↗️": [(width - twidth) - 20, 20],
        "⬅️": [20, (height - theight) /2],
        "⏺": [(width - twidth) / 2, (height - theight) / 2],
        "➡️": [(width - twidth) - 20, (height - theight) / 2],
        "↙️": [20, (height - theight) - 20],
        "⬇️": [(width - twidth) / 2, (height - theight) - 20],
        "↘️": [(width - twidth) - 20, (height - theight) - 20],
    }
    return WHERES[where][0], WHERES[where][1]

async def photochanger():
    PHOTOS = get_photos()
    TEXTS = client.DB.get_key("TEXT_TIMES")
    FONT = client.PATH + "FontFile.ttf"
    phmode = client.DB.get_key("PHOTO_MODE") or "OFF"
    if phmode == "ON" and PHOTOS and TEXTS and os.path.exists(FONT):
        PHOTO = random.choice(PHOTOS)
        FPHOTO = client.PATH + PHOTO
        phinfo = client.DB.get_key("PHOTOS")[PHOTO]
        TEXT = AddVars(random.choice(TEXTS), font=False)
        sizes = {"verysmall":20, "small":35, "medium":50, "big":70, "verybig":90}
        SIZE = sizes[phinfo["Size"]]
        COLOR = phinfo["Color"]
        if COLOR == "Random":
            COLOR = random.choice(client.functions.COLORS)
        COLOR = ImageColor.getrgb(COLOR)
        img = Image.open(FPHOTO)
        img = img.resize((640, 640))
        width, height = img.size
        FONT = ImageFont.truetype(FONT, SIZE)
        draw = ImageDraw.Draw(img)
        twidth, theight = draw.textsize(TEXT, font=FONT)
        newwidth, newheight = get_where(phinfo["Where"], width, height)
        draw.text((newwidth, newheight), TEXT, COLOR, font=FONT, align=str(phinfo["Align"]))
        img.save(client.PATH + "NEWPROFILE.jpg")
        try:
            phfile = await client.upload_file(client.PATH + "NEWPROFILE.jpg")
            await client(functions.photos.UploadProfilePhotoRequest(file=phfile))
            pphoto = (await client.get_profile_photos("me"))[1]
            await client(functions.photos.DeletePhotosRequest(id=[types.InputPhoto(id=pphoto.id, access_hash=pphoto.access_hash, file_reference=pphoto.file_reference)]))
        except:
            pass
        os.remove(client.PATH + "NEWPROFILE.jpg")

aiocron.crontab("*/1 * * * *", func=namechanger)
aiocron.crontab("*/1 * * * *", func=biochanger)
aiocron.crontab("*/1 * * * *", func=photochanger)