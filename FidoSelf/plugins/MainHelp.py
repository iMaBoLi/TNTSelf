from FidoSelf import client
from telethon import Button
from googletrans import Translator
import math

def translate(text, lang):
    translator = Translator()
    trjome = translator.translate(text, dest=lang.lower())
    return trjome.text

CATS = {
    "Settings": "Settings ⚙️",
    "Manager": "Manager 👮",
    "Tools": "Tools 🔧",
    "Account": "Account 💎",
    "Groups": "Groups 👥",
    "Time": "Time ⏰",
}

def get_help_buttons():
    buttons = []
    for cat in CATS:
        name = CATS[cat] if client.lang == "en" else translate(CATS[cat], client.lang)
        buttons.append(Button.inline(f"• {name} •", data=f"gethelp:{cat}:1"))
    buttons = list(client.utils.chunks(buttons, 2))
    buttons = client.get_buttons(buttons)
    return buttons

def get_cat_buttons(cat, page):
    buttons = []
    PLUGS = {}
    for plugin in client.HELP:
        if client.HELP[plugin]["category"] == cat:
            PLUGS.update({plugin: client.HELP[plugin]})
    pcount = math.ceil(len(PLUGS) / 10)
    start = (page - 1) * 10
    end = start + 10
    if end > len(PLUGS):
        end = len(PLUGS)
    for Plug in PLUGS:
        name = "•" + Plug + "•"
        buttons.append(Button.inline(f"• {name} •", data=f"getplugin:{Plug}:{page}"))
        if len(buttons) == end: break
    buttons = list(client.utils.chunks(buttons, 2))
    return buttons

@client.Cmd(pattern=f"(?i)^\{client.cmd}Help$")
async def help(event):
    await event.edit(client.get_string("Wait"))
    res = await client.inline_query(client.bot.me.username, "selfmainhelp")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="selfmainhelp")
async def inlinehelp(event):
    text = "Please Chose Your Page:"
    buttons = get_help_buttons()
    await event.answer([event.builder.article(f"{client.str} FidoSelf - Help", text=text, buttons=buttons)])

@client.Callback(data="gethelp\:(.*)\:(.*)")
async def gethelp(event):
    cat = str(event.data_match.group(1).decode('utf-8'))
    page = int(event.data_match.group(2).decode('utf-8'))
    buttons = get_cat_buttons(cat, page) 
    await event.edit(buttons=buttons)

@client.Callback(data="getplugin\:(.*)\:(.*)")
async def getplugin(event):
    plugin = str(event.data_match.group(1).decode('utf-8'))
    page = int(event.data_match.group(2).decode('utf-8'))
    text = f"**{client.str} Plugin Name:** ( `{plugin}` )\n"
    info = client.HELP[plugin]
    text += f'**{client.str} Category:** ( `{info["category"]}` )\n'
    text += f'**{client.str} Note:** ( `{info["note"]}` )\n'
    for command in info["commands"]:
        text += f'\n**{client.str} {command}:**\n'
        for com in info["commands"][command]:
            ncom = com.replace("{CMD}", client.cmd)
            text += f'    `{ncom} - **{info["commands"][command][com]}\n'
    #buttons = get_plugin_buttons(page) 
    await event.edit(text=text) 
