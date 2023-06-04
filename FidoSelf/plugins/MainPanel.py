from FidoSelf import client
from telethon import Button
from .Action import ACTIONS

STRINGS = {
    "modepage": "**Select Which Mode You Want Turn On-Off:**",
    "fontpage": "**Select Which Time Font You Want Turn On-Off:**",
    "editpage": "**Select Which Edit Mode You Want Turn On-Off:**",
    "actionpage": "**Select Which Action Mode You Want Turn On-Off:**",
    "close": "**The Panel Successfuly Closed!**",
    "Modes": {
        "NAME_MODE": "Name",
        "BIO_MODE": "Bio",
        "PHOTO_MODE": "Photo",
        "TIMER_MODE": "Timer Save",
        "MUTE_PV": "Mute Pv",
        "LOCK_PV": "Lock Pv",
        "ANTISPAM_PV": "AntiSpam Pv",
        "READALL_MODE": "Mark All",
        "READPV_MODE": "Mark Pv",
        "READGP_MODE": "Mark Group",
        "READCH_MODE": "Mark Channel",
    },
    "Edits": {
        "Bold": "Bold",
        "Mono": "Mono",
        "Italic": "Italic",
        "Underline": "Underline",
        "Strike": "Strike",
        "Spoiler": "Spoiler",
        "Hashtag": "Hashtag",
    },
    "Random1": "Random",
    "Random2": "Random V2",
}

def get_pages_button(opage):
    buttons = []
    PAGES_COUNT = 5 + 1
    for page in range(1, PAGES_COUNT):
        font = 3 if page != opage else 4
        name = client.functions.create_font(page, font)
        buttons.append(Button.inline(f"( {name} )", data=f"panelpage:{page}"))
    return buttons

def get_mode_buttons(page):
    buttons = []
    MODES = STRINGS["Modes"]
    for mode in MODES:
        gmode = client.DB.get_key(mode) or "off"
        cmode = "on" if gmode == "off" else "off"
        name = MODES[mode]
        nmode = client.STRINGS["inline"]["On"] if gmode == "on" else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{name} {nmode}", data=f"setmode:{mode}:{cmode}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append(get_pages_button(page))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closepanel")])
    return buttons

def get_time_buttons(page):
    newtime = datetime.now().strftime("%H:%M")
    last = client.DB.get_key("TIME_FONT") or 1
    buttons = []
    rname = STRINGS["Random1"]
    rmode = client.STRINGS["inline"]["On"] if str(last) == "random" else client.STRINGS["inline"]["Off"]
    r2name = STRINGS["Random2"]
    r2mode = client.STRINGS["inline"]["On"] if str(last) == "random2" else client.STRINGS["inline"]["Off"]
    buttons.append(Button.inline(f"{rname} {rmode}", data=f"setfonttime:random"))
    buttons.append(Button.inline(f"{r2name} {r2mode}", data=f"setfonttime:random2"))
    for font in client.functions.FONTS:
        name = client.functions.create_font(newtime, font)
        mode = client.STRINGS["inline"]["On"] if str(last) == str(font) else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{name} {mode}", data=f"setfonttime:{font}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append(get_pages_button(page))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closepanel")])
    return buttons

def get_edit_buttons(page):
    last = client.DB.get_key("EDIT_MODE")
    buttons = []
    EDITS = STRINGS["Edits"]
    for edit in EDITS:
        name = EDITS[edit]
        mode = client.STRINGS["inline"]["On"] if str(last) == str(edit) else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{name} {mode}", data=f"seteditmode:{edit}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append(get_pages_button(page))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closepanel")])
    return buttons

def get_action_buttons(page):
    buttons = []
    for action in ACTIONS:
        mode = action.upper() + "_CHATS"
        chats = client.DB.get_key(mode) or []
        gmode = "del" if event.chat_id in chats else "add"
        name = action.replace("-", " ").title()
        nmode = client.STRINGS["inline"]["On"] if gmode == "del" else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{name} {nmode}", data=f"actionchat:{action}:{event.chat_id}:{gmode}"))
        mode = action.upper() + "_ALL"
        gmode = client.DB.get_key(mode) or "off"
        cmode = "on" if mode == "off" else "off"
        name = action.replace("-", " ").title()
        nmode = client.STRINGS["inline"]["On"] if gmode == "on" else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{name} {nmode}", data=f"actionall:{action}:{cmode}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append(get_pages_button(page))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closepanel")])
    return buttons

@client.Command(command="Panel")
async def addecho(event):
    await event.edit(client.STRINGS["wait"])
    res = await client.inline_query(client.bot.me.username, "selfmainpanel")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Inline(pattern="selfmainpanel")
async def inlinepanel(event):
    text = STRINGS["modepage"]
    buttons = get_mode_buttons(1)
    await event.answer([event.builder.article("FidoSelf - Panel", text=text, buttons=buttons)])

@client.Callback(data="panelpage\:(.*)")
async def panelpages(event):
    page = int(event.data_match.group(1).decode('utf-8'))
    if page == 1:
        text = STRINGS["modepage"]
        buttons = get_mode_buttons(page)
    elif page == 2:
        text = STRINGS["fontpage"]
        buttons = get_time_buttons(page)
    elif page == 3:
        text = STRINGS["editpage"]
        buttons = get_edit_buttons(page)
    elif page == 5:
        text = STRINGS["actionpage"]
        buttons = get_action_buttons(page)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="setmode\:(.*)\:(.*)")
async def setmode(event):
    mode = event.data_match.group(1).decode('utf-8')
    change = event.data_match.group(2).decode('utf-8')
    client.DB.set_key(mode, change)
    text = STRINGS["modepage"]
    buttons = get_mode_buttons(1)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="setfonttime\:(.*)")
async def setfonttime(event):
    font = event.data_match.group(1).decode('utf-8')
    client.DB.set_key("TIME_FONT", str(font))
    buttons = get_time_buttons(2)
    await event.edit(buttons=buttons)

@client.Callback(data="seteditmode\:(.*)")
async def seteditmode(event):
    edit = event.data_match.group(1).decode('utf-8')
    last = client.DB.get_key("EDIT_MODE")
    if str(last) == str(edit):
        client.DB.set_key("EDIT_MODE", False)
    else:
        client.DB.set_key("EDIT_MODE", str(edit))
    buttons = get_edit_buttons(3)
    await event.edit(buttons=buttons)
    
@client.Callback(data="actionall\:(.*)\:(.*)")
async def setmode(event):
    action = event.data_match.group(1).decode('utf-8')
    change = event.data_match.group(2).decode('utf-8')
    action = action.upper() + "_ALL"
    client.DB.set_key(action, change)
    text = STRINGS["actionpage"]
    buttons = get_action_buttons(5)
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="actionchats\:(.*)\:(.*)\:(.*)")
async def setmode(event):
    action = event.data_match.group(1).decode('utf-8')
    chatid = int(event.data_match.group(2).decode('utf-8'))
    change = event.data_match.group(3).decode('utf-8')
    action = action.upper() + "_CHATS"
    last = client.DB.get_key(action)
    if change == "add":
        new = last.append(chatid)
        client.DB.set_key(action, new)
    if change == "del":
        new = last.remove(chatid)
        client.DB.set_key(action, new)
    text = STRINGS["actionpage"]
    buttons = get_action_buttons(5)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="closepanel")
async def closepanel(event):
    text = STRINGS["close"]
    await event.edit(text=text)