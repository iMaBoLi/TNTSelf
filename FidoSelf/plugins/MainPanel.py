from FidoSelf import client
from telethon import Button
from datetime import datetime

__INFO__ = {
    "Category": "Setting",
    "Plugname": "Panel",
    "Pluginfo": {
        "Help": "To Get Inline Panel To Setting Self!",
        "Commands": {
            "{CMD}Panel": None,
            "{CMD}Panel <ChatID>": "To Get Panel For Other Chat!",
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "changemode":  "**➜ The {} Has Been {}!**",
    "changefont":  "**➜ The Time Font Has Been Set To:** ( `{}` )",
    "changeeditchat":  "**➜ The Edit Mode For This Chat Has Been Set To:** ( `{}` )",
    "closeeditchat":  "**➜ The Edit Mode For This Chat Has Been Disabled!**",
    "changeeditall":  "**➜ The Edit Mode Has Been Set To:** ( `{}` )",
    "closeeditall":  "**➜ The Edit Mode Has Been Disabled!**",
    "changeactionchat":  "**➜ The Action Chat** ( `{}` ) **For This Chat Has Been {}!**",
    "changeactionall":  "**➜ The Action Chat** ( `{}` ) **Has Been {}!**",
    "modepage": "**❃ Select Which Mode You Want Turn On-Off:**",
    "fontpage": "**❃ Select Which Time Font You Want Turn On-Off:**",
    "editpage": "**❃ Select Which Edit Mode You Want Turn On-Off:**",
    "actionpage": "**❃ Select Which Action Mode You Want Turn On-Off:**",
    "sleeppage": "**❃ Select Which Mode You Want Setting Sleep-Limit:**",
    "allpage": "☻︎ You Are Already In This Page!",
    "closepanel":  "**☻︎ The Panel Successfuly Closed!**",
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

@client.Command(command="Panel ?(.*)?")
async def panel(event):
    await event.edit(client.STRINGS["wait"])
    result, chatid = await event.chatid(event.pattern_match.group(1))
    if not result and str(chatid) == "Invalid":
        return await event.edit(client.STRINGS["getid"]["IU"])
    elif not result and not chatid:
        return await event.edit(client.STRINGS["getid"]["UC"])
    res = await client.inline_query(client.bot.me.username, f"Panel:{chatid}:1")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="Panel\:(.*)\:(.*)")
async def inlinepanel(event):
    chatid = event.pattern_match.group(1)
    page = int(event.pattern_match.group(2))
    await event.answer([event.builder.article("FidoSelf - Panel", text=get_text(page), buttons=get_buttons(chatid, page))])

@client.Callback(data="Page\:(.*)\:(.*)")
async def panelpages(event):
    chatid = event.data_match.group(1).decode('utf-8')
    page = int(event.data_match.group(2).decode('utf-8'))
    await event.edit(text=get_text(page), buttons=get_buttons(chatid, page))

def get_text(page):
    ModePages = len(MODES)
    if page in MODES.keys():
        text = STRINGS["modepage"]
    elif page == (ModePages + 1):
        text = STRINGS["fontpage"]
    elif page == (ModePages + 2):
        text = STRINGS["editpage"]
    elif page == (ModePages + 3):
        text = STRINGS["actionpage"]
    elif page == (ModePages + 4):
        text = STRINGS["sleeppage"]
    return text + f" **(** `Page {page}` **)**"

def get_pages_button(chatid, opage):
    buttons = []
    PAGES_COUNT = len(MODES) + 4 + 1
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
            buttons.append(Button.inline(f"{Modes[Mode]} {ShowMode}", data=f"SetPanel:{Mode}:{ChangeMode}:{chatid}:{page}"))
        buttons = list(client.functions.chunks(buttons, 2))
    elif page == (ModePages + 1):
        newtime = datetime.now().strftime("%H:%M")
        lastFont = client.DB.get_key("TIME_FONT") or 1
        Mode = "TIME_FONT"
        for randfont in ["random", "random2"]:
            ShowMode = client.STRINGS["inline"]["On"] if str(lastFont) == randfont else client.STRINGS["inline"]["Off"]
            buttons.append(Button.inline(f"{randfont.title()} {ShowMode}", data=f"SetPanel:{Mode}:{randfont}:{chatid}:{page}"))
        for font in client.functions.FONTS:
            ShowName = client.functions.create_font(newtime, font)
            ShowMode = client.STRINGS["inline"]["On"] if str(lastFont) == str(font) else client.STRINGS["inline"]["Off"]
            buttons.append(Button.inline(f"{ShowName} {ShowMode}", data=f"SetPanel:{Mode}:{font}:{chatid}:{page}"))
        buttons = list(client.functions.chunks(buttons, 2))
    elif page == (ModePages + 2):
        EditMode = client.DB.get_key("EDITALL_MODE")
        EditChats = client.DB.get_key("EDITCHATS_MODE") or {}
        Chbuttons = []
        Allbuttons = []
        for Edit in client.functions.EDITS:
            ChangeMode = "EDITCHATS_MODE"
            getMode = "off" if (int(chatid) in EditChats and EditChats[int(chatid)] == Edit) else "on"
            ShowMode = client.STRINGS["inline"]["On"] if getMode == "off" else client.STRINGS["inline"]["Off"]
            Chbuttons.append(Button.inline(f"{Edit} {ShowMode}", data=f"SetPanel:{ChangeMode}:{Edit}:{chatid}:{page}"))
        for Edit in client.functions.EDITS:
            ChangeMode = "EDITALL_MODE"
            ShowName = Edit + " All"
            ShowMode = client.STRINGS["inline"]["On"] if str(EditMode) == str(Edit) else client.STRINGS["inline"]["Off"]
            Allbuttons.append(Button.inline(f"{ShowName} {ShowMode}", data=f"SetPanel:{ChangeMode}:{Edit}:{chatid}:{page}"))
        OthButton = [[Button.inline(" --------------- ", data="Empty")]]
        buttons = list(client.functions.chunks(Chbuttons, 3)) + OthButton + list(client.functions.chunks(Allbuttons, 3))
    elif page == (ModePages + 3):
        Chbuttons = []
        Allbuttons = []
        for action in client.functions.ACTIONS:
            acName = action.upper() + "_CHATS"
            acChats = client.DB.get_key(acName) or []
            getMode = "del" if (int(chatid) in acChats or str(chatid) in acChats) else "add"
            ShowName = action.replace("-", " ").title()
            ShowMode = client.STRINGS["inline"]["On"] if getMode == "del" else client.STRINGS["inline"]["Off"]
            Chbuttons.append(Button.inline(f"{ShowName} {ShowMode}", data=f"SetPanel:{acName}:{getMode}:{chatid}:{page}"))
        for action in client.functions.ACTIONS:
            acName = action.upper() + "_ALL"
            getMode = client.DB.get_key(acName) or "off"
            ChangeMode = "on" if getMode == "off" else "off"
            ShowName = action.replace("-", " ").title() + " All"
            ShowMode = client.STRINGS["inline"]["On"] if getMode == "on" else client.STRINGS["inline"]["Off"]
            Allbuttons.append(Button.inline(f"{ShowName} {ShowMode}", data=f"SetPanel:{acName}:{ChangeMode}:{chatid}:{page}"))
        OthButton = [[Button.inline(" --------------- ", data="Empty")]]
        buttons = list(client.functions.chunks(Chbuttons, 3)) + OthButton + list(client.functions.chunks(Allbuttons, 3))
    buttons.append(get_pages_button(chatid, page))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="ClosePanel")])
    return buttons
    
