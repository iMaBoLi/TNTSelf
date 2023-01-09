from FidoSelf import client
from telethon import Button

def get_filter_buttons():
    buttons = []
    TYPES = client.get_string("FilterPvType")
    for type in TYPES:
        last = client.DB.get_key(type) or "off"
        smode = "( ✔️ )" if last == "on" else "( ✖️ )"
        cmode = "off" if last == "on" else "on"
        buttons.append(Button.inline(f"• {TYPES[type]} - {smode} •", data=f"setfilterpv:{type}:{cmode}"))
    buttons = list(client.utils.chunks(buttons, 2))
    buttons = client.get_buttons(buttons)
    return buttons

@client.Cmd(pattern=f"(?i)^\{client.cmd}SFilterPv$")
async def filterpvmedia(event):
    await event.edit(client.get_string("Wait"))
    res = await client.inline_query(client.bot.me.username, "filtermediapv")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="filtermediapv")
async def inlinefilterpanel(event):
    text = client.get_string("FilterMediaPv_1")
    buttons = get_filter_buttons()
    await event.answer([event.builder.article(f"{client.str} FidoSelf - Filter Media Pv", text=text, buttons=buttons)])

@client.Callback(data="setfilterpv\:(.*)\:(.*)")
async def setfilterpvs(event):
    mode = event.data_match.group(1).decode('utf-8')
    change = event.data_match.group(2).decode('utf-8')
    client.DB.set_key(mode, change)
    text = client.get_string("FilterMediaPv_1")
    buttons = get_filter_buttons()
    await event.edit(text=text, buttons=buttons)

@client.Cmd(sudo=False, edits=False)
async def mediafilter(event):
    if not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    TYPES = client.get_string("FilterPvType")
    MODES = {}
    for type in TYPES:
        mode = client.DB.get_key(type) or "off" 
        MODES.update({type: mode})
    if event.text and MODES["FILTERPV_TEXT"] == "on":
        await event.delete()
    elif client.mediatype(event) == "photo" and MODES["FILTERPV_PHOTO"] == "on":
        await event.delete()
    elif client.mediatype(event) == "video" and MODES["FILTERPV_VIDEO"] == "on":
        await event.delete()
    elif client.mediatype(event) == "gif" and MODES["FILTERPV_GIF"] == "on":
        await event.delete()
    elif client.mediatype(event) == "voice" and MODES["FILTERPV_VOICE"] == "on":
        await event.delete()
    elif client.mediatype(event) == "music" and MODES["FILTERPV_MUSIC"] == "on":
        await event.delete()
    elif client.mediatype(event) == "sticker" and MODES["FILTERPV_STICKER"] == "on":
        await event.delete()
    elif client.mediatype(event) == "animated sticker" and MODES["FILTERPV_ANISTICKER"] == "on":
        await event.delete()
    elif client.mediatype(event) == "file" and MODES["FILTERPV_FILE"] == "on":
        await event.delete()
    elif event.text and MODES["FILTERPV_LINK"] == "on":
        if event.reply_message.entities:
            for entity in event.reply_message.to_dict()["entities"]:
                if entity["_"] in ["MessageEntityUrl"]:
                    await event.delete()
