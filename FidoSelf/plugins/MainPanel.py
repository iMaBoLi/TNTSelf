from FidoSelf import client
from telethon import Button
from jdatetime import datetime

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
    "changeturn":  "**➜ The {} Has Been {}!**",
    "changemode":  "**➜ The {} Has Been Set To:** ( `{}` )",
    "disablemode":  "**➜ The {} Has Been Disabled!**",
    "changeall":  "**➜ The {} For All Chats Has Been {}!**",
    "changechat":  "**➜ The {} For This Chat Has Been {}!**",
    "changechatmode":  "**➜ The {} For This Chat Has Been Set To:** ( `{}` )",
    "disablechatmode":  "**➜ The {} For This Chat Has Been Disabled!**",
    "modepage": "**❃ Select Which Mode You Want Turn On-Off:**",
    "fontpage": "**❃ Select Which Time Font You Want Turn On-Off:**",
    "editpage": "**❃ Select Which edit Mode You Want Turn On-Off:**",
    "actionpage": "**❃ Select Which Action Mode You Want Turn On-Off:**",
    "allpage": "☻︎ You Are Already In This Page!",
    "closepanel":  "**☻︎ The Panel Successfuly Closed!**",
}

def get_modename(mode):
    MODES ={
        "ONLINE_MODE": "Online",
        "QUICKS_MODE": "Quicks",
        "ANTI_SPAM": "Anti Spam",
        "NAME_MODE": "Name",
        "BIO_MODE": "Bio",
        "PHOTO_MODE": "Photo",
        "AUTO_MODE": "Auto",
        "SIGN_MODE": "Sign",
        "EMOJI_MODE": "Emoji",
        "TIMER_MODE": "Timer Save",
        "MUTE_PV": "MutePv",
        "LOCK_PV": "LockPv",
        "REPEAT_ALL": "Repeat",
        "REPEAT_CHATS": "Repeat",
        "REACTION_ALL": "Reaction",
        "REACTION_CHATS": "Reaction",
        "POKER_ALL": "Poker",
        "POKER_CHATS": "Poker",
        "ANTIFORWARD_MODE": "Anti Forward",
        "ANTIEDIT_MODE": "Anti Edit",
        "ENEMY_DELETE": "Delete EnemyPm",
        "AUTODELETE_MODE": "Auto Delete",
        "READ_CHATS": "MarkRead",
        "READALL_MODE": "MarkRead All",
        "READPV_MODE": "MarkRead Pv",
        "READGP_MODE": "MarkRead Group",
        "READCH_MODE": "MarkRead Channel",
        "AUTOTR_MODE": "Translate",
        "COMMENT_MODE": "Comment",
        "LOVE_MODE": "Love",
        "ALARM_MODE": "Alarm",
        "WELCOME_MODE": "WelCome",
        "GOODBY_MODE": "GoodBy",
        "AUTOJOIN_MODE": "Auto Join",
        "AUTOLEAVE_MODE": "Auto Leave",
        "ANTISPAM_PV": "AntiSpam Pv",
        "ANTISPAM_WARN": "AntiSpam Warn",
        "ANTISPAM_TYPE": "AntiSpam Type",
        "TIME_FONT": "Time Font",
        "EDITALL_MODE": "Edit",
        "EDITCHATS_MODE": "Edit",
        "ACTION_ALL": "Send Action",
        "ACTION_CHATS": "Send Action",
        "ACTION_TYPE": "Action Type",
    }
    if mode in MODES:
        return MODES[mode]
    else:
        return mode.split("_")[0].title()

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
    TEXTS = {
        1: STRINGS["modepage"],
        2: STRINGS["modepage"],
        3: STRINGS["modepage"],
        4: STRINGS["fontpage"],
        5: STRINGS["editpage"],
        6: STRINGS["actionpage"]
    }
    text = TEXTS[page]
    return text + f" **(** `Page {page}` **)**"

def get_pages_button(chatid, opage):
    buttons = []
    PAGES_COUNT = 6
    for page in range(1, PAGES_COUNT + 1):
        font = 4 if page != opage else 5
        data = page if page != opage else 0
        name = client.functions.create_font(page, font)
        buttons.append(Button.inline(f"( {name} )", data=f"Page:{chatid}:{data}"))
    return buttons

