from FidoSelf import client
from telethon import functions, utils

@client.Command(command="Spack (.*)")
async def Spack(event):
    await event.edit(client.STRINGS["wait"])
    packname = event.pattern_match.group(1)
    reply = event.reply_message
    id = reply.media.document.attributes[1].stickerset.id
    hash = reply.media.document.attributes[1].stickerset.access_hash
    stickers = await client(
        functions.messages.GetStickerSetRequest(
            stickerset=types.InputStickerSetID(id=id, access_hash=hash), hash=0
        )
    )
    stickers = stickers.documents
    anim = True if reply.document.mime_type in ["image/webp"] else False
    vid = True if reply.document.mime_type in ["video/webm", "application/x-tgsticker"] else False
    stiks = []
    for sticker in stickers:
        doc = utils.get_input_document(sticker)
        stiks.append(
            types.InputStickerSetItem(
                document=doc,
                emoji=sticker.attributes[1]).alt,
        )
    short_name = packname.replace(" ", "_")
    short_name = f"{short_name}_by_{client.bot.me.username}"
    result = await client.bot(
        functions.stickers.CreateStickerSetRequest(
                user_id=event.sender_id,
                title=packname,
                short_name=short_name,
                animated=anim,
                videos=vid,
                stickers=stiks,
            )
        )