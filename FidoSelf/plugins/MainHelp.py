from FidoSelf import client
from telethon import Button
import math

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
    #CATS = client.get_string("Cats")
    for cat in CATS:
        buttons.append(Button.inline(f"• {CATS[cat]} •", data=f"gethelp:{cat}:1"))
    buttons = list(client.utils.chunks(buttons, 2))
    buttons.append([Button.inline(client.get_string("Inline_3"), data="closehelp")])
    buttons = client.get_buttons(buttons)
    return buttons

def get_plugins(cat):
    plugins = {}
    for plugin in client.HELP:
        if client.HELP[plugin]["category"] == cat:
            plugins.update({plugin: client.HELP[plugin]})
    return plugins

def get_pages_button(cat, page):
    buttons = []
    plugins = get_plugins(cat)
    pcount = math.ceil(len(plugins) / 10)
    start = (page - 1) * 10
    end = start + 10
    if end < len(plugins):
        buttons.append(Button.inline(client.get_string("Inline_4"), data=f"gethelp:{cat}:{page+1}"))
    if page > 1:
        buttons.append(Button.inline(client.get_string("Inline_5"), data=f"gethelp:{cat}:{page-1}"))
    buttons.append(Button.inline(client.get_string("Inline_3"), data="closehelp"))
    return buttons

def get_cat_buttons(cat, page):
    buttons = []
    plugins = get_plugins(cat)
    start = (page - 1) * 10
    end = start + 10
    if end > len(plugins):
        end = len(plugins)
    for plugin in plugins:
        name = "• " + plugin + " •"
        buttons.append(Button.inline(name, data=f"gethelpplugin:{plugin}:{page}"))
        if len(buttons) == end: break
    buttons = list(client.utils.chunks(buttons, 2))
    pgbts = get_pages_button(cat, page)
    buttons.append(pgbts)
    buttons = client.get_buttons(buttons)
    return buttons

@client.Cmd(pattern=f"(?i)^\{client.cmd}Help$")
async def help(event):
    await event.edit(client.get_string("Wait"))
    res = await client.inline_query(client.bot.me.username, "selfmainhelp")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="selfmainhelp")
async def inlinehelp(event):
    text = "Ok"
    buttons = get_help_buttons()
    await event.answer([event.builder.article(f"{client.str} FidoSelf - Help", text=text, buttons=buttons)])

@client.Callback(data="gethelp\:(.*)\:(.*)")
async def gethelp(event):
    cat = str(event.data_match.group(1).decode('utf-8'))
    page = int(event.data_match.group(2).decode('utf-8'))
    #text = client.get_string("Help_2").format(CATS[cat])
    buttons = get_cat_buttons(cat, page)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="gethelpplugin\:(.*)\:(.*)")
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
            text += f'    `{ncom}` - **{info["commands"][command][com]}\n'
    #buttons = get_plugin_buttons(page) 
    await event.edit(text=text) 

@client.Callback(data="closehelp")
async def closehelp(event):
    text = "Closed!"
    await event.edit(text=text)
