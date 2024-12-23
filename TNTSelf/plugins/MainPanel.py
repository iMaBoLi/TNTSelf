from TNTSelf import client
from telethon import Button
from jdatetime import datetime

__INFO__ = {
    "Category": "Setting",
    "Name": "Panel",
    "Info": {
        "Help": "To Get Panel To Setting Self!",
        "Commands": {
            "{CMD}Panel": {
                "Help": "To Get Panel",
            },
            "{CMD}PanelPv": {
                "Help": "To Get Panel In Your Saved Message",
            },
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
    "editpage": "**❃ Select Which Edit Mode You Want Turn On-Off:**",
    "actionpage": "**❃ Select Which Action Mode You Want Turn On-Off:**",
    "filterpvpage": "**❃ Select Which Media Filter For Your Pv You Want Turn On-Off:**",
    "allpage": "☻︎ You Are Already In This Page!",
    "closepanel":  "**☻︎ The Panel Successfuly Closed!**",
}

def get_modename(mode):
    MODES ={
        "ONLINE_MODE": "Online",
        "QUICK_MODE": "Quicks",
        "NAME_MODE": "Name",
        "BIO_MODE": "Bio",
        "PHOTO_MODE": "Photo",
        "AUTO_MODE": "Auto",
        "SIGN_MODE": "Sign",
        "EMOJI_MODE": "Emoji",
        "TIMER_MODE": "Timer Save",
        "MEDIAPV_MODE": "Media Save",
        "MUTEPV_MODE": "MutePv",
        "LOVKPV_MODE": "LockPv",
        "ANTI_SPAM": "Anti Spam",
        "REPEAT_MODE": "Repeat",
        "REPEAT_CHATS": "Repeat",
        "REACTION_MODE": "Reaction",
        "REACTION_CHATS": "Reaction",
        "POKER_MODE": "Poker",
        "POKER_CHATS": "Poker",
        "ANTIFORWARD_MODE": "Anti Forward",
        "ANTIEDIT_MODE": "Anti Edit",
        "DELENEMY_MSGS": "Delete EnemyPm",
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
        "CHSIGN_MODE": "Sign Channel",
        "ANTISPAMPV_MODE": "AntiSpam Pv",
        "ANTISPAMPVWARN_MODE": "AntiSpam Warn",
        "ANTISPAMPV_TYPE": "AntiSpam Type",
        "TIME_FONT": "Time Font",
        "EDIT_MODE": "Edit",
        "COPYACTION_MODE": "Copy Action",
        "COPYACTION_CHATS": "Copy Action",
        "ACTION_MODE": "Send Action",
        "ACTION_CHATS": "Send Action",
        "ACTION_TYPE": "Action Type",
        "FILTERPV_MEDIA": "Filter Media",
        "FILTERPV_TEXT": "Filter Text",
        "FILTERPV_PHOTO": "Filter Photo",
        "FILTERPV_VIDEO": "Filter Video",
        "FILTERPV_GIF": "Filter Gif",
        "FILTERPV_VOICE": "Filter Voice",
        "FILTERPV_MUSIC": "Filter Music",
        "FILTERPV_STICKER": "Filter Sticker",
        "FILTERPV_FILE": "Filter File",
        "FILTERPV_LINK": "Filter Link",
    }
    if mode in MODES:
        return MODES[mode]
    else:
        return mode.split("_")[0].title()

@client.Command(command="Panel")
async def panel(event):
    await event.edit(client.STRINGS["wait"])
    chatid = event.chat_id
    res = await event.client.inline_query(client.bot.me.username, f"Panel:{chatid}:1")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Command(command="PanelPv")
async def panelpv(event):
    await event.edit(client.STRINGS["wait"])
    chatid = event.chat_id
    res = await event.client.inline_query(client.bot.me.username, f"Panel:{chatid}:1")
    await res[0].click(client.me.id)
    await event.delete()

@client.Inline(pattern="Panel\\:(.*)\\:(.*)")
async def inlinepanel(event):
    chatid = event.pattern_match.group(1)
    page = int(event.pattern_match.group(2))
    await event.answer([event.builder.article("TNTSelf - Panel", text=get_text(page), buttons=get_buttons(event, chatid, page))])

@client.Callback(data="Page\\:(.*)\\:(.*)")
async def panelpages(event):
    chatid = event.data_match.group(1).decode('utf-8')
    page = int(event.data_match.group(2).decode('utf-8'))
    if page == 0:
        return await event.answer(client.getstrings(STRINGS)["allpage"], alert=True)
    await event.edit(text=get_text(page), buttons=get_buttons(event, chatid, page))
    
def get_text(page):
    TEXTS = {
        1: client.getstrings(STRINGS)["modepage"],
        2: client.getstrings(STRINGS)["modepage"],
        3: client.getstrings(STRINGS)["modepage"],
        4: client.getstrings(STRINGS)["fontpage"],
        5: client.getstrings(STRINGS)["editpage"],
        6: client.getstrings(STRINGS)["actionpage"],
        7: client.getstrings(STRINGS)["filterpvpage"]
    }
    mention = client.functions.mention(client.me)
    text = f"**ᯓ Dear** ( {mention} )\n\n"
    text += "  " + TEXTS[page] + "\n"
    text += f"    **❃ Page:** ( `{page}` )"
    return text

def get_pages_button(chatid, opage):
    buttons = []
    PAGES_COUNT = 7
    for page in range(1, PAGES_COUNT + 1):
        apage = page if page != opage else 0
        name = page
        buttons.append(Button.inline(f"( {name} )", data=f"Page:{chatid}:{apage}"))
    return buttons

def create_button(event, key, value, type, settype, chatid, page, default=None, show=None):
    showname = show if show else get_modename(key)
    if type == "Turn":
        getMode = event.client.DB.get_key(key) or default
        value = "ON" if getMode == "OFF" else "OFF"
        svalue = client.STRINGS["inline"]["On"] if getMode == "ON" else client.STRINGS["inline"]["Off"]
        return Button.inline(f"{showname} {svalue}", data=f"Set:{key}:{value}:{settype}:{chatid}:{page}")
    elif type == "Mode":
        getMode = event.client.DB.get_key(key) or default
        svalue = client.STRINGS["inline"]["On"] if str(getMode) == str(value) else client.STRINGS["inline"]["Off"]
        return Button.inline(f"{showname} {svalue}", data=f"Set:{key}:{value}:{settype}:{chatid}:{page}")
    elif type == "Chat":
        chats = event.client.DB.get_key(key) or default
        value = "del" if int(chatid) in chats else "add"
        smode = client.STRINGS["inline"]["On"] if value == "del" else client.STRINGS["inline"]["Off"]
        return Button.inline(f"{showname} {smode}", data=f"Set:{key}:{value}:{settype}:{chatid}:{page}")
    elif type == "ChatMode":
        chats = event.client.DB.get_key(key) or default
        smode = client.STRINGS["inline"]["On"] if (int(chatid) in chats and chats[int(chatid)] == value) else client.STRINGS["inline"]["Off"]
        return Button.inline(f"{showname} {smode}", data=f"Set:{key}:{value}:{settype}:{chatid}:{page}")

def get_buttons(event, chatid, page):
    buttons = []
    if page == 1: 
        for Mode in ["ONLINE_MODE", "QUICK_MODE", "NAME_MODE", "BIO_MODE", "PHOTO_MODE", "AUTO_MODE", "SIGN_MODE", "EMOJI_MODE", "MEDIAPV_MODE", "TIMER_MODE", "MUTEPV_MODE", "LOVKPV_MODE", "ANTI_SPAM"]:
            default = "OFF" if Mode not in ["QUICK_MODE", "ANTI_SPAM"] else "ON"
            button = create_button(event, Mode, None, "Turn", "Turn", chatid, page, default)
            buttons.append(button)
        buttons = list(client.functions.chunks(buttons, 2))
    elif page == 2:
        for Mode in ["REPEAT", "REACTION", "POKER"]:
            chbutton = create_button(event, Mode + "_CHATS", None, "Chat", "Chat", chatid, page, [], Mode.title())
            allbutton = create_button(event, Mode + "_ALL", None, "Turn", "Turn", chatid, page, "OFF", (Mode.title() + " All"))
            buttons.append([chbutton, allbutton])
        othbutton = []
        for Mode in ["ANTIFORWARD_MODE", "ANTIEDIT_MODE", "DELENEMY_MSGS", "AUTODELETE_MODE", "READALL_MODE", "READPV_MODE", "READGP_MODE", "READCH_MODE"]:
            othbutton.append(create_button(event, Mode, None, "Turn", "Turn", chatid, page, "OFF"))
        othbutton.insert(4, create_button(event, "READ_CHATS", None, "Chat", "Chat", chatid, page, [], "MarkRead"))
        buttons = buttons + list(client.functions.chunks(othbutton, 2))
    elif page == 3:
        for Mode in ["AUTOTR_MODE", "COMMENT_MODE", "LOVE_MODE", "ALARM_MODE", "WELCOME_MODE", "GOODBY_MODE", "AUTOJOIN_MODE", "AUTOLEAVE_MODE", "CHSIGN_MODE", "ANTISPAMPV_MODE", "ANTISPAMPVWARN_MODE"]:
            button = create_button(event, Mode, None, "Turn", "Turn", chatid, page, "OFF")
            buttons.append(button)
        buttons = client.functions.chunker(buttons, [2,2,2,2,1,2])
        typebts = [Button.inline("AntiSapm Mode:", data="Empty")]
        for type in ["Mute", "Block"]:
            typebts.append(create_button(event, "ANTISPAMPV_TYPE", type, "Mode", "Mode", chatid, page, "Mute", type))
        buttons.append(typebts)
    elif page == 4:
        newtime = datetime.now().strftime("%H:%M")
        for randfont in ["random", "random2"]:
            buttons.append(create_button(event, "TIME_FONT", randfont, "Mode", "Mode", chatid, page, 1, randfont.title()))
        for font in client.functions.FONTS:
            smode = client.functions.create_font(newtime, font)
            buttons.append(create_button(event, "TIME_FONT", font, "Mode", "Mode", chatid, page, 1, smode))
        buttons = list(client.functions.chunks(buttons, 2))
    elif page == 5:
        buttons = []
        for edit in client.functions.EDITS:
            buttons.append(create_button(event, "EDIT_MODE", edit, "Mode", "ModeDel", chatid, page, "", edit.title()))
        buttons = list(client.functions.chunks(buttons, 2))
    elif page == 6:
        buttons.append([create_button(event, "COPYACTION_CHATS", None, "Chat", "Chat", chatid, page, [], "Copy Action"), create_button(event, "COPYACTION_MODE", None, "Turn", "Turn", chatid, page, "OFF", "Copy Action All")])
        buttons.append([create_button(event, "ACTION_CHATS", None, "Chat", "Chat", chatid, page, [], "Action"), create_button(event, "ACTION_MODE", None, "Turn", "Turn", chatid, page, "OFF", "Action All")])
        actbts = []
        for action in client.functions.ACTIONS:
            actbts.append(create_button(event, "ACTION_TYPE", action, "Mode", "Mode", chatid, page, "random", (action.replace("record-", "Rec ").title())))
        buttons = buttons + list(client.functions.chunks(actbts, 3))
    elif page == 7:
        for Mode in client.functions.PVFILTERS:
            smode = Mode.split("_")[-1].title()
            button = create_button(event, Mode, None, "Turn", "Turn", chatid, page, "OFF", smode)
            buttons.append(button)
        buttons = list(client.functions.chunks(buttons, 2))
    buttons.append(get_pages_button(chatid, page))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="ClosePanel")])
    return buttons
    
