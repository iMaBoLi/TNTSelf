from FidoSelf import client
from telethon import types, Button
import os

STRINGS = {
    "linkinv": "**The Entered Youtube Link Is Invalid!**",
    "downingvid": "**Downloadig Video** ( `{}` ) **...**",
    "downingaud": "**Downloadig Audio** ( `{}` ) **...**",
    "caption": "**Title:** ( `{}` )\n**Uploader:** ( `{}` )\n**Views:** ( `{}` )\n**Duration:** ( `{}` )\n**Description:** ( `{}` )",
    "ytclick": "**Click To Follow Button To Get Search Results For Query:** ( `{}` )",
    "ytsearch": "**Click To Follow Button To Get Search Results For Query:** ( `{}` )",
}

@client.Command(command="Yt(Video|Music) (.*)")
async def ytdownload(event):
    await event.edit(client.STRINGS["wait"])
    type = event.pattern_match.group(1).lower()
    link = event.pattern_match.group(2)
    if not client.functions.YOUTUBE_REGEX.search(link):
        return await event.edit(client.STRINGS["linkinv"])
    ytinfo = client.functions.yt_info(link)
    if type == "video":
        await event.edit(STRINGS["downingvid"].format(ytinfo["title"]))
        info = await client.functions.yt_downloader(link, type, "720")
        duration = int(ytinfo["duration"])
        attributes = [types.DocumentAttributeVideo(duration=duration, w=720, h=720, supports_streaming=True)]
    else:
        await event.edit(STRINGS["downingaud"].format(ytinfo["title"]))
        info = await client.functions.yt_downloader(link, type, "320k")
        duration = int(ytinfo["duration"])
        title = ytinfo["title"]
        performer = ytinfo["uploader"]
        attributes = [types.DocumentAttributeAudio(duration=duration, title=title, performer=performer)]
    description = str(ytinfo["description"])[:100]
    caption = STRINGS["caption"].format(ytinfo["title"], ytinfo["uploader"], ytinfo["view_count"], ytinfo["duration_string"], description)
    callback = event.progress(upload=True)
    await client.send_file(
        event.chat_id,
        file=info["OUTFILE"],
        thumb=info["THUMBNAIL"],
        attributes=attributes,
        caption=caption,
        progress_callback=callback,
    )
    os.remove(info["OUTFILE"])
    os.remove(info["THUMBNAIL"])
    await event.delete()
    
@client.Command(command="YtSearch (.*)")
async def ytsearch(event):
    await event.edit(client.STRINGS["wait"])
    query = event.pattern_match.group(1)
    query = query[:15]
    res = await client.inline_query(client.bot.me.username, f"ytclick:{query}")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="ytclick\:(.*)")
async def ytsearchclick(event):
    query = event.pattern_match.group(1)
    text = STRINGS["ytclick"].format(query)
    buttons = [[Button.switch_inline("• Click!", "ytsearch:" + str(query), same_peer=True)]]
    await event.answer([event.builder.article("FidoSelf - YtClick", text=text, buttons=buttons)])

@client.Inline(pattern="ytsearch\:(.*)")
async def ytsearch(event):
    query = event.pattern_match.group(1)
    answers = []
    searchs = client.functions.yt_search(query, limit=10)
    for search in searchs:
        link = search["link"]
        title = search["title"]
        description = search["title"]
        text = STRINGS["ytsearch"].format(title)
        vidurl = f"http://t.me/share/text?text=.ytvideo+{link}"
        audurl = f"http://t.me/share/text?text=.ytmusic+{link}"
        buttons = [[Button.url("• Download Video •", url=vidurl), Button.url("• Download Audio •", url=audurl)]]
        thumblink = search["thumbnails"][-1]["url"]
        thumb = types.InputWebDocument(thumblink, 0, "image/jpg", [])
        answer = event.builder.article(
            title=title,
            description=description,
            text=text,
            buttons=buttons,
            thumb=photo,
        )
        #answer = event.builder.document(photo, title=title, description=description, text=text, buttons=buttons)
        answers.append(answer)
    await event.answer(answers)
