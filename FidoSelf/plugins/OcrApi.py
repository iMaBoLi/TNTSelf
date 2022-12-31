from FidoSelf import client
import requests, os

LANGS = {"ara": "Arabic", "eng": "English", "fre": "French", "kor": "Korean", "ita": "Italian", "jpn": "Japanese", "chs": "Chinese", "ger": "German", "spa": "Spanish", "swe": "Swedish", "tur": "Turkish", "bul": "Bulgarian", "pol": "Polish", "por": "Portugal", "rus": "Russian", "hrv": "Croatian", "hin": "Hindi"}

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

@client.Cmd(pattern=f"(?i)^\{client.cmd}OcrApi (.*)$")
async def saveocrapi(event):
    await event.edit(client.get_string("Wait"))
    api = event.pattern_match.group(1)
    client.DB.set_key("OCR_API_KEY", api)
    await event.edit(f"**{client.str} The Ocr ApiKey** ( `{api}` ) **Has Been Saved!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}Ocr (.*)$")
async def ocrapi(event):
    await event.edit(client.get_string("Wait"))
    lang = event.pattern_match.group(1)
    if not client.DB.get_key("OCR_API_KEY"):
        return await event.edit(f"**{client.str} Please Save Ocr ApiKey First!**")
    if not lang in LANGS:
        return await event.edit(f"**{client.str} The Language Not Found!**")
    if not event.is_reply or not event.photo:
        return await event.edit(f"**{client.str} Please Reply To Photo!**")
    photo = f"{event.reply_message.id}.png"
    await event.reply_message.download_media(photo)
    stat, res = ocr_file(photo, lang)
    if not stat:
        return await event.edit(text=f"**{client.str} The Extract Text Not Completed!**\n**{client.str} Error:** ( `{res}` )")
    await event.edit(f"**{client.str} The Extract Text Completed!**\n**{client.str} Language:** ( `{LANGS[lang]}` )\n\n**{client.str} Result:** ( `{res}` )")    
    os.remove(photo)

@client.Cmd(pattern=f"(?i)^\{client.cmd}OcrLangs$")
async def ocrlangs(event):
    await event.edit(client.get_string("Wait"))
    text = f"**{client.str} The Ocr Languages:**\n\n"
    for lang in LANGS:
        text += f"• `{lang}` - **{LANGS[lang]}**\n"
    await event.edit(text)
