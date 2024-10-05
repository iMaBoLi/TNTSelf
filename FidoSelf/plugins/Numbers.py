from FidoSelf import client
from telethon import events
import aiocron
import asyncio
import re

STRINGS = {
    "change": "**{STR} The Find Number For Bot** ( `{}` ) **Has Been {}!**",
}

@client.Command(command="Find(Seller|Ir|Sms|Venus) (On|Off)")
async def findnumber(event):
    await event.edit(client.STRINGS["wait"])
    bot = event.pattern_match.group(1).upper()
    change = event.pattern_match.group(2).upper()
    client.DB.set_key(f"FINDNUM{bot}_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(bot, showchange))

@client.on(events.NewMessage(from_users=[6892848909]))
async def seller(event):
    fmode = client.DB.get_key("FINDNUMSELLER_MODE") or "OFF"
    if fmode == "OFF": return
    country = "🇺🇿 ازبکستان"
    ranges = "9985"
    if "موفقیت دریافت شد" in event.raw_text:
        if ranges not in event.raw_text:
            text = "#New_Number - @" + client.me.username + "\n\n" + event.raw_text
            await client.bot.send_message(client.REALM, text)
            await event.respond(country)
    if "مشکلی پیش آمد " in event.raw_text:
        await event.respond(country)

@client.on(events.MessageEdited(from_users=[6892848909]))
async def editseller(event):
    fmode = client.DB.get_key("FINDNUMSELLER_MODE") or "OFF"
    if fmode == "OFF": return
    country = "🇺🇿 ازبکستان"
    if "سفارش با موفقیت لغو شد" in event.raw_text:
        await event.respond(country)

async def cancelsellernums():
    fmode = client.DB.get_key("FINDNUMSELLER_MODE") or "OFF"
    if fmode == "OFF": return
    await client.bot.send_message(client.REALM, "text")
    query = "Number :"
    async for message in client.iter_messages(6892848909, search=query, limit=30):
        ranges = "9985"
        if ranges in message.raw_text:
            await message.click(1)

aiocron.crontab("*/20 * * * * *", func=cancelsellernums)

@client.on(events.MessageEdited(from_users=[7100598907]))
async def venus(event):
    fmode = client.DB.get_key("FINDNUMVENUS_MODE") or "OFF"
    if fmode == "OFF": return
    country = "🔄 تکرار آخرین خرید"
    if "شماره با موفقیت دریافت گردید" in event.raw_text:
        phone = re.search("\\+(\\d*)", event.raw_text)
        text = f"[#New_Number](@{client.me.username}) \n\n `+{phone}`"
        await client.bot.send_message(client.REALM, text)
    await asyncio.sleep(2)
    await event.respond(country)

@client.on(events.NewMessage(from_users=[5044250099]))
async def irbot(event):
    fmode = client.DB.get_key("FINDNUMIR_MODE") or "OFF"
    if fmode == "OFF": return
    country = "ازبکستان,🇺🇿"
    ranges = "998 5"
    if "#شماره_فعال" in event.raw_text:
        if ranges in event.raw_text:
            await event.click(1)
        else:
            text = "#New_Number - @" + client.me.username + "\n\n" + event.raw_text
            await client.bot.send_message(client.REALM, text)
        await event.respond(country)
    if "یافت نشد" in event.raw_text:
        await event.respond(country)
    
async def cancelirnums():
    fmode = client.DB.get_key("FINDNUMIR_MODE") or "OFF"
    if fmode == "OFF": return
    query = "#شماره_فعال"
    async for message in client.iter_messages(5044250099, search=query, limit=30):
        ranges = "998 5"
        if ranges in message.raw_text:
            await message.click(1)

aiocron.crontab("*/1 * * * *", func=cancelirnums)

@client.on(events.MessageEdited(from_users=[5816454966]))
async def smscode(event):
    fmode = client.DB.get_key("FINDNUMSMS_MODE") or "OFF"
    if fmode == "OFF": return
    ranges = "9985"
    if "💎 قیمت" in event.raw_text:
        if ranges in event.raw_text:
            await event.click(-1)
        else:
            text = "#New_Number - @" + client.me.username + "\n\n" + event.raw_text
            await client.bot.send_message(client.REALM, text)
    if "❌" in event.raw_text:
        await event.click(0)