@client.Callback(data="SetPanel\:(.*)\:(.*)\:(.*)\:(.*)")
async def SetPanel(event):
    ChangeMode = event.data_match.group(1).decode('utf-8')
    Change = event.data_match.group(2).decode('utf-8')
    chatid = int(event.data_match.group(3).decode('utf-8'))
    page = int(event.data_match.group(4).decode('utf-8'))
    ModePages = len(MODES)
    if page in MODES.keys():
        client.DB.set_key(ChangeMode, Change)
        pagetext = get_text(page)
        ShowChange = client.STRINGS["On"] if Change == "on" else client.STRINGS["Off"]
        ShowMode = MODES[page][ChangeMode]
        settext = STRINGS["changemode"].format(ShowMode, ShowChange)
        text = settext + "\n\n" + pagetext
    elif page == (ModePages + 1):
        client.DB.set_key(ChangeMode, Change)
        pagetext = get_text(page)
        settext = STRINGS["changefont"].format(Change)
        text = settext + "\n\n" + pagetext
    elif page == (ModePages + 2):
        pagetext = get_text(page)
        if ChangeMode == "EDITCHATS_MODE":
            EditChats = client.DB.get_key("EDITCHATS_MODE") or {}
            if chatid not in EditChats:
                EditChats.update({chatid: ""})
            EditChats[chatid] = Change if EditChats[chatid] != Change else ""
            client.DB.set_key("EDITCHATS_MODE", EditChats)
            settext = STRINGS["changeeditchat"].format(Change) if EditChats[chatid] == Change else STRINGS["closeeditchat"]
        else:
            EditMode = client.DB.get_key("EDITALL_MODE")
            if str(EditMode) == str(Change):
                client.DB.set_key("EDITALL_MODE", False)
                settext = STRINGS["closeeditall"]
            else:
                client.DB.set_key("EDITALL_MODE", str(Change))
                settext = STRINGS["changeeditall"].format(Change) 
        text = settext + "\n\n" + pagetext
    elif page == (ModePages + 3):
        pagetext = get_text(page)
        if ChangeMode.endswith("CHATS"):
            acChats = client.DB.get_key(ChangeMode) or []
            ShowMode = ChangeMode.split("_")[0].title()
            if Change == "add":
                NewChats = acChats + [chatid]
                settext = STRINGS["changeactionchat"].format(ShowMode, client.STRINGS["On"]) 
            elif Change == "del":
                NewChats = acChats.remove(chatid)
                settext = STRINGS["changeactionchat"].format(ShowMode, client.STRINGS["Off"]) 
            client.DB.set_key(ChangeMode, NewChats)
        else:
            client.DB.set_key(ChangeMode, Change)
            ShowMode = ChangeMode.split("_")[0].title()
            ShowChange = client.STRINGS["On"] if Change == "on" else client.STRINGS["Off"]
            settext = STRINGS["changeactionall"].format(ShowMode, ShowChange) 
        text = settext + "\n\n" + pagetext
    buttons = get_buttons(chatid, page)
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="ClosePanel")
async def closepanel(event):
    await event.edit(text=STRINGS["closepanel"])
    
@client.Callback(data="Empty")
async def empty(event):
    await event.answer(client.STRINGS["inline"]["Show"], alert=True)