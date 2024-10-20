from TNTSelf import client
from telethon import functions, types, errors

__INFO__ = {
    "Category": "Funs",
    "Name": "Copy Sticker",
    "Info": {
        "Help": "To Copy Sticker Set To New Stickers!",
        "Commands": {
            "{CMD}CopySticker <Title>:<SName>": {
               "Help": "To Copy Sticker",
                "Input": {
                    "<Title>" : "Title For StickerSet",
                    "<SName>" : "Short Name For StickerSet"
                },
                "Reply": ["Sticker"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "invshort": "**{STR} The StickerSet Short Name** ( `{}` ) **Is Invalid!**",
    "ocshort": "**{STR} The StickerSet Short Name** ( `{}` ) **Is Occupied!**",
    "creating": "**{STR} The New StickerSet** ( {} ) **Was Created!**\n\n**{STR} Stickers Was Adding To New StickerSet ...**",
    "created": "**{STR} The New StickerSet Created And Stickers Is Added!**\n\n**{STR} Title:** ( {} )\n**{STR} Short Name:** ( `{}` )",
}

@client.Command(command="CopySticker (.*)\\:(.*)")
async def copysticker(event):
    await event.edit(client.STRINGS["wait"])
    title = str(event.pattern_match.group(1))
    sname = str(event.pattern_match.group(2))
    if reply:= event.checkReply(["Sticker", "ASticker", "VSticker"]):
        return await event.edit(reply)
    try:
        await client(functions.stickers.CheckShortNameRequest(short_name=sname))
    except errors.ShortNameInvalidError:
        return await event.edit(client.getstrings(STRINGS)["invshort"].format(sname))
    except errors.ShortNameOccupiedError:
        return await event.edit(client.getstrings(STRINGS)["ocshort"].format(sname))
    for atts in event.reply_message.media.document.attributes:
        if atts.to_dict()["_"] == "DocumentAttributeSticker":
            attributes = atts
    getstickers = await client(functions.messages.GetStickerSetRequest(stickerset=types.InputStickerSetID(id=attributes.stickerset.id, access_hash=attributes.stickerset.access_hash), hash=0))
    first = getstickers.documents[0]
    for atts in first.attributes:
        if atts.to_dict()["_"] == "DocumentAttributeSticker":
            attributes = atts
    create = await client(functions.stickers.CreateStickerSetRequest(user_id=client.me.id, title=title, short_name=sname, stickers=[types.InputStickerSetItem(document=types.InputDocument(id=first.id, access_hash=first.access_hash, file_reference=first.file_reference), emoji=attributes.alt)]))
    setmen = f"[{create.set.title}](https://t.me/addstickers/{create.set.short_name})"
    await event.edit(client.getstrings(STRINGS)["creating"].format(setmen))
    for sticker in getstickers.documents:
        if sticker.id == first.id: continue
        for atts in sticker.attributes:
            if atts.to_dict()["_"] == "DocumentAttributeSticker":
                attributes = atts
        try:
            await client(functions.stickers.AddStickerToSetRequest(stickerset=types.InputStickerSetID(id=create.set.id, access_hash=create.set.access_hash), sticker=types.InputStickerSetItem(document=types.InputDocument(id=sticker.id, access_hash=sticker.access_hash, file_reference=sticker.file_reference), emoji=attributes.alt)))
        except:
            continue
    await event.edit(client.getstrings(STRINGS)["created"].format(setmen, sname))