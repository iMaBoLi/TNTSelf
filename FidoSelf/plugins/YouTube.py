from FidoSelf import client
from telethon import types, Button
import os

STRINGS = {
    "linkinv": "**The Entered Youtube Link Is Invalid!**",
    "downingvid": "**Downloadig Video** ( `{}` ) **...**",
    "downingaud": "**Downloadig Audio** ( `{}` ) **...**",
    "caption": "**Title:** ( `{}` )\n**Uploader:** ( `{}` )\n**Views:** ( `{}` )\n**Duration:** ( `{}` )\n**Description:** ( `{}` )",
    "ytclick": "**Click To Follow Button To Get Search Results For Query:** ( `{}` )",
}

@client.Command(command="Yt(Video|Music) (.*) ?(.*)?")
async def ytdownload(event):
    await event.edit(client.STRINGS["wait"])
    type = event.pattern_match.group(1).lower()
    link = event.pattern_match.group(2)
    quality = event.pattern_match.group(3)
    if not client.functions.YOUTUBE_REGEX.search(link):
        return await event.edit(client.STRINGS["linkinv"])
    ytinfo = client.functions.yt_info(link)
    if type == "video":
        await event.edit(STRINGS["downingvid"].format(ytinfo["title"]))
        info = await client.functions.yt_downloader(link, type, (quality or "720"))
        duration = int(ytinfo["duration"])
        attributes = [types.DocumentAttributeVideo(duration=duration, w=720, h=720, supports_streaming=True)]
    else:
        await event.edit(STRINGS["downingaud"].format(ytinfo["title"]))
        info = await client.functions.yt_downloader(link, type, (quality or "720"))
        duration = int(ytinfo["duration"])
        title = ytinfo["title"]
        performer = ytinfo["uploader"]
        attributes = [types.DocumentAttributeAudio(duration=duration, title=title, performer=performer)]
    description = str(ytinfo["description"])[:100] + " ..."
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
    
@client.Command(command="YtDown (.*)")
async def ytdown(event):
    await event.edit(client.STRINGS["wait"])
    link = event.pattern_match.group(1)
    if not client.functions.YOUTUBE_REGEX.search(link):
        return await event.edit(client.STRINGS["linkinv"])
    videoid = client.functions.get_videoid(link)
    res = await client.inline_query(client.bot.me.username, f"ytdown:{videoid}")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="ytdown\:(.*)")
async def ytdowninline(event):
    videoid = event.pattern_match.group(1)
    link = client.functions.YOUTUBE_URL + videoid
    videos, audios = client.functions.get_formats(link)
    vidbuttons = []
    for video in videos:
        vid = videos[video]
        size = client.functions.convert_bytes(int(vid["filesize"])) if vid["filesize"] != "---" else vid["filesize"]
        name = vid["format"] + " - " + size
        buttons.append(Button.inline(name, data=f"ytdownload:{videoid}:{video}"))
    vidbuttons = list(client.functions.chunks(vidbuttons, 2))
    audbuttons = []
    for audio in audios:
        aud = audios[audio]
        size = client.functions.convert_bytes(int(aud["filesize"])) if aud["filesize"] != "---" else aud["filesize"]
        name = aud["format"] + " - " + size
        buttons.append(Button.inline(name, data=f"ytdownload:{videoid}:{video}"))
    audbuttons = list(client.functions.chunks(audbuttons, 2))
    buttons = vidbuttons + audbuttons
    await event.answer([event.builder.article("FidoSelf - YtSearch", text=link, buttons=buttons)])

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
        description = str(search["descriptionSnippet"][0]["text"])[:100] + " ..."
        text = STRINGS["caption"].format(search["title"], search["channel"]["name"], search["viewCount"]["text"], search["duration"], description)
        vidurl = f"http://t.me/share/text?text=.ytvideo+{link}"
        audurl = f"http://t.me/share/text?text=.ytmusic+{link}"
        buttons = [[Button.url("• Download Video •", url=vidurl), Button.url("• Download Audio •", url=audurl)]]
        thumblink = search["thumbnails"][-1]["url"]
        thumb = types.InputWebDocument(thumblink, 0, "image/jpg", [])
        answer = event.builder.article(
            title=search["title"],
            description=search["viewCount"]["text"],
            text=text,
            buttons=buttons,
            thumb=thumb,
            content=thumb,
        )
        answers.append(answer)
    await event.answer(answers)
