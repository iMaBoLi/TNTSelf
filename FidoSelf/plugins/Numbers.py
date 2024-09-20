from FidoSelf import client
from telethon import events
import aiocron

@client.on(events.NewMessage(from_users=[5044250099]))
async def irbot(event):
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
    query = "#شماره_فعال"
    async for message in client.iter_messages(5044250099, search=query, limit=30):
        ranges = "998 5"
        if ranges in message.raw_text:
            await message.click(1)

aiocron.crontab("*/1 * * * *", func=cancelnums)

@client.on(events.MessageEdited(from_users=[5816454966]))
async def smscode(event):
    ranges = "9985"
    if "💎 قیمت" in event.raw_text:
        if ranges in event.raw_text:
            await event.click(-1)
        else:
            text = "#New_Number - @" + client.me.username + "\n\n" + event.raw_text
            await client.bot.send_message(client.REALM, text)
    if "❌" in event.raw_text:
        await event.click(0)
