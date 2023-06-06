from FidoSelf import client
from telethon.types import Message
import re
import os

def check_cmd(event):
    if not event.text: return False
    commands = client.DB.get_key("SELFCOMMANDS") or []
    for command in commands:
        search = re.search(command, event.text)
        if search:
            return True
    return False

setattr(Message, "checkCmd", check_cmd)

async def DownloadFiles():
    os.mkdir("downloads")
    
    foshs = client.DB.get_key("FOSHS_FILE")
    if foshs:
        try:
            get = await client.get_messages(int(foshs["chat_id"]), ids=int(foshs["msg_id"]))
            await get.download_media(client.PATH + "FOSHS.txt")
        except:
            pass

    cover = client.DB.get_key("FILE_COVER")
    if cover:
        try:
            get = await client.get_messages(int(cover["chat_id"]), ids=int(cover["msg_id"]))
            await get.download_media(client.PATH + "Cover.png")
        except:
            pass

    photos = client.DB.get_key("PHOTOS")
    if photos:
        for photo in list(photos.keys()):
            try:
                get = await client.get_messages(int(photos[photo]["chat_id"]), ids=int(photos[photo]["msg_id"]))
                await get.download_media(client.PATH + photo)
            except:
                pass
            
    fonts = client.DB.get_key("FONTS")
    if fonts:
        for font in fonts:
            try:
                get = await client.get_messages(int(fonts[font]["chat_id"]), ids=int(fonts[font]["msg_id"]))
                await get.download_media(client.PATH + font)
            except:
                pass