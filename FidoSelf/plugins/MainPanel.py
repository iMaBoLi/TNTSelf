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
    "actionall": "**➜ The Send Chat Action Has Been {}!**",
    "actionchat": "**➜ The Send Chat Action For This Chat Has Been {}!**",
    "setaction":  "**➜ The Send Action Mode Was Set To** ( `{}` )",
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
        "SIGN_MODE": "Sign",
        "EMOJI_MODE": "Emoji",
        "TIMER_MODE": "Timer Save",
        "ANTISPAM_PV": "AntiSpam Pv",
        "MUTE_PV": "Mute Pv",
        "LOCK_PV": "Lock Pv",
    },
    2: {
        "ENEMY_DELETE": "Delete Enemy Pms",
        "READALL_MODE": "Read All",
        "READPV_MODE": "Read Pv",
        "READGP_MODE": "Read Group",
        "READCH_MODE": "Read Channel",
    },
}

@client.Command(command="Panel")
async def panel(event):
    await event.edit(client.STRINGS["wait"])
    chatid = event.chat_id
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
    if page == 0:
        return await event.answer(STRINGS["allpage"], alert=True)
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
        data = page if page != opage else 0
        name = client.functions.create_font(page, font)
        buttons.append(Button.inline(f"( {name} )", data=f"Page:{chatid}:{data}"))
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
        acMode = client.DB.get_key("ACTION_ALL") or "off"
        acChats = client.DB.get_key("ACTION_CHATS") or []
        Mact = client.STRINGS["inline"]["On"] if int(chatid) in acChats else client.STRINGS["inline"]["Off"]
        Cact = "del" if int(chatid) in acChats else "add"
        Mactall = client.STRINGS["inline"]["On"] if acMode == "on" else client.STRINGS["inline"]["Off"]
        Cactall = "on" if acMode == "off" else "off"
        buttons = [[Button.inline(f"Action {Mact}", data=f"SetPanel:ACTION_CHATS:{Cact}:{chatid}:{page}"), Button.inline(f"Action All {Mactall}", data=f"SetPanel:ACTION_ALL:{Cactall}:{chatid}:{page}")]]
        actbts = []
        for action in client.functions.ACTIONS:
            acType = client.DB.get_key("ACTION_TYPE") or "random"
            getMode = "on" if action == acType else "off"
            ShowName = action.replace("-", " ").title()
            ShowMode = client.STRINGS["inline"]["On"] if getMode == "on" else client.STRINGS["inline"]["Off"]
            actbts.append(Button.inline(f"{ShowName} {ShowMode}", data=f"SetPanel:ACTION_TYPE:{action}:{chatid}:{page}"))
        actbts = list(client.functions.chunks(actbts, 3))
        buttons += actbts
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
        if ChangeMode.endswith("TYPE"):
            ShowName = Change.replace("-", " ").title()
            settext = STRINGS["setaction"].format(ShowName) 
            client.DB.set_key("ACTION_TYPE", Change)
        elif ChangeMode.endswith("ALL"):
            client.DB.set_key(ChangeMode, Change)
            ShowChange = client.STRINGS["On"] if Change == "on" else client.STRINGS["Off"]
            settext = STRINGS["actionall"].format(ShowChange)
        else:
            acChats = client.DB.get_key("ACTION_CHATS") or []
            if Change == "add":
                if chatid not in acChats:
                    acChats.append(chatid)
                    client.DB.set_key("ACTION_CHATS", acChats)
            elif Change == "del":
                if chatid in acChats:
                    acChats.remove(chatid)
                    client.DB.set_key("ACTION_CHATS", acChats)
            ShowChange = client.STRINGS["On"] if Change == "add" else client.STRINGS["Off"]
            settext = STRINGS["actionchat"].format(ShowChange) 
        text = settext + "\n\n" + pagetext
    buttons = get_buttons(chatid, page)
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="ClosePanel")
async def closepanel(event):
    await event.edit(text=STRINGS["closepanel"])
    
@client.Callback(data="Empty")
async def empty(event):
    await event.answer(client.STRINGS["inline"]["Show"], alert=True)