def create_button(key, value, type, settype, chatid, page, default=None, show=None):
    showname = show if show else get_modename(key)
    if type == "Turn":
        getMode = client.DB.get_key(key) or default
        value = "ON" if getMode == "OFF" else "OFF"
        svalue = client.STRINGS["inline"]["On"] if getMode == "ON" else client.STRINGS["inline"]["Off"]
        return Button.inline(f"{showname} {svalue}", data=f"Set:{key}:{value}:{settype}:{chatid}:{page}")
    elif type == "Mode":
        getMode = client.DB.get_key(key) or default
        svalue = client.STRINGS["inline"]["On"] if str(getMode) == str(value) else client.STRINGS["inline"]["Off"]
        return Button.inline(f"{showname} {svalue}", data=f"Set:{key}:{value}:{settype}:{chatid}:{page}")
    elif type == "Chat":
        chats = client.DB.get_key(key) or default
        value = "del" if int(chatid) in chats else "add"
        smode = client.STRINGS["inline"]["On"] if value == "del" else client.STRINGS["inline"]["Off"]
        return Button.inline(f"{showname} {smode}", data=f"Set:{key}:{value}:{settype}:{chatid}:{page}")
    elif type == "ChatMode":
        chats = client.DB.get_key(key) or default
        smode = client.STRINGS["inline"]["On"] if (chatid in chats and chats[chatid] == value) else client.STRINGS["inline"]["Off"]
        return Button.inline(f"{showname} {smode}", data=f"Set:{key}:{value}:{settype}:{chatid}:{page}")

def get_buttons(chatid, page):
    buttons = []
    if page == 1: 
        for Mode in ["ONLINE_MODE", "NAME_MODE", "BIO_MODE", "PHOTO_MODE", "AUTO_MODE", "SIGN_MODE", "EMOJI_MODE", "TIMER_MODE", "MUTE_PV", "LOCK_PV"]:
            button = create_button(Mode, None, "Turn", "Turn", chatid, page, "OFF")
            buttons.append(button)
        buttons.insert(1, create_button("QUICKS_MODE", None, "Turn", "Turn", chatid, page, "ON"))
        buttons.insert(5, create_button("ANTI_SPAM", None, "Turn", "Turn", chatid, page, "ON"))
        buttons = list(client.functions.chunks(buttons, 2))
    elif page == 2:
        for Mode in ["REPEAT", "REACTION", "POKER"]:
            chbutton = create_button(Mode + "_CHATS", None, "Chat", "Chat", chatid, page, [], Mode.title())
            allbutton = create_button(Mode + "_ALL", None, "Turn", "Turn", chatid, page, "OFF", (Mode.title() + " All"))
            buttons.append([chbutton, allbutton])
        othbutton = []
        for Mode in ["ANTIFORWARD_MODE", "ANTIEDIT_MODE", "ENEMY_DELETE", "AUTODELETE_MODE", "READALL_MODE", "READPV_MODE", "READGP_MODE", "READCH_MODE"]:
            othbutton.append(create_button(Mode, None, "Turn", "Turn", chatid, page, "OFF"))
        othbutton.insert(4, create_button("READ_CHATS", None, "Chat", "Chat", chatid, page, [], "MarkRead"))
        buttons = buttons + list(client.functions.chunks(othbutton, 2))
    elif page == 3:
        for Mode in ["AUTOTR_MODE", "COMMENT_MODE", "LOVE_MODE", "ALARM_MODE", "WELCOME_MODE", "GOODBY_MODE", "AUTOJOIN_MODE", "AUTOLEAVE_MODE", "ANTISPAM_PV", "ANTISPAM_WARN"]:
            button = create_button(Mode, None, "Turn", "Turn", chatid, page, "OFF")
            buttons.append(button)
        buttons = list(client.functions.chunks(buttons, 2))
        typebts = [Button.inline("• AntiSapm Mode :", data="Empty")]
        for type in ["Mute", "Block"]:
            typebts.append(create_button("ANTISPAM_TYPE", type, "Mode", "Mode", chatid, page, "Mute", type))
        buttons.append(typebts)
    elif page == 4:
        newtime = datetime.now().strftime("%H:%M")
        for randfont in ["random", "random2"]:
            buttons.append(create_button("TIME_FONT", randfont, "Mode", "Mode", chatid, page, 1, randfont.title()))
        for font in client.functions.FONTS:
            smode = client.functions.create_font(newtime, font)
            buttons.append(create_button("TIME_FONT", font, "Mode", "Mode", chatid, page, 1, smode))
        buttons = list(client.functions.chunks(buttons, 2))
    elif page == 5:
        chbts, allbts = [], []
        for edit in client.functions.EDITS:
            chbts.append(create_button("EDITCHATS_MODE", edit, "ChatMode", "ChatModeDel", chatid, page, 1, edit.title()))
            allbts.append(create_button("EDITALL_MODE", edit, "Mode", "ModeDel", chatid, page, 1, (edit.title() + "All")))
        buttons = list(client.functions.chunks(chbts, 3)) + list(client.functions.chunks(allbts, 3))
    elif page == 6:
        buttons.append([create_button("ACTION_ALL", None, "Turn", "Turn", chatid, page, "OFF", "Action All"), create_button("ACTION_CHATS", None, "Chat", "Chat", chatid, page, [], "Action")])
        actbts = []
        for action in client.functions.ACTIONS:
            actbts.append(create_button("ACTION_TYPE", action, "Mode", "Mode", chatid, page, "random", (action.replace("record-", "Rec ").title())))
        buttons = buttons + list(client.functions.chunks(actbts, 3))
    buttons.append(get_pages_button(chatid, page))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="ClosePanel")])
    return buttons
    
