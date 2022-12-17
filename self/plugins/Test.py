from self import client
from telethon import events

@client.on(events.NewMessage(pattern=f"(?i)^\{client.cmd}ping$"))
async def test(event):
    await event.edit(f"**{client.str} Pong‌ !!**")
