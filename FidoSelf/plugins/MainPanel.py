from FidoSelf import client
from telethon import Button
from datetime import datetime
from FidoSelf.plugins.ManageTime import FONTS, create_font

PAGES_COUNT = 3

def get_pages_button(page):
    buttons = []
    if page > 1:
        buttons.append(Button.inline("◀️ Back", data=f"panelpage:{page-1}"))
    if page < PAGES_COUNT:
        buttons.append(Button.inline("Next ▶️", data=f"panelpage:{page+1}"))
    buttons.append(Button.inline("🚫 Close 🚫", data="closepanel"))
    return buttons

def get_mode_buttons(page):
    buttons = []
    MODES = {
        "SELF_ALL_MODE": "Self Mode",
        "QUICKS_MODE": "Quicks",
        "NAME_MODE": "Name",
        "BIO_MODE": "Bio",
        "PHOTO_MODE": "Photo",
        "SMART_MONSHI_MODE": "Smart Monshi",
        "OFFLINE_MONSHI_MODE": "Offline Monshi",
        "TIMER_MODE": "Timer Save",
    }
    for mode in MODES: 
        gmode = client.DB.get_key(mode) or "off"
        cmode = "on" if gmode == "off" else "off"
        buttons.append([Button.inline(f"• {MODES[mode]} •", data=f"setmode:{page}:{mode}:{cmode}"), Button.inline(("✔️|Active" if gmode == "on" else "✖️|DeActive"), data=f"setmode:{page}:{mode}:{cmode}")])
    pgbts = get_pages_button(page)
    buttons.append(pgbts)
    return buttons

def get_time_buttons(page):
    newtime = datetime.now().strftime("%H:%M")
    last = client.DB.get_key("TIME_FONT") or 1
    buttons = []
    buttons.append([Button.inline("• Random •", data=f"setfonttime:{page}:random"), Button.inline(("✔️|Active" if str(last) == "random" else "✖️|DeActive"), data=f"setfonttime:{page}:random")])
    buttons.append([Button.inline("• Random 2 •", data=f"setfonttime:{page}:random2"), Button.inline(("✔️|Active" if str(last) == "random2" else "✖️|DeActive"), data=f"setfonttime:{page}:random2")])
    for font in FONTS:
        buttons.append([Button.inline(f"• {create_font(newtime, font)} •", data=f"setfonttime:{page}:{font}"), Button.inline(("✔️|Active" if str(last) == str(font) else "✖️|DeActive"), data=f"setfonttime:{page}:{font}")])
    pgbts = get_pages_button(page)
    buttons.append(pgbts)
    return buttons

def get_edit_buttons(page):
    last = client.DB.get_key("EDIT_MODE") or False
    buttons = []
    EDITS = ["Bold", "Mono", "Italic", "Underline", "Strike", "Spoiler", "Hashtag"]
    for edit in EDITS:
        buttons.append([Button.inline(f"• {edit} •", data=f"seteditmode:{page}:{edit}"), Button.inline(("✔️|Active" if str(last) == str(edit) else "✖️|DeActive"), data=f"seteditmode:{page}:{edit}")])
    pgbts = get_pages_button(page)
    buttons.append(pgbts)
    return buttons

@client.Cmd(pattern=f"(?i)^\{client.cmd}Panel$")
async def addecho(event):
    await event.edit(f"**{client.str} Processing . . .**")
    res = await client.inline_query(client.bot.me.username, "selfmainpanel")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Inline(pattern="selfmainpanel")
async def inlinepanel(event):
    text = f"**{client.str} Please Use The Buttons Below To Control The Different Parts:**\n\n"
    buttons = get_mode_buttons(1)
    await event.answer([event.builder.article(f"{client.str} Smart Self - Panel", text=text, buttons=buttons)])

@client.Callback(data="panelpage\:(.*)")
async def panelpages(event):
    page = int(event.data_match.group(1).decode('utf-8'))
    if page == 1:
        text = f"**{client.str} Please Use The Buttons Below To Control The Different Parts:**\n\n"
        buttons = get_mode_buttons(page)
        await event.edit(text=text, buttons=buttons)
    elif page == 2:
        text = f"**{client.str} Please Use The Options Below To Select The Font You Want To Use In Time Name And Bio:**"
        buttons = get_time_buttons(page)
        await event.edit(text=text, buttons=buttons)
    elif page == 3:
        text = f"**{client.str} Please Use The Options Below To Manage Edit Texts Mode:**"
        buttons = get_edit_buttons(page)
        await event.edit(text=text, buttons=buttons)

@client.Callback(data="setmode\:(.*)\:(.*)\:(.*)")
async def setmode(event):
    page = int(event.data_match.group(1).decode('utf-8'))
    mode = event.data_match.group(2).decode('utf-8')
    change = event.data_match.group(3).decode('utf-8')
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
    last = client.DB.get_key("EDIT_MODE") or False
    if str(last) == str(edit):
        client.DB.set_key("EDIT_MODE", False)
    else:
        client.DB.set_key("EDIT_MODE", str(edit))
    buttons = get_edit_buttons(page)
    await event.edit(buttons=buttons)

@client.Callback(data="closepanel")
async def closepanel(event):
    await event.edit(text=f"**{client.str} The Panel Successfuly Closed!**")
