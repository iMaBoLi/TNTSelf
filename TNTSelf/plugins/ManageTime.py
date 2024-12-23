from TNTSelf import client
from telethon import functions, types
from jdatetime import datetime
import aiocron
import random
import os

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

def add_items(client, text, font=True):
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
            nVAR = create_font(VARS[VAR], tfont)
        else:
            nVAR = VARS[VAR]
        text = text.replace(VAR, nVAR)
    return text

async def namechanger():
    for sinclient in client.clients:
        NAME_LIST = sinclient.DB.get_key("NAME_LIST")
        nmode = sinclient.DB.get_key("NAME_MODE") or "OFF"
        if nmode == "ON" and NAME_LIST:
            chname = add_items(client, random.choice(NAME_LIST))
            try:
                await sinclient(functions.account.UpdateProfileRequest(first_name=str(chname)))
            except:
                pass

async def biochanger():
    for sinclient in client.clients:
        BIO_LIST = sinclient.DB.get_key("BIO_LIST")
        bmode = sinclient.DB.get_key("BIO_MODE") or "OFF"
        if bmode == "ON" and BIO_LIST:
            chbio = add_items(client, random.choice(BIO_LIST))
            try:
                await sinclient(functions.account.UpdateProfileRequest(about=str(chbio)))
            except:
                pass

aiocron.crontab("*/1 * * * *", func=namechanger)
aiocron.crontab("*/30 * * * *", func=biochanger)