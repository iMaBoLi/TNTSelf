from TNTSelf import client
import qrcode

__INFO__ = {
    "Category": "Tools",
    "Name": "QrCode",
    "Info": {
        "Help": "To Create And Read Qr Codes!",
        "Commands": {
            "{CMD}SQrCode": {
                "Help": "To Create QrCode",
                "Reply": ["Text"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "caption": "**{STR} The QrCode Image Is Created!**",
}

@client.Command(command="SQrCode")
async def createqrcode(event):
    await event.edit(client.STRINGS["wait"])
    if not event.reply_message or not event.reply_message.text:
        return await event.edit(client.STRINGS["replytext"])
    text = str(event.reply_message.text)
    code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    code.add_data(text)
    code.make()
    qrimg = code.make_image().convert("RGB")
    qrname = client.PATH + "QrCode.jpg"
    qrimg.save(qrname)
    caption = client.getstrings(STRINGS)["caption"]
    await client.send_file(event.chat_id, qrname, caption=caption)
    os.remove(qrname)
    await event.delete()