from FidoSelf import client
import random

@client.Cmd(pattern=f"(?i)^\{client.cmd}Flood \'(\d*)\' ?([\s\S]*)?")
async def flood(event):
    count = int(event.pattern_match.group(1))
    texts = event.pattern_match.group(2)
    if not texts and not event.is_reply:
        texts = "1,2,3,4,5,6,7,8,9"
    await event.delete()
    if texts:
        for i in range(count):
            rand = random.choice(texts.split(","))
            await event.respond(rand)
    elif event.is_reply:
        for i in range(count):
            message = await client.get_messages(event.chat_id, ids=event.reply_message.id)
            await event.respond(message)
