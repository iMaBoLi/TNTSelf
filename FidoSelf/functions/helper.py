from FidoSelf import client
from traceback import format_exc
from telethon.types import Message
import asyncio
import time
import math
import random

def progress(event, download=False, upload=False):
    newtime = time.time()
    callback = lambda start, end: client.loop.create_task(
        create_progress(
            event,
            start,
            end,
            newtime,
            download,
            upload,
         )
    )
    return callback

setattr(Message, "progress", progress)
setattr(client, "progress", progress)

async def create_progress(event, current, total, start, download=False, upload=False):
    if download:
        type = client.STRINGS["progress"]["Down"]
    elif upload:
        type = client.STRINGS["progress"]["Up"]
    else:
        type = "-----"
    diff = time.time() - start
    if round(diff % 8.00) == 0 or current == total:
        perc = current * 100 / total
        speed = current / diff
        eta = round((total - current) / speed) * 1000
        pstrs = "".join("■" for i in range(math.floor(perc / 5)))
        fstrs = "".join("□" for i in range(20-len(pstrs)))
        rperc = str(round(perc))
        if len(rperc) < 3 and int(rperc[-1]) > 4:
            rstrs = "◧"
        elif len(rperc) < 3 and int(rperc[-1]) < 4:
            rstrs = "□"
        else:
            rstrs = "■" 
        strs = pstrs + rstrs + fstrs
        text = client.STRINGS["progress"]["Text"].format(type, strs, round(perc, 2), client.functions.convert_bytes(current), client.functions.convert_bytes(total), client.functions.convert_bytes(speed), client.functions.convert_time(eta))
        await event.edit(text)

async def getuserid(event, match=None):
    userid = None
    if match:
        inputid = int(match) if match.isdigit() else str(match)
        try:
            userinfo = await client.get_entity(inputid)
            if userinfo.to_dict()["_"] == "User":
                userid = userinfo.id
        except:
            pass
    elif event.reply_message:
        userid = event.reply_message.sender_id
    elif event.is_private:
        userid = event.chat_id
    return userid

setattr(Message, "userid", getuserid)

async def getchatid(event, match=None):
    chatid = None
    if match:
        inputid = int(match) if match.isdigit() else str(match)
        try:
            chatinfo = await client.get_entity(inputid)
            if chatinfo.to_dict()["_"] in ["Channel", "Group"]:
                chatid = chatinfo.id
        except:
            pass
    elif not event.is_private:
        chatid = event.chat_id
    return chatid

setattr(Message, "chatid", getchatid)

def mention(info, coustom=None):
    if not coustom:
        coustom = f"{info.first_name} {info.last_name}" if info.last_name else info.first_name
    return f"[{coustom}](tg://user?id={info.id})"

def mediatype(event):
    type = None
    if not event:
        return type
    if event.photo:
        type = "Photo"
    elif event.video:
        if event.video_note:
            type = "VideoNote"
        elif event.gif or event.file.mime_type == "image/gif":
            type = "Gif"
        elif event.file.mime_type == "video/webm":
            type = "ASticker"
        else:
            type = "Video"
    elif event.voice:
        type = "Voice"
    elif event.audio:
        type = "Music"
    elif event.sticker:
        if event.file.mime_type == "image/webp":
            type = "Sticker"
        elif event.file.mime_type == "application/x-tgsticker":
            type = "ASticker"
    elif event.document:
        if event.document.mime_type == "image/png":
            type = "Photo"
        else:
            type = "File"
    return type

setattr(Message, "mediatype", mediatype)

async def save(event):
    if client.BACKUP:
        forward = await event.forward_to(client.BACKUP)
        info = {"chat_id": client.BACKUP, "msg_id": forward.id}
    else:
        forward = await event.forward_to(client.me.id)
        info = {"chat_id": client.me.id, "msg_id": forward.id}
    return info

setattr(Message, "save", save)

def AddInfo(info):
    category = info["Category"]
    pluginname = info["Plugname"]
    plugininfo = info["Pluginfo"]
    if category not in client.HELP:
        client.HELP.update({category: {}})
    client.HELP[category][pluginname] = plugininfo

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