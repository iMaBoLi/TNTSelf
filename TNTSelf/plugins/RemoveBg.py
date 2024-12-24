from TNTSelf import client
import requests, os

__INFO__ = {
    "Category": "Tools",
    "Name": "RemoveBg",
    "Info": {
        "Help": "To Remove Background From Your Photos!",
        "Commands": {
            "{CMD}SetRmBgKey <Key>": None,
            "{CMD}RmBg <Reply(Photo)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "setapi": "**{STR} The RemoveBg ApiKey** ( `{}` ) **Has Been Saved!**",
    "notsave": "**{STR} The RemoveBg ApiKey Is Not Saved!**",
    "notcom": "**{STR} The Remove Background Not Completed!**\n**Error:** ( `{}` )",
    "caption": "**{STR} The Remove Background From Photo Completed!**"
}

def removebg(event, photo, newphoto):
    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": open(photo, "rb")},
        data={"size": "auto"},
        headers={"X-Api-Key": str(event.client.DB.get_key("RMBG_API_KEY"))},
    )
    if response.status_code == requests.codes.ok:
        with open(newphoto, "wb") as out:
            out.write(response.content)
        return True, newphoto
    elif "API Key invalid" in str(response.text):
        return False, "Api Key Invalid"
    else:
        return False, "Unknown Error"

@client.Command(command="SetRmBgKey (.*)")
async def savebgapi(event):
    await event.edit(client.STRINGS["wait"])
    api = event.pattern_match.group(1)
    event.client.DB.set_key("RMBG_API_KEY", api)
    await event.edit(client.getstrings(STRINGS)["setapi"].format(api))

@client.Command(command="RmBg")
async def rmbg(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    apikey = event.client.DB.get_key("RMBG_API_KEY")
    if not apikey:
        return await event.edit(client.getstrings(STRINGS)["notsave"])
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = event.client.PATH + "RemoveBG.png"
    state, result = removebg(photo, newphoto)
    if not state:
        return await event.edit(client.getstrings(STRINGS)["notcom"].format(result))
    caption = client.getstrings(STRINGS)["caption"]
    await event.client.send_file(event.chat_id, newphoto, caption=caption)
    await event.client.send_file(event.chat_id, newphoto, force_document=True, caption=caption)
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()