from FidoSelf import client
from telethon import Button
from datetime import datetime
from .Action import ACTIONS
from .EditModes import EDITS

STRINGS = {
    "changemode": "**The {} Has Been {}!**",
    "changefont": "**The Time Font Has Been Set To:** ( `{}` )",
    "changeeditchat": "**The Edit Mode For This Chat Has Been Set To:** ( `{}` )",
    "closeeditchat": "**The Edit Mode For This Chat Has Been Disabled!**",
    "changeeditall": "**The Edit Mode Has Been Set To:** ( `{}` )",
    "closeeditall": "**The Edit Mode Has Been Disabled!**",
    "modepage": "**Select Which Mode You Want Turn On-Off:**",
    "fontpage": "**Select Which Time Font You Want Turn On-Off:**",
    "editpage": "**Select Which Edit Mode You Want Turn On-Off:**",
    "actionpage": "**Select Which Action Mode You Want Turn On-Off:**",
    "closepanel": "**The Panel Successfuly Closed!**",
}

MODES ={
    1: {
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
    },
    2: {
        "READALL_MODE": "Read All",
        "READPV_MODE": "Read Pv",
        "READGP_MODE": "Read Group",
        "READCH_MODE": "Read Channel",
    },
}

TEXTS = {
    1: STRINGS["modepage"],
    2: STRINGS["modepage"],
    3: STRINGS["fontpage"],
    4: STRINGS["editpage"],
    5: STRINGS["actionpage"],
}

@client.Command(command="Panel")
async def panel(event):
    await event.edit(client.STRINGS["wait"])
    res = await client.inline_query(client.bot.me.username, f"Panel:{event.chat_id}:1")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="Panel\:(.*)\:(.*)")
async def inlinepanel(event):
    chatid = event.pattern_match.group(1)
    page = int(event.pattern_match.group(2))
    await event.answer([event.builder.article("FidoSelf - Panel", text=TEXTS[page], buttons=get_buttons(chatid, page))])

@client.Callback(data="Page\:(.*)\:(.*)")
async def panelpages(event):
    chatid = event.data_match.group(1).decode('utf-8')
    page = int(event.data_match.group(2).decode('utf-8'))
    text = TEXTS[1] if page in MODES.keys() else TEXTS[page]
    await event.edit(text=text, buttons=get_buttons(chatid, page))

def get_pages_button(chatid, opage):
    buttons = []
    PAGES_COUNT = len(TEXTS) + 1
    for page in range(1, PAGES_COUNT):
        font = 4 if page != opage else 5
        name = client.functions.create_font(page, font)
        buttons.append(Button.inline(f"( {name} )", data=f"Page:{chatid}:{page}"))
    return buttons

def get_buttons(chatid, page):
    buttons = []
    ModePages = len(MODES)
    if page in MODES.keys():
        for Mode in MODES[page]:
            Modes = MODES[page]
            getMode = client.DB.get_key(Mode) or "off"
            ChangeMode = "on" if getMode == "off" else "off"
            ShowMode = client.STRINGS["inline"]["On"] if getMode == "on" else client.STRINGS["inline"]["Off"]
            buttons.append(Button.inline(f"{Modes[Mode]} {ShowMode}", data=f"Change:{Mode}:{ChangeMode}:{chatid}:{page}"))
    elif page == (ModePages + 1):
        newtime = datetime.now().strftime("%H:%M")
        lastFont = client.DB.get_key("TIME_FONT") or 1
        Mode = "TIME_FONT"
        for randfont in ["random", "random2"]:
            ShowMode = client.STRINGS["inline"]["On"] if str(lastFont) == randfont else client.STRINGS["inline"]["Off"]
            buttons.append(Button.inline(f"{randfont.title()} {ShowMode}", data=f"Change:{Mode}:{randfont}:{chatid}:{page}"))
        for font in client.functions.FONTS:
            ShowName = client.functions.create_font(newtime, font)
            ShowMode = client.STRINGS["inline"]["On"] if str(lastFont) == str(font) else client.STRINGS["inline"]["Off"]
            buttons.append(Button.inline(f"{ShowName} {ShowMode}", data=f"Change:{Mode}:{font}:{chatid}:{page}"))
    elif page == (ModePages + 2):
        EditMode = client.DB.get_key("EDITALL_MODE")
        EditChats = client.DB.get_key("EDITCHATS_MODE") or {}
        for Edit in EDITS:
            ChangeMode = "EDITCHATS_MODE"
            getMode = "off" if (chatid in EditChats and EditChats[chatid] == Edit) else "on"
            ShowMode = client.STRINGS["inline"]["On"] if getMode == "off" else client.STRINGS["inline"]["Off"]
            buttons.append(Button.inline(f"{Edit} {ShowMode}", data=f"Change:{ChangeMode}:{Edit}:{chatid}:{page}"))
        for Edit in EDITS:
            ChangeMode = "EDITALL_MODE"
            ShowName = Edit + " All"
            ShowMode = client.STRINGS["inline"]["On"] if str(EditMode) == str(Edit) else client.STRINGS["inline"]["Off"]
            buttons.append(Button.inline(f"{ShowName} {ShowMode}", data=f"Change:{ChangeMode}:{Edit}:{chatid}:{page}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append(get_pages_button(chatid, page))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="ClosePanel")])
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
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="ClosePanel")])
    return buttons

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
    
@client.Callback(data="Change\:(.*)\:(.*)\:(.*)\:(.*)")
async def Changer(event):
    ChangeMode = event.data_match.group(1).decode('utf-8')
    Change = event.data_match.group(2).decode('utf-8')
    chatid = int(event.data_match.group(3).decode('utf-8'))
    page = int(event.data_match.group(4).decode('utf-8'))
    ModePages = len(MODES)
    if page in MODES.keys():
        client.DB.set_key(ChangeMode, Change)
        pagetext = TEXTS[1]
        schange = client.STRINGS["On"] if Change == "on" else client.STRINGS["Off"]
        settext = STRINGS["changemode"].format(ChangeMode.title(), schange)
        text = settext + "\n" + pagetext
    elif page == (ModePages + 1):
        client.DB.set_key(ChangeMode, Change)
        pagetext = TEXTS[page]
        settext = STRINGS["changefont"].format(Change)
        text = settext + "\n" + pagetext
    elif page == (ModePages + 2):
        pagetext = TEXTS[page]
        if ChangeMode == "EDITCHATS_MODE":
            EditChats = client.DB.get_key("EDITCHATS_MODE") or {}
            if chatid not in EditChats:
                EditChats.update({chatid: ""})
            EditChats[chatid] = Change if EditChats[chatid] != Change else ""
            client.DB.set_key("EDITCHATS_MODE", EditChats)
            settext = STRINGS["changeeditchat"].format(Change) if EditChats[chatid] != Change else STRINGS["closeeditchat"]
        else:
            EditMode = client.DB.get_key("EDITALL_MODE")
            if str(EditMode) == str(Change):
                client.DB.set_key("EDITALL_MODE", False)
                settext = STRINGS["closeeditall"]
            else:
                client.DB.set_key("EDITALL_MODE", str(Change))
                settext = STRINGS["changeeditall"].format(Change) 
        text = settext + "\n" + pagetext
    buttons = get_buttons(chatid, page)
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="ClosePanel")
async def closepanel(event):
    await event.edit(text=STRINGS["closepanel"])