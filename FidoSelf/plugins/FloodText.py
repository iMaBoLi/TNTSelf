from FidoSelf import client
import random

__INFO__ = {
    "Category": "Funs",
    "Name": "Flood",
    "Info": {
        "Help": "To Flood Message In Chats!",
        "Commands": {
            "{CMD}Flood <Count> <Reply>": None,
            "{CMD}Flood <Count> <Text>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

@client.Command(command="Flood (\d*) ?([\s\S]*)?")
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
            await event.respond(event.reply_message)