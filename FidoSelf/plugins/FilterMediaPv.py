from FidoSelf import client

@client.Command(onlysudo=False, allowedits=False)
async def mediafilterpv(event):
    if not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    mtype = event.mediatype()
    MODES = {}
    for Mode in client.functions.PVFILTERS:
        getmode = client.DB.get_key(Mode) or "OFF" 
        MODES.update({Mode: getmode})
    if event.text and MODES["FILTERPV_TEXT"] == "ON":
        await event.delete()
    elif event.media and MODES["FILTERPV_MEDIA"] == "ON":
        await event.delete()
    elif mtype.endswith("Photo") and MODES["FILTERPV_PHOTO"] == "ON":
        await event.delete()
    elif mtype == "Video" and MODES["FILTERPV_VIDEO"] == "ON":
        await event.delete()
    elif mtype == "Gif" and MODES["FILTERPV_GIF"] == "ON":
        await event.delete()
    elif mtype == "Voice" and MODES["FILTERPV_VOICE"] == "ON":
        await event.delete()
    elif mtype == "Music" and MODES["FILTERPV_MUSIC"] == "ON":
        await event.delete()
    elif mtype in ["Sticker", "ASticker", "VSticker"] and MODES["FILTERPV_STICKER"] == "ON":
        await event.delete()
    elif mtype.endswith("File") and MODES["FILTERPV_FILE"] == "ON":
        await event.delete()
    elif event.text and MODES["FILTERPV_LINK"] == "ON":
        if event.entities:
            for entity in event.to_dict()["entities"]:
                if entity["_"] in ["MessageEntityUrl"]:
                    await event.delete()