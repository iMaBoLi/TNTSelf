from FidoSelf import client
from telethon import Button
from datetime import datetime
from FidoSelf.plugins.ManageTime import FONTS, create_font

@client.Cmd(pattern=f"(?i)^\{client.cmd}Panel$")
async def addecho(event):
    await event.edit(f"**{client.str} Processing . . .**")
    res = await client.inline_query(client.bot.me.username, "selfmainpanel")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Inline(pattern="selfmainpanel")
async def panel(event):
    buttons = []
    text = f"**{client.str} Please Choose Modes:**\n\n"
    buttons.append(Button.inline("◀️ Back", data=f"panelpage:5"))
    buttons.append(Button.inline("Next ▶️", data=f"panelpage:2"))
    buttons.append(Button.inline("🚫 Close 🚫", data="closepanel"))
    buttons = list(client.utils.chunks(buttons, 2))
    await event.answer([event.builder.article(f"{client.str} Smart Self - Panel", text=text, buttons=buttons)])

@client.Callback(data="panelpage\:(.*)")
async def pages(event):
    page = int(event.data_match.group(1).decode('utf-8'))
    buttons = []
    if page == 1:
        text = f"**{client.str} Please Choose Modes:**"
    elif page == 2:
        text = f"**{client.str} Please Choose Modes:**"
    elif page == 3:
        text = f"**{client.str} Please Choose Modes:**"
    elif page == 4:
        text = f"**{client.str} Please Edit Chat Actions To Be Set:**"
    elif page == 5:
        text = f"**{client.str} Please Use The Options Below To Select The Font You Want To Use In Time Name And Bio:**"
        newtime = datetime.now().strftime("%H:%M")
        last = client.DB.get_key("TIME_FONT")
        buttons.append(Button.inline("• Random •", data="setfonttime:random"))
        buttons.append(Button.inline(("✔️|Active" if last == "random" else "✖️|DeActive"), data="setfonttime:random"))
        buttons.append(Button.inline("• Random2 •", data="setfonttime:random2"))
        buttons.append(Button.inline(("✔️|Active" if last == "random2" else "✖️|DeActive"), data="setfonttime:random2"))
        for font in FONTS:
            buttons.append(Button.inline(f"• {create_font(newtime, font)} •", data=f"setfonttime:{font}"))
            buttons.append(Button.inline(("✔️|Active" if font == last else "✖️|DeActive"), data=f"setfonttime:{font}"))
    back = (page - 1) if page != 1 else 5
    next = (page + 1) if page != 5 else 1
    buttons.append(Button.inline("◀️ Back", data=f"panelpage:{back}"))
    buttons.append(Button.inline("Next ▶️", data=f"panelpage:{next}"))
    buttons.append(Button.inline("🚫 Close 🚫", data="closepanel"))
    buttons = list(client.utils.chunks(buttons, 2))
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="setfonttime\:(.*)")
async def setfonttime(event):
    font = event.data_match.group(1).decode('utf-8')
    client.DB.set_key("TIME_FONT", font)
    newtime = datetime.now().strftime("%H:%M")
    last = client.DB.get_key("TIME_FONT")
    buttons = []
    buttons.append(Button.inline("• Random •", data="setfonttime:random"))
    buttons.append(Button.inline(("✔️|Active" if last == "random" else "✖️|DeActive"), data="setfonttime:random"))
    for font in FONTS:
        buttons.append(Button.inline(f"• {create_font(newtime, font)} •", data=f"setfonttime:{font}"))
        buttons.append(Button.inline(("✔️|Active" if font == last else "✖️|DeActive"), data=f"setfonttime:{font}"))
    buttons.append(Button.inline("◀️ Back", data="panelpage:4"))
    buttons.append(Button.inline("Next ▶️", data="panelpage:1"))
    buttons.append(Button.inline("🚫 Close 🚫", data="closepanel"))
    buttons = list(client.utils.chunks(buttons, 2))
    await event.edit(buttons=buttons)

@client.Callback(data="closepanel")
async def closepanel(event):
    await event.edit(text=f"**{client.str} The Panel Successfuly Closed!**")
