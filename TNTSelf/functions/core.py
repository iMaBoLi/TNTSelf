from TNTSelf import client
from telethon import functions
from telethon.types import Message
import re
import time
import os
import shutil

def create_font(newtime, timefont):
    newtime = str(newtime)
    if str(timefont) == "random2":
        for par in newtime:
            fonts = [1,3,4,5,6,7,8,9,10,11,12]
            rfont = random.choice(fonts)
            if par.isdigit():
                nfont = client.functions.FONTS[int(rfont)].split(",")[int(par)]
                newtime = newtime.replace(par, nfont)
            fonts.remove(rfont)
    else:
        if str(timefont) == "random":
            fonts = list(range(1, len(client.functions.FONTS)+2))
            timefont = random.choice(fonts)
        for par in newtime:
            if par.isdigit():
                nfont = client.functions.FONTS[int(timefont)].split(",")[int(par)]
                newtime = newtime.replace(par, nfont)
    return newtime

def getstrings(STRINGS):
    NEWSTR = {}
    for element in STRINGS:
        text = STRINGS[element]
        if type(text) == str:
            STR = client.DB.get_key("EMOJI_SIMBEL") or "❃"
            CMD = client.DB.get_key("CMD_SIMBEL") or "."
            text = text.replace("{STR}", STR)
            text = text.replace("{CMD}", CMD)
        NEWSTR.update({element: text})
    return NEWSTR

def checkCmd(text):
    if not text: return False
    for command in client.COMMANDS:
        search = re.search(command, text)
        if search:
            return True
    return False

SPAMS = {}
def checkSpam(event, bantime=30, maxbans=3, maxtime=3, maxmsg=6, block=False):
    antimode = client.DB.get_key("ANTI_SPAM") or "ON"
    if antimode == "OFF":
        return False
    if event.sender_id not in SPAMS:
        SPAMS[event.sender_id] = {"next_time": int(time.time()) + maxtime, "messages": 0, "banned": 0, "bancount": 0}
        uspam = SPAMS[event.sender_id]
    else:
        uspam = SPAMS[event.sender_id]
        uspam["messages"] += 1
    if uspam["banned"] >= int(time.time()):
        return True
    else:
        if uspam["next_time"] >= int(time.time()):
            if uspam["messages"] >= maxmsg:
                SPAMS[event.sender_id]["banned"] = int(time.time()) + bantime
                SPAMS[event.sender_id]["bancount"] += 1
                if SPAMS[event.sender_id]["bancount"] >= maxbans:
                    if block:
                        client.loop.create_task(client(functions.contacts.BlockRequest(event.sender_id)))
                    else:
                        blacks = client.DB.get_key("BLACK_LIST") or []
                        blacks.append(event.sender_id)
                        client.DB.set_key("BLACK_LIST", blacks)
                    SPAMS[event.sender_id]["bancount"] = 0
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