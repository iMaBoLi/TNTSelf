from FidoSelf import client
from telethon import events
import aiocron

STRINGS = {
    "change": "**{STR} The Find Number Mode Has Been {}!**",
}

@client.Command(command="Find (On|Off)")
async def findnumber(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("FINDNUM_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.on(events.NewMessage(from_users=[5044250099]))
async def irbot(event):
    fmode = client.DB.get_key("FINDNUM_MODE") or "OFF"
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
    
async def cancelnums():
    fmode = client.DB.get_key("FINDNUM_MODE") or "OFF"
    if fmode == "OFF": return
    query = "#شماره_فعال"
    async for message in client.iter_messages(5044250099, search=query, limit=30):
        ranges = "998 5"
        if ranges in message.raw_text:
            await message.click(1)

aiocron.crontab("*/1 * * * *", func=cancelnums)

@client.on(events.MessageEdited(from_users=[5816454966]))
async def smscode(event):
    fmode = client.DB.get_key("FINDNUM_MODE") or "OFF"
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
