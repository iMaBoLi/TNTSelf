from FidoSelf import client
from telethon import functions, types, utils
from telethon.errors.rpcerrorlist import PackShortNameOccupiedError

STRINGS = {
    "notall": "**The Short Name** ( `{}` ) **iS Already Used in Other Packs!**",
    "creating": "**The Pack** ( `{}` ) **iS Creating ...**",
    "adding": "**The Stickers On Pack** ( `{}` ) **iS Adding ...**",
    "created": "**The Pack iS Copied!**\n\n**Title:** ( `{}` )\n**Link:** ( `{}` )\n**Stickers Count:** ( `{}` )",
}

@client.Command(command="Cpack (.*)\:(.*)")
async def copypack(event):
    await event.edit(client.STRINGS["wait"])
    packtitle = event.pattern_match.group(1)
    packname = event.pattern_match.group(2)
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Sticker", "ASticker"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["Sticker"] + " - " + medias["ASticker"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    id = event.reply_message.media.document.attributes[1].stickerset.id
    hash = event.reply_message.media.document.attributes[1].stickerset.access_hash
    stickers = await client(
        functions.messages.GetStickerSetRequest(
            stickerset=types.InputStickerSetID(
                id=id,
                access_hash=hash
            ),
            hash=0,
        )
    )
    stickers = stickers.documents
    stiks = []
    for sticker in stickers:
        doc = utils.get_input_document(sticker)
        stiks.append(
            types.InputStickerSetItem(
                document=doc,
                emoji=event.reply_message.document.attributes[-2].alt,
            )
        )
    short_name = packname.replace(" ", "_")
    short_name = f"{short_name}_by_{client.bot.me.username}"
    anim = True if mtype == "Sticker" else False
    await event.edit(STRINGS["creating"].format(packtitle))
    try:
        result = await client.bot(
            functions.stickers.CreateStickerSetRequest(
                    user_id=event.sender_id,
                    title=packtitle,
                    short_name=short_name,
                    animated=anim,
                    stickers=stiks[:10],
                )
            )
    except PackShortNameOccupiedError:
        return await event.edit(STRINGS["notall"].format(packname))
    id = result.set.id
    id = result.set.access_hash
    await event.edit(STRINGS["adding"].format(packtitle))
    for sticker in stiks[10:]:
        result = await client.bot(
            functions.stickers.AddStickerToSetRequest(
                stickerset=types.InputStickerSetID(
                    id=id,
                    access_hash=access_hash,
                ),
                sticker=sticker,
            )
        )
    link = f"https://t.me/addstickers/{short_name}"
    text = STRINGS["created"].format(packtitle, link, len(stiks))
    await event.edit(text)
