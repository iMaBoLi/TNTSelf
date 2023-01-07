from FidoSelf import client
from telethon import Button
import wikipedia

@client.Cmd(pattern=f"(?i)^\{client.cmd}SWiki (.*)$")
async def wikisearch(event):
    await event.edit(client.get_string("Wait"))
    wikipedia.set_lang("fa")
    query = event.pattern_match.group(1)
    res = await client.inline_query(client.bot.me.username, f"wikipedia:{query}")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="wikipedia\:(.*)")
async def inlinewiki(event):
    query = str(event.pattern_match.group(1))
    results = wikipedia.search(query)
    if not results:
        text = client.get_string("Wikipedia_1").format(query)
        return await event.answer([event.builder.article(f"{client.str} FidoSelf - Wiki Empty", text=text)])
    text = client.get_string("Wikipedia_2").format(query)
    buttons = []
    con = 0
    for result in results[:20]:
        buttons.append([Button.inline(f"• {result} •", data=f"getwikipedia:{query}:{con}")])
        con += 1
    buttons = list(client.utils.chunks(buttons, 2))
    await event.answer([event.builder.article(f"{client.str} FidoSelf - Wikipedia", text=text, buttons=buttons)])

@client.Callback(data="getwikipedia\:(.*)\(.*)")
async def getwikipedia(event):
    query = str(event.data_match.group(1).decode('utf-8'))
    count = int(event.data_match.group(2).decode('utf-8'))
    search = wikipedia.search(query)[count]
    result = wikipedia.summary(search)
    text = client.get_string("Wikipedia_3").format(query, result)
    await event.edit(text=text)
