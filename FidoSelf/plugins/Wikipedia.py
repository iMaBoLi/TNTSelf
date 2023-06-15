from FidoSelf import client
from telethon import Button
import wikipedia

__INFO__ = {
    "Category": "Practical",
    "Plugname": "Wikipedia",
    "Pluginfo": {
        "Help": "To Search A Note On Wikipedia!",
        "Commands": {
            "{CMD}SWiki <Text>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "not": "**No Results Found For Query:** ( `{}` ) **In Wikipedia!**",
    "result": "**The Wikipedia Results For Query:** ( `{}` )",
    "info": "**Title:** ( `{}` )\n\n`{}`",
}

@client.Command(command="SWiki (.*)")
async def wikisearch(event):
    await event.edit(client.STRINGS["wait"])
    query = event.pattern_match.group(1)
    res = await client.inline_query(client.bot.me.username, f"wikipedia:{query}")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="wikipedia\:(.*)")
async def inlinewiki(event):
    query = str(event.pattern_match.group(1))
    results = wikipedia.search(query)
    if not results:
        text = STRINGS["not"].format(query)
        return await event.answer([event.builder.article("FidoSelf - Wiki Empty", text=text)])
    text = STRINGS["result"].format(query)
    buttons = []
    con = 0
    for result in results[:10]:
        buttons.append(Button.inline(f"• {result} •", data=f"getwikipedia:{query}:{con}"))
        con += 1
    buttons = list(client.functions.chunks(buttons, 2))
    await event.answer([event.builder.article("FidoSelf - Wikipedia", text=text, buttons=buttons)])

@client.Callback(data="getwikipedia\:(.*)\:(.*)")
async def getwikipedia(event):
    query = str(event.data_match.group(1).decode('utf-8'))
    count = int(event.data_match.group(2).decode('utf-8'))
    search = wikipedia.search(query)[count]
    result = wikipedia.summary(search)
    if len(result) > 3000:
        result = result[:3000]
    text = STRINGS["info"].format(search, result)
    await event.edit(text=text)