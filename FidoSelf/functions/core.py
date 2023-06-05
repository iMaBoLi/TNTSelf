from FidoSelf import client
from telethon.types import Message
import re

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
    foshs = client.DB.get_key("FOSHS_FILE")
    if foshs:
        try:
            get = await client.get_messages(int(foshs["chat_id"]), ids=int(foshs["msg_id"]))
            await get.download_media("FOSHS.txt")
        except:
            pass

    cover = client.DB.get_key("FILE_COVER")
    if cover:
        try:
            get = await client.get_messages(int(cover["chat_id"]), ids=int(cover["msg_id"]))
            await get.download_media("Cover.png")
        except:
            pass

    photos = client.DB.get_key("PHOTOS")
    if photos:
        for photo in photos:
            try:
                get = await client.get_messages(int(photos[photo]["chat_id"]), ids=int(PHOTOS[photo]["msg_id"]))
                await get.download_media(photo)
            except:
                pass
            
    fonts = client.DB.get_key("FONTS")
    if fonts:
        for font in fonts:
            try:
                get = await client.get_messages(int(fonts[font]["chat_id"]), ids=int(fonts[font]["msg_id"]))
                await get.download_media(font)
            except:
                pass