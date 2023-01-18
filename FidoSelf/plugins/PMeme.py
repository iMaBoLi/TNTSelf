from FidoSelf import client
from telethon import Button
import os

@client.Command(pattern=f"(?i)^\{client.cmd}Pmeme (.*)$")
async def persianmeme(event):
    await event.edit(client.get_string("Wait"))
    query = event.pattern_match.group(1)
    res = await client.inline_query(client.bot.me.username, f"pmeme:{query}")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="pmeme\:(.*)")
async def inlinememe(event):
    query = str(event.pattern_match.group(1))
    results = await client.inline_query("Persian_Meme_Bot", query)
    if not results:
        text = client.get_string("PMeme_1").format(query)
        return await event.answer([event.builder.article(f"{client.str} FidoSelf - PMeme Empty", text=text)])
    text = client.get_string("PMeme_2").format(query)
    buttons = []
    con = 0
    for result in results[:20]:
        title = result.title
        type = "🎞️" if result.type == "video" else "🎤"
        buttons.append([Button.inline(f"{type} {title}", data=f"getpmeme:{query}:{con}")])
        con += 1
    await event.answer([event.builder.article(f"{client.str} FidoSelf - PMeme", text=text, buttons=buttons)])

@client.Callback(data="getpmeme\:(.*)\:(.*)")
async def getpmeme(event):
    query = str(event.data_match.group(1).decode('utf-8'))
    count = int(event.data_match.group(2).decode('utf-8'))
    results = await client.inline_query("Persian_Meme_Bot", query)
    result = results[count]
    caption = client.get_string("PMeme_3").format(result.title, result.type)
    if result.type == "video":
        file = await result.download_media()
        await client.send_file(event.chat_id, file, caption=caption)  
    elif result.type == "voice":
        file = await result.download_media()
        await client.send_file(event.chat_id, file, caption=caption, voice_note=True)  
    os.remove(file)
