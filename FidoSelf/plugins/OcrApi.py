from FidoSelf import client
import requests, os

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

@client.Command(pattern=f"(?i)^\{client.cmd}OcrApi (.*)$")
async def saveocrapi(event):
    await event.edit(client.get_string("Wait"))
    api = event.pattern_match.group(1)
    client.DB.set_key("OCR_API_KEY", api)
    await event.edit(client.get_string("OcrApi_1").format(api))

@client.Command(pattern=f"(?i)^\{client.cmd}Ocr (.*)$")
async def ocrapi(event):
    await event.edit(client.get_string("Wait"))
    lang = event.pattern_match.group(1)
    LANGS = client.get_string("OcrLangs")
    if not client.DB.get_key("OCR_API_KEY"):
        return await event.edit(client.get_string("OcrApi_2"))
    if not lang in LANGS:
        return await event.edit(client.get_string("OCrApi_3"))
    if not event.is_reply or not event.photo:
        return await event.edit(client.get_string("Reply_P"))
    photo = f"{event.reply_message.id}.png"
    await event.reply_message.download_media(photo)
    stat, res = ocr_file(photo, lang)
    if not stat:
        text = client.get_string("OcrApi_4").format(res)
        return await event.edit(text)
    await event.edit(client.get_string("OcrApi_5").format(LANGS[lang], res))   
    os.remove(photo)

@client.Command(pattern=f"(?i)^\{client.cmd}OcrLangs$")
async def ocrlangs(event):
    await event.edit(client.get_string("Wait"))
    text = client.get_string("OcrApi_6")
    LANGS = client.get_string("OcrLangs")
    for lang in LANGS:
        text += f"• `{lang}` - **{LANGS[lang]}**\n"
    await event.edit(text)
