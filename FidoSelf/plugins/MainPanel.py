from FidoSelf import client
from telethon import Button
from datetime import datetime
from .Action import ACTIONS
from .EditModes import EDITS

STRINGS = {
    "change": "**The {} Has Been {}!**",
    "modepage": "**Select Which Mode You Want Turn On-Off:**",
    "fontpage": "**Select Which Time Font You Want Turn On-Off:**",
    "editpage": "**Select Which Edit Mode You Want Turn On-Off:**",
    "actionpage": "**Select Which Action Mode You Want Turn On-Off:**",
    "readpage": "**Select Which Reader Mode You Want Turn On-Off:**",
    "close": "**The Panel Successfuly Closed!**",
    "Modes": {
        "ONLINE_MODE": "Online",
        "NAME_MODE": "Name",
        "BIO_MODE": "Bio",
        "PHOTO_MODE": "Photo",
        "TIMER_MODE": "Timer Save",
        "SIGN_MODE": "Sign",
        "SIGNENEMY_MODE": "Sign Enemy",
        "ENEMY_DELETE": "Delete Enemy Pms",
        "MUTE_PV": "Mute Pv",
        "LOCK_PV": "Lock Pv",
        "ANTISPAM_PV": "AntiSpam Pv",
        "READALL_MODE": "Read All",
        "READPV_MODE": "Read Pv",
        "READGP_MODE": "Read Group",
        "READCH_MODE": "Read Channel",
    },
}

TEXTS = {
    1: STRINGS["modepage"],
    2: STRINGS["fontpage"],
    3: STRINGS["editpage"],
    4: STRINGS["actionpage"],
}

def get_buttons(chatid, page):
    BUTTONS = {
        1: get_mode_buttons(chatid, page),
        2: get_time_buttons(chatid, page),
        3: get_edit_buttons(chatid, page),
        4: get_action_buttons(chatid, page),
    }
    return BUTTONS[page]

def get_pages_button(chatid, opage):
    buttons = []
    PAGES_COUNT = len(TEXTS)
    for page in range(1, PAGES_COUNT):
        font = 4 if page != opage else 5
        name = client.functions.create_font(page, font)
        buttons.append(Button.inline(f"( {name} )", data=f"page:{chatid}:{page}"))
    return buttons

def get_mode_buttons(chatid, page):
    buttons = []
    MODES = STRINGS["Modes"]
    for mode in MODES:
        gmode = client.DB.get_key(mode) or "off"
        cmode = "on" if gmode == "off" else "off"
        name = MODES[mode]
        nmode = client.STRINGS["inline"]["On"] if gmode == "on" else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{name} {nmode}", data=f"Turn:{cmode}:{mode}:{chatid}:{page}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append(get_pages_button(chatid, page))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closepanel")])
    return buttons

def get_time_buttons(chatid, page):
    newtime = datetime.now().strftime("%H:%M")
    last = client.DB.get_key("TIME_FONT") or 1
    buttons = []
    rname, r2name = "Random", "Random V2"
    rmode = client.STRINGS["inline"]["On"] if str(last) == "random" else client.STRINGS["inline"]["Off"]
    r2mode = client.STRINGS["inline"]["On"] if str(last) == "random2" else client.STRINGS["inline"]["Off"]
    buttons.append(Button.inline(f"{rname} {rmode}", data=f"setfonttime:{chatid}:{page}:random"))
    buttons.append(Button.inline(f"{r2name} {r2mode}", data=f"setfonttime:{chatid}:{page}:random2"))
    for font in client.functions.FONTS:
        name = client.functions.create_font(newtime, font)
        mode = client.STRINGS["inline"]["On"] if str(last) == str(font) else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{name} {mode}", data=f"setfonttime:{chatid}:{page}:{font}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append(get_pages_button(chatid, page))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closepanel")])
    return buttons

def get_edit_buttons(chatid, page):
    lastall = client.DB.get_key("EDITALL_MODE")
    lastchat = client.DB.get_key("EDITCHATS_MODE") or {}
    buttons = []
    for edit in EDITS:
        gmode = "off" if (chatid in lastchat and lastchat[chatid] == edit) else "on"
        nmode = client.STRINGS["inline"]["On"] if gmode == "off" else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{edit} {nmode}", data=f"seteditchat:{chatid}:{page}:{edit}"))
        name = edit + " All"        
        mode = client.STRINGS["inline"]["On"] if str(lastall) == str(edit) else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{name} {mode}", data=f"seteditall:{chatid}:{page}:{edit}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append(get_pages_button(chatid, page))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closepanel")])
    return buttons

def get_action_buttons(chatid, page):
    buttons = []
    for action in ACTIONS:
        chats = client.DB.get_key(action.upper() + "_CHATS") or []
        gmode = "del" if int(chatid) in chats else "add"
        name = action.replace("-", " ").title()
        nmode = client.STRINGS["inline"]["On"] if gmode == "del" else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{name} {nmode}", data=f"actionchat:{chatid}:{page}:{action}:{gmode}"))
        gmode = client.DB.get_key(action.upper() + "_ALL") or "off"
        cmode = "on" if gmode == "off" else "off"
        name = action.replace("-", " ").title() + " All"
        nmode = client.STRINGS["inline"]["On"] if gmode == "on" else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{name} {nmode}", data=f"actionall:{chatid}:{page}:{action}:{cmode}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append(get_pages_button(chatid, page))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closepanel")])
    return buttons

