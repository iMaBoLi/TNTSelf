from FidoSelf import client
import requests, os

__INFO__ = {
    "Category": "Practical",
    "Plugname": "Ocr",
    "Pluginfo": {
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
    "com": "**The Extract Text Completed!**\n**Language:** ( `{}` )\n\n**Result:** ( `{}` )",
    "langs": "**The Available OcrApi Languages:**\n\n",
}
LANGS = {
    "ara": "Arabic",
    "eng": "English",
    "fre": "French",
    "kor": "Korean",
    "ita": "Italian",
    "jpn": "Japanese",
    "chs": "Chinese",
    "ger": "German",
    "spa": "Spanish",
    "swe": "Swedish",
    "tur": "Turkish",
    "bul": "Bulgarian",
    "pol": "Polish",
    "por": "Portugal",
    "rus": "Russian",
    "hrv": "Croatian",
    "hin": "Hindi",
}

def ocr_file(file, language):
    payload = {
        "isOverlayRequired": True,
        "apikey": client.DB.get_key("OCR_API_KEY"),
        "language": language,
    }
    with open(file, "rb") as fget:
        req = requests.post("https://api.ocr.space/parse/image", files={'filename': fget}, data=payload)
    raw = req.json()
    if type(raw) == str:
        if "API Key is not specified" in str(raw) or "The API key is invalid" in str(raw):
            return False, "invalid apikey"
        return False, raw
    elif raw['IsErroredOnProcessing']:
        return False, raw['ErrorMessage'][0]
    return True, raw['ParsedResults'][0]['ParsedText']

@client.Command(command="SetOcrKey (.*)")
async def saveocrapi(event):
    await event.edit(client.STRINGS["wait"])
    api = event.pattern_match.group(1)
    client.DB.set_key("OCR_API_KEY", api)
    await event.edit(STRINGS["setapi"].format(api))

@client.Command(command="Ocr ?(.*)?")
async def ocrapi(event):
    await event.edit(client.STRINGS["wait"])
    lang = event.pattern_match.group(1) or "eng"
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Photo"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["Photo"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    if not client.DB.get_key("OCR_API_KEY"):
        return await event.edit(STRINGS["notsave"])
    if not lang in LANGS:
        return await event.edit(STRINGS["notlang"])
    photo = await event.reply_message.download_media(client.PATH)
    stat, res = ocr_file(photo, lang)
    if not stat:
        text = STRINGS["notcom"].format(res)
        return await event.edit(text)
    await event.edit(STRINGS["com"].format(LANGS[lang], res))   
    os.remove(photo)

@client.Command(command="OcrLangs")
async def ocrlangs(event):
    await event.edit(client.STRINGS["wait"])
    text = STRINGS["langs"]
    for lang in LANGS:
        text += f"• `{lang}` - **{LANGS[lang]}**\n"
    await event.edit(text)
