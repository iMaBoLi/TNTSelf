from FidoSelf import client
from telethon.types import Message
import re
import time
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

SPAMS = {}

def checkspam(event):
    bantime = 30
    maxtime = 3
    if event.sender_id not in SPAMS:
        SPAMS[event.sender_id] = {"next_time": time.time() + maxtime, "messages": 1, "banned": 0}
        uspam = SPAMS[event.sender_id]
    else:
        uspam = SPAMS[event.sender_id]
        uspam["messages"] += 1
    if uspam["banned"] >= time.time():
        return True
    else:
        if uspam["next_time"] >= int(time.time()):
            if uspam["messages"] >= 5:
                SPAMS[event.sender_id]["banned"] = int(time.time()) + bantime
                return True
        else:
            SPAMS[event.sender_id]["messages"] = 1
            SPAMS[event.sender_id]["next_time"] = int(time.time()) + maxtime
            return False

setattr(Message, "checkSpam", checkspam)

async def DownloadFiles():
    data = client.DB.get_key("DATABASE")
    if data:
        try:
            get = await client.get_messages(int(data["chat_id"]), ids=int(data["msg_id"]))
            await get.download_media("DB.json")
        except:
            pass

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