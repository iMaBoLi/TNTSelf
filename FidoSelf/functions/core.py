from FidoSelf import client
from telethon.types import Message
import re
import time
import os

def getstrings(STRINGS):
    NEWSTR = {}
    for element in STRINGS:
        text = STRINGS[element]
        if type(text) == str:
            STR = client.DB.get_key("EMOJI_SAMBOL") or "❃"
            CMD = client.DB.get_key("CMD_SAMBOL") or "."
            text = text.replace("{CMD}", CMD)
            text = f"**{STR}** " + text
        NEWSTR.update({element: text})
    return NEWSTR

def checkCmd(event, text=None):
    if not (event.text and text):
        return False
    text = text if text else event.text
    for command in client.COMMANDS:
        search = re.search(command, text)
        if search:
            return True
    return False

setattr(Message, "checkCmd", checkCmd)

SPAMS = {}

def checkSpam(event):
    bantime = 30
    maxtime = 4
    if event.sender_id not in SPAMS:
        SPAMS[event.sender_id] = {"next_time": int(time.time()) + maxtime, "messages": 0, "banned": 0}
        uspam = SPAMS[event.sender_id]
    else:
        uspam = SPAMS[event.sender_id]
        uspam["messages"] += 1
    if uspam["banned"] >= int(time.time()):
        return True
    else:
        if uspam["next_time"] >= int(time.time()):
            if uspam["messages"] >= 8:
                SPAMS[event.sender_id]["banned"] = int(time.time()) + bantime
                return True
        else:
            SPAMS[event.sender_id]["messages"] = 0
            SPAMS[event.sender_id]["next_time"] = int(time.time()) + maxtime
            return False

setattr(Message, "checkSpam", checkSpam)

def checkReply(event, medias=[]):
    message = None
    mediatype = client.functions.mediatype(event.reply_message)
    if event.is_reply:
        if not medias:
            return message
        if mediatype not in medias:
            if ("File" in medias and mediatype and mediatype.endswith("File")) or ("Photo" in medias and mediatype and mediatype.endswith("Photo")):
                return message
            message = ""
            for media in medias:
                message += media + " Or "
            message = message[:-4]
            message = client.STRINGS["reply"].format(message)
    else:
        message = "A Message"
        message = client.STRINGS["reply"].format(message)
    return message

setattr(Message, "checkReply", checkReply)

def checkAdmin(event, change_info=False, ban_users=False, invite_users=False, add_admins=False):
    chat = event.chat
    if chat.creator:
        return True
    if chat.left:
        return False
    if chat.admin_rights:
        rights = chat.admin_rights
        if change_info and not rights.change_info:
            return False
        if ban_users and not rights.ban_users:
            return False
        if invite_users and not rights.invite_users:
            return False
        if add_admins and not rights.add_admins:
            return False
        return True
    return False

setattr(Message, "checkAdmin", checkAdmin)

async def DownloadFiles():
    
    if not os.path.exists("downloads"):
        os.mkdir("downloads")
        
    foshs = client.DB.get_key("FOSHS_FILE")
    if foshs:
        try:
            get = await client.get_messages(int(foshs["chat_id"]), ids=int(foshs["msg_id"]))
            await get.download_media(client.PATH + "FOSHS.txt")
        except:
            pass
    logo = client.DB.get_key("LOGO_FILE")
    if logo:
        try:
            get = await client.get_messages(int(logo["chat_id"]), ids=int(logo["msg_id"]))
            await get.download_media(client.PATH + "Logo.png")
        except:
            pass
        
    cover = client.DB.get_key("FILE_COVER")
    if cover:
        try:
            get = await client.get_messages(int(cover["chat_id"]), ids=int(cover["msg_id"]))
            await get.download_media(client.PATH + "Cover.png")
        except:
            pass

    photos = client.DB.get_key("PHOTO_LIST")
    if photos:
        for photo in list(photos.keys()):
            try:
                get = await client.get_messages(int(photos[photo]["chat_id"]), ids=int(photos[photo]["msg_id"]))
                await get.download_media(client.PATH + photo)
            except:
                pass
            
    font = client.DB.get_key("FONT_FILE")
    if font:
        try:
            get = await client.get_messages(int(font["chat_id"]), ids=int(font["msg_id"]))
            await get.download_media(client.PATH + "FontFile.ttf")
        except:
            pass