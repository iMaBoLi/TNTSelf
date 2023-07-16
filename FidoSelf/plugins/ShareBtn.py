from FidoSelf import client
from telethon import functions, Button

SHARES = {}

def create_share(chatid, text, bttext="• Share •"):
    rand = random.randint(0, 9999999)
    info = {"chat_id": chatid, "text": text}
    SHARES.update({rand: info})
    data = "Share:" + str(rand)
    button = Button.inline(bttext, data=data)
    return button

client.create_share = create_share

STRINGS = {
    "notfound": "**{STR} The Error Occurred, Please Try Again!**",
}

@client.Callback(data="Share\:(.*)")
async def sharetext(event):
    shareid = int(event.data_match.group(1).decode('utf-8'))
    if shareid not in SHARES:
        return await event.edit(client.getstrings(STRINGS)["notfound"])
    info = SHARES[shareid]
    await client(functions.messages.SaveDraftRequest(peer=info["chat_id"], message=info["text"]))