@client.Callback(data="Set\:(.*)\:(.*)\:(.*)\:(.*)\:(.*)")
async def setpanel(event):
    key = event.data_match.group(1).decode('utf-8')
    value = event.data_match.group(2).decode('utf-8')
    type = event.data_match.group(3).decode('utf-8')
    chatid = int(event.data_match.group(4).decode('utf-8'))
    page = int(event.data_match.group(5).decode('utf-8'))
    skey = get_modename(key)
    pagetext = get_text(page)
    if type == "Turn":
        client.DB.set_key(key, value)
        cshow = client.STRINGS["On"] if value == "ON" else client.STRINGS["Off"]
        settext = STRINGS["changeturn"].format(skey, cshow)
    elif type == "Mode":
        client.DB.set_key(key, value)
        settext = STRINGS["changemode"].format(skey, value)
    elif type == "ModeDel":
        gvalue = client.DB.get_key(key)
        value = value if value != gvalue else None
        client.DB.set_key(key, value)
        if not value:
            settext = STRINGS["disablemode"].format(skey)
        else:
            settext = STRINGS["changemode"].format(skey, value)
    elif type == "ModeAll":
        client.DB.set_key(key, value)
        cshow = client.STRINGS["On"] if value == "ON" else client.STRINGS["Off"]
        settext = STRINGS["changeall"].format(skey, cshow)
    elif type == "Chat":
        chats = client.DB.get_key(key) or []
        if value == "add":
            chats.append(chatid)
        elif value == "del":
            chats.remove(chatid)
        client.DB.set_key(key, chats)
        cshow = client.STRINGS["On"] if value == "add" else client.STRINGS["Off"]
        settext = STRINGS["changechat"].format(skey, cshow)
    elif type == "ChatMode":
        chats = client.DB.get_key(key) or {}
        if chatid not in chats:
            chats.update({chatid: None})
        chats[chatid] = value
        client.DB.set_key(key, chats)
        settext = STRINGS["changechatmode"].format(skey, value)
    elif type == "ChatModeDel":
        chats = client.DB.get_key(key) or {}
        if chatid not in chats:
            chats.update({chatid: None})
        value = value if chats[chatid] != value else None
        chats[chatid] = value
        client.DB.set_key(key, chats)
        if not value:
            settext = STRINGS["disablechatmode"].format(skey)
        else:
            settext = STRINGS["changechatmode"].format(skey, value)
    text = settext + "\n\n" + pagetext
    buttons = get_buttons(chatid, page)
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="ClosePanel")
async def closepanel(event):
    await event.edit(text=STRINGS["closepanel"])
    
@client.Callback(data="Empty")
async def empty(event):
    await event.answer(client.STRINGS["inline"]["Show"], alert=True)