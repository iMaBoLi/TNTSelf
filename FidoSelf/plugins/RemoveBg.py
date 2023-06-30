from FidoSelf import client
import requests, os

__INFO__ = {
    "Category": "Practical",
    "Plugname": "RemoveBg",
    "Pluginfo": {
        "Help": "To Remove Background From Your Photos!",
        "Commands": {
            "{CMD}SetRmBgKey <Key>": None,
            "{CMD}RmBg <Reply(Photo)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "setapi": "**The RemoveBg ApiKey** ( `{}` ) **Has Been Saved!**",
    "notsave": "**The RemoveBg ApiKey Is Not Saved!**",
    "notcom": "**The Remove Background Not Completed!**\n**Error:** ( `{}` )",
    "caption": "**The Remove Background From Photo Completed!**",
}

def removebg(photo, newphoto):
    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": open(photo, "rb")},
        data={"size": "auto"},
        headers={"X-Api-Key": str(client.DB.get_key("RMBG_API_KEY"))},
    )
    if response.status_code == requests.codes.ok:
        with open(newphoto, "wb") as out:
            out.write(response.content)
        return True, newphoto
    else:
        return False, response.text["errors"][0]["title"]

@client.Command(command="SetRmBgKey (.*)")
async def savebgapi(event):
    await event.edit(client.STRINGS["wait"])
    api = event.pattern_match.group(1)
    client.DB.set_key("RMBG_API_KEY", api)
    await event.edit(STRINGS["setapi"].format(api))

@client.Command(command="RmBg")
async def rmbg(event):
    await event.edit(client.STRINGS["wait"])
    reply, _ = event.checkReply(["Photo"])
    if reply: return await event.edit(reply)
    if not client.DB.get_key("RMBG_API_KEY"):
        return await event.edit(STRINGS["notsave"])
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = client.PATH + "RemoveBG.png"
    state, result = removebg(photo, newphoto)
    if not state:
        return await event.edit(STRINGS["notcom"].format(result))
    caption = STRINGS["caption"]
    await client.send_file(event.chat_id, newphoto, force_document=True, allow_cache=True, caption=caption)
    await client.send_file(event.chat_id, newphoto, caption=caption)
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()