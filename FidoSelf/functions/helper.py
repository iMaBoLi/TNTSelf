from FidoSelf import client
from traceback import format_exc
from telethon.types import Message
from telethon.errors.rpcerrorlist import UsernameInvalidError
from jdatetime import datetime
from jdatetime import date as jdate
import asyncio
import time
import math

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

async def getuserid(event, inputid=None):
    userid = None
    result = False
    if inputid:
        inputid = int(inputid) if inputid.isdigit() else str(inputid)
        try:
            userid =  await client.get_peer_id(inputid)
            result = True
        except (UsernameInvalidError, ValueError):
            userid = "Invalid"
        except:
            userid = None
    elif event.reply_message:
        userid = event.reply_message.sender_id
        result = True
    elif event.is_private:
        userid = event.chat_id
        result = True
    return result, userid

async def getchatid(event, inputid=None):
    chatid = None
    result = False
    if inputid:
        inputid = int(inputid) if inputid.isdigit() else str(inputid)
        try:
            chatid =  await client.get_peer_id(inputid)
            result = True
        except (UsernameInvalidError, ValueError):
            userid = "Invalid"
        except:
            userid = None
    else:
        chatid = event.chat_id
        result = True
    return result, chatid

setattr(Message, "userid", getuserid)
setattr(Message, "chatid", getchatid)

def mention(info, coustom=None):
    if not coustom:
        coustom = f"{info.first_name} {info.last_name}" if info.last_name else info.first_name
    return f"[{coustom}](tg://user?id={info.id})"

def mediatype(event):
    type = None
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

def convert_date(year, month, day):
    gregorian_date = datetime(year, month, day)
    shamsi_date = jdate.fromgregorian(date=gregorian_date)
    shamsi = f"{shamsi_date.year}/{shamsi_date.month}/{shamsi_date.day}"
    return shamsi