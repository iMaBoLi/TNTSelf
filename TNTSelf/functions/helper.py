from TNTSelf import client
from traceback import format_exc
from telethon.types import Message
import asyncio
import time
import math
import random
import os

def progress(event, download=False, upload=False, filename=None):
    newtime = time.time()
    if download and not filename:
        if event.file:
            filename = event.file.name
        elif event.to_dict().get("reply_message", None) and event.reply_message and event.reply_message.file:
            filename = event.reply_message.file.name
    callback = lambda current, total: client.loop.create_task(create_progress(event, current, total, newtime, download, upload, filename))
    return callback

setattr(Message, "progress", progress)
setattr(client, "progress", progress)

async def create_progress(event, current, total, start, download=False, upload=False, filename=None):
    filename = " " + filename if filename else ""
    if download:
        strmode = client.STRINGS["progress"]["Down"] + filename + " ..."
    elif upload:
        strmode = client.STRINGS["progress"]["Up"] + filename + " ..."
    duration = time.time() - start
    if duration != 0 and round(duration % 7.00) == 0 or current == total:
        perc = current * 100 / total
        speed = current / duration
        speed = speed if speed else 1
        eta = round((total - current) / speed) * 1000
        strings = "".join("▰" for i in range(math.floor(perc / 5)))
        strings += "".join("▱" for i in range(20 - len(strings)))
        text = client.STRINGS["progress"]["Text"].format(strmode, strings, round(perc, 2), client.functions.convert_bytes(current), client.functions.convert_bytes(total), client.functions.convert_bytes(speed), client.functions.convert_time(eta), client.functions.convert_time(duration))
        await event.edit(text)

async def getuserid(event, number=1):
    userid = 0
    inputs = event.text.split(" ")
    if len(inputs) > number:
        match = inputs[number]
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
    return int(userid)

async def getchatid(event, number=1):
    chatid = 0
    inputs = event.text.split(" ")
    if len(inputs) > number:
        match = inputs[number]
        inputid = int(match) if match.isdigit() else str(match)
        try:
            chatinfo = await client.get_entity(inputid)
            if chatinfo.to_dict()["_"] in ["Channel", "Group"]:
                chatid = chatinfo.id
        except:
            pass
    elif not event.is_private:
        chatid = event.chat_id
    return int(chatid)

def mention(info, coustom=None):
    if not coustom:
        coustom = f"{info.first_name} {info.last_name}" if info.last_name else info.first_name
    return f"[{coustom}](tg://user?id={info.id})"

def mediatype(event):
    if not event or not event.file: return None
    if event.photo:
        filetype = "JPG Photo"
    elif event.video:
        if event.video_note:
            filetype = "VideoNote"
        elif event.gif or event.file.mime_type == "image/gif":
            filetype = "Gif"
        elif event.file.mime_type == "video/webm":
            filetype = "VSticker"
        else:
            filetype = "Video"
    elif event.voice:
        filetype = "Voice"
    elif event.audio:
        filetype = "Music"
    elif event.sticker:
        if event.file.mime_type == "image/webp":
            filetype = "Sticker"
        elif event.file.mime_type == "application/x-tgsticker":
            filetype = "ASticker"
    elif event.document:
        mimetype = event.file.mime_type
        TYPES = {
            "image/jpeg": "JPG Photo",
            "image/png": "PNG Photo",
            "font/ttf": "TTF File",
            "text/plain": "TXT File",
            "application/zip": "ZIP File",
            "application/vnd.android.package-archive": "APP File",
        }
        filetype = TYPES[mimetype] if mimetype in TYPES else "File"
    return filetype

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
    plugcat = info["Category"]
    plugname = info["Name"]
    pluginfo = info["Info"]
    pluginfo.update({"Category": plugcat})
    client.HELP.update({plugname: pluginfo})