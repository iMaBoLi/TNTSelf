from TNTSelf import client
from telethon import functions, types
from jdatetime import datetime
import aiocron
import random
import os

def AddVars(text, font=True):
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
            nVAR = client.functions.create_font(VARS[VAR], tfont)
        else:
            nVAR = VARS[VAR]
        text = text.replace(VAR, nVAR)
    return text

async def namechanger():
    NAME_LIST = client.DB.get_key("NAME_LIST")
    nmode = client.DB.get_key("NAME_MODE") or "OFF"
    if nmode == "ON" and NAME_LIST:
        chname = AddVars(random.choice(NAME_LIST))
        try:
            await client.do(functions.account.UpdateProfileRequest(first_name=str(chname)))
        except:
            pass

async def biochanger():
    BIO_LIST = client.DB.get_key("BIO_LIST")
    bmode = client.DB.get_key("BIO_MODE") or "OFF"
    if bmode == "ON" and BIO_LIST:
        chbio = AddVars(random.choice(BIO_LIST))
        try:
            await client.do(functions.account.UpdateProfileRequest(about=str(chbio)))
        except:
            pass

aiocron.crontab("*/1 * * * *", func=namechanger)
aiocron.crontab("*/30 * * * *", func=biochanger)