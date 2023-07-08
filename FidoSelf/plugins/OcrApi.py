from FidoSelf import client
import requests, os

__INFO__ = {
    "Category": "Tools",
    "Name": "Ocr",
    "Info": {
        "Help": "To Extract Text From Your Photos!",
        "Commands": {
            "{CMD}SetOcrKey <Key>": "Set Ocr Api Key!",
            "{CMD}Ocr <Lang>": "Get Ocr Result White Language!",
            "{CMD}OcrLangs": "Get Ocr Languages!",
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "setapi": "**The Ocr ApiKey** ( `{}` ) **Has Been Saved!**",
    "notsave": "**The Ocr ApiKey Is Not Saved!**",
    "notlang": "**The Entered Language Is Not Found!**",
    "notcom": "**The Extract Text Not Completed!**\n**Error:** ( `{}` )",
    "notresult": "**The Extract Text Completed And Not Text Finded!**",
    "result": "**The Extract Text Completed!**\n**Language:** ( `{}` )\n\n**Result:** ( `{}` )",
    "langs": "**The Available OcrApi Languages:**\n\n",
}

def ocr_file(file, language):
    payload = {
        "isOverlayRequired": True,
        "apikey": client.DB.get_key("OCR_APIKEY"),
        "language": language,
    }
    with open(file, "rb") as fget:
        req = requests.post("https://api.ocr.space/parse/image", files={'filename': fget}, data=payload)
    raw = req.json()
    if type(raw) == str:
        if "API Key is not specified" in str(raw) or "The API key is invalid" in str(raw):
            return False, "Invalid Api Key"
        return False, raw
    elif raw['IsErroredOnProcessing']:
        return False, raw['ErrorMessage'][0]
    return True, raw['ParsedResults'][0]['ParsedText']

@client.Command(command="SetOcrKey (.*)")
async def saveocrapi(event):
    await event.edit(client.getstrings()["wait"])
    api = event.pattern_match.group(1)
    client.DB.set_key("OCR_APIKEY", api)
    await event.edit(client.getstrings(STRINGS)["setapi"].format(api))

@client.Command(command="Ocr ?(.*)?")
async def ocrapi(event):
    await event.edit(client.getstrings()["wait"])
    lang = event.pattern_match.group(1) or "eng"
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    if not client.DB.get_key("OCR_APIKEY"):
        return await event.edit(client.getstrings(STRINGS)["notsave"])
    if not lang in client.functions.OCRLANGS:
        return await event.edit(client.getstrings(STRINGS)["notlang"])
    photo = await event.reply_message.download_media(client.PATH)
    stat, res = ocr_file(photo, lang)
    if not stat:
        return await event.edit(client.getstrings(STRINGS)["notcom"].format(res))
    elif stat and not res:
        return await event.edit(client.getstrings(STRINGS)["notresult"].format(res))
    await event.edit(client.getstrings(STRINGS)["result"].format(client.functions.OCRLANGS[lang], res))   
    os.remove(photo)

@client.Command(command="OcrLangs")
async def ocrlangs(event):
    await event.edit(client.getstrings()["wait"])
    text = client.getstrings(STRINGS)["langs"]
    for lang in client.functions.OCRLANGS:
        text += f"• `{lang}` - **{client.functions.OCRLANGS[lang]}**\n"
    await event.edit(text)
