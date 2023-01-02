from FidoSelf import client
from telethon import Button
from datetime import datetime
from FidoSelf.functions.vars import FONTS, create_font
import time

PAGES_COUNT = 3

def get_pages_button(page):
    buttons = []
    if page < PAGES_COUNT:
        buttons.append(Button.inline(client.get_string("Inline_4"), data=f"panelpage:{page+1}"))
    if page > 1:
        buttons.append(Button.inline(client.get_string("Inline_5"), data=f"panelpage:{page-1}"))
    buttons.append(Button.inline(client.get_string("Inline_3"), data="closepanel"))
    return buttons

def get_mode_buttons(page):
    buttons = []
    MODES = client.get_string("Modes")
    for mode in MODES:
        if mode in ["SELF_ALL_MODE", "QUICKS_MODE", "AUTO_REPLACE_MODE"] and not client.DB.get_key(mode):
            gmode = "on"
            cmode = "on" if gmode == "off" else "off"
            buttons.append([Button.inline(f"• {MODES[mode]} •", data=f"setmode:{page}:{mode}:{cmode}"), Button.inline((client.get_string("Inline_1") if gmode == "on" else client.get_string("Inline_2")), data=f"setmode:{page}:{mode}:{cmode}")])
        elif mode == "LANGUAGE":
            gmode = client.DB.get_key(mode) or client.lang or "en"
            cmode = "en" if gmode == "fa" else "fa"
            buttons.append([Button.inline(f"• {MODES[mode]} •", data=f"setmode:{page}:{mode}:{cmode}"), Button.inline(client.get_string("Lang_2"), data=f"setmode:{page}:{mode}:{cmode}")])
        elif not client.DB.get_key(mode):
            gmode = client.DB.get_key(mode)
            cmode = "on" if gmode == "off" else "off"
            buttons.append([Button.inline(f"• {MODES[mode]} •", data=f"setmode:{page}:{mode}:{cmode}"), Button.inline((client.get_string("Inline_1") if gmode == "on" else client.get_string("Inline_2")), data=f"setmode:{page}:{mode}:{cmode}")])
    pgbts = get_pages_button(page)
    buttons.append(pgbts)
    buttons = client.get_buttons(buttons)
    return buttons

def get_time_buttons(page):
    newtime = datetime.now().strftime("%H:%M")
    last = client.DB.get_key("TIME_FONT") or 1
    buttons = []
    buttons.append([Button.inline(f'• {client.get_string("Random_1")} •', data=f"setfonttime:{page}:random"), Button.inline((client.get_string("Inline_1") if str(last) == "random" else client.get_string("Inline_2")), data=f"setfonttime:{page}:random")])
    buttons.append([Button.inline(f'• {client.get_string("Random_2")} •', data=f"setfonttime:{page}:random2"), Button.inline((client.get_string("Inline_1") if str(last) == "random2" else client.get_string("Inline_2")), data=f"setfonttime:{page}:random2")])
    for font in FONTS:
        buttons.append([Button.inline(f"• {create_font(newtime, font)} •", data=f"setfonttime:{page}:{font}"), Button.inline((client.get_string("Inline_1") if str(last) == str(font) else client.get_string("Inline_2")), data=f"setfonttime:{page}:{font}")])
    pgbts = get_pages_button(page)
    buttons.append(pgbts)
    buttons = client.get_buttons(buttons)
    return buttons

def get_edit_buttons(page):
    last = client.DB.get_key("EDIT_MODE")
    buttons = []
    EDITS = client.get_string("Edits")
    for edit in EDITS:
        buttons.append([Button.inline(f"• {EDITS[edit]} •", data=f"seteditmode:{page}:{edit}"), Button.inline((client.get_string("Inline_1") if str(last) == str(edit) else client.get_string("Inline_2")), data=f"seteditmode:{page}:{edit}")])
    pgbts = get_pages_button(page)
    buttons.append(pgbts)
    buttons = client.get_buttons(buttons)
    return buttons

@client.Cmd(pattern=f"(?i)^\{client.cmd}Panel$")
async def addecho(event):
    await event.edit(client.get_string("Wait"))
    res = await client.inline_query(client.bot.me.username, "selfmainpanel")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Inline(pattern="selfmainpanel")
async def inlinepanel(event):
    text = client.get_string("Panel_1")
    buttons = get_mode_buttons(1)
    await event.answer([event.builder.article(f"{client.str} Smart Self - Panel", text=text, buttons=buttons)])

@client.Callback(data="panelpage\:(.*)")
async def panelpages(event):
    page = int(event.data_match.group(1).decode('utf-8'))
    if page == 1:
        text = client.get_string("Panel_1")
        buttons = get_mode_buttons(page)
        await event.edit(text=text, buttons=buttons)
    elif page == 2:
        text = client.get_string("Panel_2")
        buttons = get_time_buttons(page)
        await event.edit(text=text, buttons=buttons)
    elif page == 3:
        text = client.get_string("Panel_3")
        buttons = get_edit_buttons(page)
        await event.edit(text=text, buttons=buttons)

@client.Callback(data="setmode\:(.*)\:(.*)\:(.*)")
async def setmode(event):
    page = int(event.data_match.group(1).decode('utf-8'))
    mode = event.data_match.group(2).decode('utf-8')
    change = event.data_match.group(3).decode('utf-8')
    if mode == "AFK_MODE":
        client.DB.set_key("AFK_LASTSEEN", str(time.time()))
    if mode == "LANGUAGE":
        client.lang = change
    client.DB.set_key(mode, change)
    buttons = get_mode_buttons(page)
    await event.edit(buttons=buttons)

@client.Callback(data="setfonttime\:(.*)\:(.*)")
async def setfonttime(event):
    page = int(event.data_match.group(1).decode('utf-8'))
    font = event.data_match.group(2).decode('utf-8')
    client.DB.set_key("TIME_FONT", str(font))
    buttons = get_time_buttons(page)
    await event.edit(buttons=buttons)

@client.Callback(data="seteditmode\:(.*)\:(.*)")
async def seteditmode(event):
    page = int(event.data_match.group(1).decode('utf-8'))
    edit = event.data_match.group(2).decode('utf-8')
    last = client.DB.get_key("EDIT_MODE")
    if str(last) == str(edit):
        client.DB.set_key("EDIT_MODE", False)
    else:
        client.DB.set_key("EDIT_MODE", str(edit))
    buttons = get_edit_buttons(page)
    await event.edit(buttons=buttons)

@client.Callback(data="closepanel")
async def closepanel(event):
    text = client.get_string("Panel_4")
    await event.edit(text=text)
