from TNTSelf import client
import cv2
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
            "{CMD}RQrCode": {
                "Help": "To Read QrCode",
                "Reply": ["Photo"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "caption": "**{STR} The QrCode Image Is Created!**",
    "notqr": "**{STR} The QrCode Is Not Founded!**",
    "readqr": "**{STR} QrCode Data:**\n( `{}` )",
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
    
@client.Command(command="RQrCode")
async def readqrcode(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    qrimg = await event.reply_message.download_media(client.PATH)
    readqr = cv2.imread(qrimg)
    detector = cv2.QRCodeDetector()
    result, y, z = detector.detectAndDecode(readqr)
    if not result:
        return await event.edit(client.getstrings(STRINGS)["notqr"])
    result = (result[:3800] + " ...") if len(result) > 3800 else result
    text = client.getstrings(STRINGS)["readqr"].format(result)
    await event.edit(text)