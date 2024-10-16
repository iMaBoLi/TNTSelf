from TNTSelf import client
from speechmatics.models import ConnectionSettings
from speechmatics.batch_client import BatchClient
from httpx import HTTPStatusError

__INFO__ = {
    "Category": "Tools",
    "Name": "SpeechText",
    "Info": {
        "Help": "To Convert Your Voice And Speech To Text!",
        "Commands": {
            "{CMD}SText": {
                "Help": "To Convert To Text",
                "Reply": ["Music", "Voice"],
            },
            "{CMD}SText <Lang>": {
                "Help": "To Convert To Text",
                "Input": {
                    "<Lang>": "Text Language",
                },
                "Reply": ["Music", "Voice"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "converting": "**{STR} Converting Your Speech To Text With Language** ( `{}` ) **...**",
    "errortext": "**{STR} The Convert Is Not Completed!**\n\n**{STR} Error:** ( `{}` )",
    "errorlang": "**{STR} The Language** ( `{}` ) **Is Not Available!**",
    "speechtext": "**{STR} The Speech Converted To Text!**\n\n**{STR} Language:** ( `{}` )\n**{STR} Results:** ( `{}` )",
}

API_KEY = "MxnMTXmF9LfkF09by0OQEHD0OgqsjwDc"

@client.Command(command="SText ?(.*)?")
async def speechtext(event):
    await event.edit(client.STRINGS["wait"])
    client.loop.create_task(convert(event))
    
async def convert(event):
    lang = str(event.pattern_match.group(1) or "en")
    if reply:= event.checkReply(["Music", "Voice"]):
        return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    file = await client.fast_download(event.reply_message, progress_callback=callback)
    await event.edit(client.getstrings(STRINGS)["converting"].format(lang))
    settings = ConnectionSettings(url="https://asr.api.speechmatics.com/v2", auth_token=API_KEY)
    config = {
        "type": "transcription",
        "transcription_config": {
            "language": lang.lower(),
        },
    }
    with BatchClient(settings) as bclient:
        try:
            jobid = bclient.submit_job(audio=file, transcription_config=config)
            transcript = bclient.wait_for_completion(jobid, transcription_format="txt")
        except Exception as error:
            if "400 Bad Request" in error:
                return await event.edit(client.getstrings(STRINGS)["errorlang"].format(lang))
            return await event.edit(client.getstrings(STRINGS)["errortext"].format(error))
    await event.edit(client.getstrings(STRINGS)["speechtext"].format(lang, transcript))