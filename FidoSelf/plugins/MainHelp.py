from FidoSelf import client
from telethon import Button
from googletrans import Translator
import math

def translate(text):
    if client.lang == "en":
        return text
    translator = Translator()
    trjome = translator.translate(text, dest=client.lang)
    return trjome.text

def get_help_buttons():
    buttons = []
    CATS = client.get_string("Categorys")
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

def get_cmds_count(cat=None):
    plugins = client.HELP if not cat else get_plugins(cat)
    count = 0
    for plugin in plugins:
        for command in client.HELP[plugin]["commands"]:
            for com in client.HELP[plugin]["commands"][command]:
                count += 1
    return count

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
        emoji = client.DB.get_key("HELP_EMOJI") or "•"
        name = emoji + " " + plugin + " " + emoji
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
    CATS = client.get_string("Categorys")
    text = client.get_string("Help_1").format(len(CATS), get_cmds_count())
    buttons = get_help_buttons()
    await event.answer([event.builder.article(f"{client.str} FidoSelf - Help", text=text, buttons=buttons)])

@client.Callback(data="gethelp\:(.*)\:(.*)")
async def gethelp(event):
    await event.edit(client.get_string("Wait"))
    cat = str(event.data_match.group(1).decode('utf-8'))
    page = int(event.data_match.group(2).decode('utf-8'))
    buttons = get_cat_buttons(cat, page)
    text = client.get_string("Help_2").format(get_cmds_count(cat))
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="gethelpplugin\:(.*)\:(.*)")
async def getplugin(event):
    plugin = str(event.data_match.group(1).decode('utf-8'))
    page = int(event.data_match.group(2).decode('utf-8'))
    text = client.get_string("Help_3").format(plugin)
    CATS = client.get_string("Categorys")
    info = client.HELP[plugin]
    text += client.get_string("Help_4").format(CATS[info["category"]])
    text += client.get_string("Help_5").format(translate(info["note"]))
    for command in info["commands"]:
        text += f'  \n**{client.str} {command}:**\n'
        for com in info["commands"][command]:
            ncom = com.replace("{CMD}", client.cmd)
            cominfo = translate(info["commands"][command][com])
            text += f'    `{ncom}` - __{cominfo}__\n'
    buttons = [[Button.inline(client.get_string("InQuicks_Back"), data=f'gethelp:{info["category"]}:{page}')]] 
    await event.edit(text=text, buttons=buttons) 

@client.Callback(data="closehelp")
async def closehelp(event):
    text = client.get_string("Help_6")
    await event.edit(text=text)