@client.Callback(data="Set\\:(.*)\\:(.*)\\:(.*)\\:(.*)\\:(.*)")
async def setpanel(event):
    key = event.data_match.group(1).decode('utf-8')
    value = event.data_match.group(2).decode('utf-8')
    type = event.data_match.group(3).decode('utf-8')
    chatid = int(event.data_match.group(4).decode('utf-8'))
    page = int(event.data_match.group(5).decode('utf-8'))
    skey = get_modename(key)
    pagetext = get_text(page)
    if type == "Turn":
        event.client.DB.set_key(key, value)
        cshow = client.STRINGS["On"] if value == "ON" else client.STRINGS["Off"]
        settext = client.getstrings(STRINGS)["changeturn"].format(skey, cshow)
    elif type == "Mode":
        event.client.DB.set_key(key, value)
        settext = client.getstrings(STRINGS)["changemode"].format(skey, value)
    elif type == "ModeDel":
        gvalue = event.client.DB.get_key(key)
        value = value if value != gvalue else None
        event.client.DB.set_key(key, value)
        if not value:
            settext = client.getstrings(STRINGS)["disablemode"].format(skey)
        else:
            settext = client.getstrings(STRINGS)["changemode"].format(skey, value)
    elif type == "ModeAll":
        event.client.DB.set_key(key, value)
        cshow = client.STRINGS["On"] if value == "ON" else client.STRINGS["Off"]
        settext = client.getstrings(STRINGS)["changeall"].format(skey, cshow)
    elif type == "Chat":
        chats = event.client.DB.get_key(key) or []
        if value == "add":
            chats.append(chatid)
        elif value == "del":
            chats.remove(chatid)
        event.client.DB.set_key(key, chats)
        cshow = client.STRINGS["On"] if value == "add" else client.STRINGS["Off"]
        settext = client.getstrings(STRINGS)["changechat"].format(skey, cshow)
    elif type == "ChatMode":
        chats = event.client.DB.get_key(key) or {}
        if chatid not in chats:
            chats.update({chatid: None})
        chats[chatid] = value
        event.client.DB.set_key(key, chats)
        settext = client.getstrings(STRINGS)["changechatmode"].format(skey, value)
    elif type == "ChatModeDel":
        chats = event.client.DB.get_key(key) or {}
        if chatid not in chats:
            chats.update({chatid: None})
        value = value if chats[chatid] != value else None
        chats[chatid] = value
        event.client.DB.set_key(key, chats)
        if not value:
            settext = client.getstrings(STRINGS)["disablechatmode"].format(skey)
        else:
            settext = client.getstrings(STRINGS)["changechatmode"].format(skey, value)
    text = settext + "\n\n" + pagetext
    buttons = get_buttons(event, chatid, page)
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="ClosePanel")
async def closepanel(event):
    await event.edit(text=client.getstrings(STRINGS)["closepanel"])
    
@client.Callback(data="Empty")
async def empty(event):
    await event.answer(client.STRINGS["inline"]["Show"], alert=True)