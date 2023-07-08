from FidoSelf import client
from telethon import types, Button
import os

__INFO__ = {
    "Category": "Usage",
    "Name": "Youtube",
    "Info": {
        "Help": "To Download From Youtube And Search On Youtube!",
        "Commands": {
            "{CMD}YtDown <Link>": None,
            "{CMD}YtSearch <Text>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "linkinv": "**The Entered Youtube Link Is Invalid!**",
    "downingvid": "**Downloadig Video** ( `{}` ) **...**",
    "downingaud": "**Downloadig Audio** ( `{}` ) **...**",
    "ytdown": "**Title:** ( `{}` )\n**Uploader:** ( `{}` )\n**Views:** ( `{}` )\n**Duration:** ( `{}` )\n**Description:** ( `{}` )",
    "ytclick": "**Click To Follow Button To Get Search Results For Query:** ( `{}` )",
    "ytsearch": "**Link:** ( {} )\n**Title:** ( `{}` )\n**Uploader:** ( `{}` )\n**Views:** ( `{}` )\n**Duration:** ( `{}` )\n**Description:** ( `{}` )",
    "com": "**The Download And Upload Completed!**",
}
    
@client.Command(command="YtDown (.*)")
async def ytdown(event):
    await event.edit(client.STRINGS["wait"])
    link = event.pattern_match.group(1)
    if not client.functions.YOUTUBE_REGEX.search(link):
        return await event.edit(client.getstrings(STRINGS)["linkinv"])
    videoid = client.functions.get_videoid(link)
    chatid = event.chat_id
    res = await client.inline_query(client.bot.me.username, f"ytdown:{chatid}:{videoid}")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="ytdown\:(.*)\:(.*)")
async def ytdowninline(event):
    chatid = event.pattern_match.group(1)
    videoid = event.pattern_match.group(2)
    link = client.functions.YOUTUBE_URL + videoid
    ytinfo = client.functions.yt_info(link)
    description = str(ytinfo["description"])[:50]
    text = client.getstrings(STRINGS)["ytdown"].format(ytinfo["title"], ytinfo["uploader"], ytinfo["view_count"], ytinfo["duration_string"], description)
    videos, audios = client.functions.get_formats(link)
    vidbuttons = []
    for video in videos:
        vid = videos[video]
        size = client.functions.convert_bytes(vid["filesize"])
        name = "🎬 " + vid["format"] + " - " + size
        vidext = vid["ext"]
        vidbuttons.append(Button.inline(name, data=f"ytdownload:{chatid}:{videoid}:{video}:{vidext}"))
    vidbuttons = list(client.functions.chunks(vidbuttons, 2))
    audbuttons = []
    for audio in audios:
        aud = audios[audio]
        size = client.functions.convert_bytes(aud["filesize"])
        name = "🎤 " + aud["format"] + " - " + size
        audext = aud["ext"]
        audbuttons.append(Button.inline(name, data=f"ytdownload:{chatid}:{videoid}:{audio}:{audext}"))
    audbuttons = list(client.functions.chunks(audbuttons, 2))
    buttons = vidbuttons + audbuttons
    await event.answer([event.builder.article("FidoSelf - YouTube Downloader", text=text, buttons=buttons)])

@client.Callback(data="ytdownload\:(.*)\:(.*)\:(.*)\:(.*)")
async def ytdownload(event):
    chatid = event.data_match.group(1).decode('utf-8')
    videoid = event.data_match.group(2).decode('utf-8')
    format = event.data_match.group(3).decode('utf-8')
    ext = event.data_match.group(4).decode('utf-8')
    link = client.functions.YOUTUBE_URL + videoid
    ytinfo = client.functions.yt_info(link)
    if ext == "mp4":
        await event.edit(client.getstrings(STRINGS)["downingvid"].format(ytinfo["title"]))
        duration = int(ytinfo["duration"])
        attributes = [types.DocumentAttributeVideo(duration=duration, w=720, h=720, supports_streaming=True)]
    elif ext == "mp3":
        await event.edit(client.getstrings(STRINGS)["downingaud"].format(ytinfo["title"]))
        duration = int(ytinfo["duration"])
        title = ytinfo["title"]
        performer = ytinfo["uploader"]
        attributes = [types.DocumentAttributeAudio(duration=duration, title=title, performer=performer)]
    down = await client.functions.yt_downloader(link, format, ext)
    description = str(ytinfo["description"])[:50]
    caption = client.getstrings(STRINGS)["ytdown"].format(ytinfo["title"], ytinfo["uploader"], ytinfo["view_count"], ytinfo["duration_string"], description)
    callback = client.progress(event, upload=True)
    await client.send_file(
        int(chatid),
        file=down["OUTFILE"],
        thumb=down["THUMBNAIL"],
        attributes=attributes,
        caption=caption,
        progress_callback=callback,
    )
    os.remove(down["OUTFILE"])
    os.remove(down["THUMBNAIL"])
    await event.edit(client.getstrings(STRINGS)["com"])
    
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
    text = client.getstrings(STRINGS)["ytclick"].format(query)
    buttons = [[Button.switch_inline("• Click !", "ytsearch:" + str(query), same_peer=True)]]
    await event.answer([event.builder.article("FidoSelf - YtClick", text=text, buttons=buttons)])

@client.Inline(pattern="ytsearch\:(.*)")
async def ytsearchinline(event):
    query = event.pattern_match.group(1)
    answers = []
    searchs = client.functions.yt_search(query, limit=20)
    for search in searchs:
        link = search["link"]
        description = str(search["descriptionSnippet"][0]["text"])[:100] if search["descriptionSnippet"] else "---"
        text = client.getstrings(STRINGS)["ytsearch"].format(link, search["title"], search["channel"]["name"], search["viewCount"]["text"], search["duration"], description)
        url = f"http://t.me/share/text?text=.ytdown+{link}"
        buttons = [[Button.url("• Download •", url=url)]]
        thumblink = search["thumbnails"][-1]["url"]
        thumb = types.InputWebDocument(thumblink, 0, "image/jpg", [])
        answer = event.builder.article(
            title=search["title"],
            description=search["viewCount"]["text"],
            text=text,
            buttons=buttons,
            thumb=thumb,
        )
        answers.append(answer)
    await event.answer(answers)