@client.Command(command="Panel")
async def addecho(event):
    await event.edit(client.STRINGS["wait"])
    chatid = event.chat_id
    res = await client.inline_query(client.bot.me.username, f"panel:{chatid}:1")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Inline(pattern="panel\:(.*)\:(.*)")
async def inlinepanel(event):
    chatid = event.pattern_match.group(1)
    page = int(event.pattern_match.group(2))
    text = STRINGS["modepage"]
    buttons = get_mode_buttons(chatid, page)
    await event.answer([event.builder.article("FidoSelf - Panel", text=text, buttons=buttons)])

@client.Callback(data="page\:(.*)\:(.*)")
async def panelpages(event):
    chatid = event.data_match.group(1).decode('utf-8')
    page = int(event.data_match.group(2).decode('utf-8'))
    text = TEXTS[page]
    buttons = get_buttons(chatid, page)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="setmode\:(.*)\:(.*)\:(.*)\:(.*)")
async def setmode(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    page = int(event.data_match.group(2).decode('utf-8'))
    mode = event.data_match.group(3).decode('utf-8')
    change = event.data_match.group(4).decode('utf-8')
    client.DB.set_key(mode, change)
    text = STRINGS["modepage"]
    buttons = get_mode_buttons(chatid, page)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="setfonttime\:(.*)\:(.*)\:(.*)")
async def setfonttime(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    page = int(event.data_match.group(2).decode('utf-8'))
    font = event.data_match.group(3).decode('utf-8')
    client.DB.set_key("TIME_FONT", str(font))
    buttons = get_time_buttons(chatid, page)
    await event.edit(buttons=buttons)

@client.Callback(data="seteditall\:(.*)\:(.*)\:(.*)")
async def seteditmodeall(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    page = int(event.data_match.group(2).decode('utf-8'))
    edit = event.data_match.group(3).decode('utf-8')
    last = client.DB.get_key("EDITALL_MODE")
    if str(last) == str(edit):
        client.DB.set_key("EDITALL_MODE", False)
    else:
        client.DB.set_key("EDITALL_MODE", str(edit))
    buttons = get_edit_buttons(chatid, page)
    await event.edit(buttons=buttons)
    
@client.Callback(data="seteditchat\:(.*)\:(.*)\:(.*)")
async def seteditmodechat(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    page = int(event.data_match.group(2).decode('utf-8'))
    edit = event.data_match.group(3).decode('utf-8')
    last = client.DB.get_key("EDITCHATS_MODE") or {}
    if chatid not in last:
        last.update({chatid: ""})
    if last[chatid] != edit:
        last[chatid] = edit
    else:
        last[chatid] = ""
    client.DB.set_key("EDITCHATS_MODE", last)
    buttons = get_edit_buttons(chatid, page)
    await event.edit(buttons=buttons)
    
@client.Callback(data="actionall\:(.*)\:(.*)\:(.*)\:(.*)")
async def actionall(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    page = int(event.data_match.group(2).decode('utf-8'))
    action = event.data_match.group(3).decode('utf-8')
    change = event.data_match.group(4).decode('utf-8')
    action = action.upper() + "_ALL"
    client.DB.set_key(action, change)
    text = STRINGS["actionpage"]
    buttons = get_action_buttons(chatid, page)
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="actionchat\:(.*)\:(.*)\:(.*)\:(.*)")
async def actionschats(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    page = int(event.data_match.group(2).decode('utf-8'))
    action = event.data_match.group(3).decode('utf-8')
    change = event.data_match.group(4).decode('utf-8')
    action = action.upper() + "_CHATS"
    last = client.DB.get_key(action) or []
    if change == "del":
        new = last.remove(chatid)
        client.DB.set_key(action, new)
    elif change == "add":
        new = last + [chatid]
        client.DB.set_key(action, new)
    text = STRINGS["actionpage"]
    buttons = get_action_buttons(chatid, page)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="closepanel")
async def closepanel(event):
    text = STRINGS["close"]
    await event.edit(text=text)
    
@client.Callback(data="Turn\:(on|off)\:(.*)\:(.*)\:(.*)")
async def turner(event):
    Change = event.data_match.group(1).decode('utf-8')
    ChangeMode = event.data_match.group(2).decode('utf-8')
    chatid = int(event.data_match.group(3).decode('utf-8'))
    page = int(event.data_match.group(4).decode('utf-8'))
    client.DB.set_key(Change, ChangeMode)
    pagetext = TEXTS[page]
    schange = client.STRINGS["On"] if Change == "on" else client.STRINGS["Off"]
    settext = STRINGS["change"].format(ChangeMode.title(), schange)
    text = settext + pagetext
    buttons = get_buttons(chatid, page)
    await event.edit(text=text, buttons=buttons)