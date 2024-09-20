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
            await event.forward_to(client.REALM)
            tag = "#New_Number - @" + client.me.username
            await client.bot.send_message(client.REALM, tag)
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