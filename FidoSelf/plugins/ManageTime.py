from FidoSelf import client
from telethon import functions, types
from PIL import Image, ImageDraw, ImageFont, ImageColor
import aiocron
import random
import os

@aiocron.crontab("*/1 * * * *")
async def namechanger():
    NAMES = client.DB.get_key("NAMES")
    nmode = client.DB.get_key("NAME_MODE") or "off"
    if nmode == "on" and NAMES:
        chname = client.vars(random.choice(NAMES))
        try:
            await client(functions.account.UpdateProfileRequest(first_name=str(chname)))
        except:
            try:
                await client(functions.account.UpdateProfileRequest(first_name=".", last_name=str(chname)))
            except:
                pass

@aiocron.crontab("*/1 * * * *")
async def biochanger():
    BIOS = client.DB.get_key("BIOS")
    bmode = client.DB.get_key("BIO_MODE") or "off"
    if bmode == "on" and BIOS:
        chbio = await client.vars(random.choice(BIOS))
        try:
            await client(functions.account.UpdateProfileRequest(about=str(chbio)))
        except:
            pass

@aiocron.crontab("*/1 * * * *")
async def photochanger():
    PHOTOS = client.DB.get_key("PHOTOS")
    FONTS = client.DB.get_key("FONTS")
    TEXTS = client.DB.get_key("TEXT_TIMES")
    phmode = client.DB.get_key("PHOTO_MODE") or "off"
    if phmode == "on" and PHOTOS and TEXTS and FONTS:
        phname = random.choice(list(PHOTOS.keys()))
        phinfo = PHOTOS[phname]
        getphoto = await client.get_messages(int(phinfo["chat_id"]), ids=int(phinfo["msg_id"]))
        PHOTO = await getphoto.download_media()
        TEXT = await client.vars(random.choice(TEXTS))
        sizes = {"vsmall":20, "small":35, "medium":50, "big":70, "vbig":90}
        SIZE = sizes[phinfo["size"]]
        COLOR = phinfo["color"]
        if COLOR == "random":
            COLOR = random.choice(COLORS)
        COLOR = ImageColor.getrgb(COLOR)
        img = Image.open(PHOTO)
        width, height = img.size
        if width > 640: width = 640
        if height > 640: height = 640
        ffont = phinfo["font"]
        if ffont == "random":
            ffont = random.choice(list(FONTS.keys())) 
        getfont = await client.get_messages(FONTS[ffont]["chat_id"], ids=int(FONTS[ffont]["msg_id"]))
        ffont = await getfont.download_media()
        FONT = ImageFont.truetype(ffont, SIZE)
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
        draw.text((newwidth, newheight), TEXT, COLOR, font=FONT, align=str(phinfo["align"]))
        img.save("NEWPROFILE.jpg")
        try:
            phfile = await client.upload_file("NEWPROFILE.jpg")
            await client(functions.photos.UploadProfilePhotoRequest(file=phfile))
            pphoto = (await client.get_profile_photos("me"))[1]
            await client(functions.photos.DeletePhotosRequest(id=[types.InputPhoto(id=pphoto.id, access_hash=pphoto.access_hash, file_reference=pphoto.file_reference)]))
        except:
            pass
        os.remove("NEWPROFILE.jpg")
        os.remove(PHOTO)
        os.remove(ffont)
