from TNTSelf import client
from telethon import functions, types
from jdatetime import datetime
import aiocron
import random
import os


def add_items(sinclient, text, font=True):
    jtime = datetime.now()
    VARS = {
        "TIME": jtime.strftime("%H:%M"),
        "DATE": jtime.strftime("%Y") + "/" + jtime.strftime("%m") + "/" + jtime.strftime("%d"),
        "DAY": jtime.strftime("%A"),
        "MONTH": jtime.strftime("%B"),
        "HEART": random.choice(client.functions.HEARTS),
    }
    tfont = sinclient.DB.get_key("TIME_FONT") or 1
    for VAR in VARS:
        if font:
            nVAR = client.functions.create_font(VARS[VAR], tfont)
        else:
            nVAR = VARS[VAR]
        text = text.replace(VAR, nVAR)
    return text

async def namechanger():
    for sinclient in client.clients:
        NAME_LIST = sinclient.DB.get_key("NAME_LIST")
        nmode = sinclient.DB.get_key("NAME_MODE") or "OFF"
        if nmode == "ON" and NAME_LIST:
            chname = add_items(sinclient, random.choice(NAME_LIST))
            sname = chname.split("/")
            fname = sname[0]
            lname = sname[1] if len(sname) > 1 else ""
            try:
                await sinclient(functions.account.UpdateProfileRequest(first_name=fname, last_name=lname))
            except:
                pass

async def biochanger():
    for sinclient in client.clients:
        BIO_LIST = sinclient.DB.get_key("BIO_LIST")
        bmode = sinclient.DB.get_key("BIO_MODE") or "OFF"
        if bmode == "ON" and BIO_LIST:
            chbio = add_items(sinclient, random.choice(BIO_LIST))
            try:
                await sinclient(functions.account.UpdateProfileRequest(about=str(chbio)))
            except:
                pass

aiocron.crontab("*/1 * * * *", func=namechanger)
aiocron.crontab("*/10 * * * *", func=biochanger)