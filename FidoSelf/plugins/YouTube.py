from FidoSelf import client
from telethon import types, Button
import os

__INFO__ = {
    "Category": "Usage",
    "Name": "Youtube",
    "Info": {
        "Help": "To Download And Search On Youtube!",
        "Commands": {
            "{CMD}YtVideo <Link>": {
                "Help": "To Download Video",
                "Input": {
                    "<Link>": "Link Of Youtube",
                },
            },
            "{CMD}YtAudio <Link>": {
                "Help": "To Download Audio",
                "Input": {
                    "<Link>": "Link Of Youtube",
                },
            },
            "{CMD}YtSearch <Text>": {
                "Help": "To Search On Youtube",
                "Input": {
                    "<Text>": "Query For Search",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "linkinv": "**{STR} The Entered Youtube Link** ( `{}` ) **Is Invalid!**",
    "downvideo": "**{STR} Downloadig Video** ( `{}` ) **...**",
    "downaudio": "**{STR} Downloadig Audio** ( `{}` ) **...**",
    "caption": "**{STR} Title:** ( `{}` )\n**{STR} Uploader:** ( `{}` )\n**{STR} Views:** ( `{}` )\n**{STR} Duration:** ( `{}` )\n**{STR} Description:** ( `{}` )",
    "ytclick": "**{STR} Click To Follow Button To Get Search Results For Query:** ( `{}` )",
    "ytsearch": "**{STR} Link:** ( {} )\n**{STR} Title:** ( `{}` )\n**{STR} Uploader:** ( `{}` )\n**{STR} Views:** ( `{}` )\n**{STR} Duration:** ( `{}` )\n**{STR} Description:** ( `{}` )",
    "complete": "**{STR} The Download And Upload Completed!**"
}
    
@client.Command(command="YtVideo (.*)")
async def ytvideo(event):
    await event.edit(client.STRINGS["wait"])
    link = event.pattern_match.group(1)
    if not client.functions.YOUTUBE_REGEX.search(link):
        return await event.edit(client.getstrings(STRINGS)["linkinv"].format(link))
    ytinfo = client.functions.yt_info(link)
    await event.edit(client.getstrings(STRINGS)["downvideo"].format(ytinfo["title"]))
    video = await client.functions.yt_video(ytinfo)
    duration = int(ytinfo["duration"])
    attributes = [types.DocumentAttributeVideo(duration=duration, w=720, h=720, supports_streaming=True)]
    description = str(ytinfo["description"])[:50]
    caption = client.getstrings(STRINGS)["caption"].format(ytinfo["title"], ytinfo["uploader"], ytinfo["view_count"], ytinfo["duration_string"], description)
    callback = client.progress(event, upload=True)
    uploadfile = await client.fast_upload(video["OUTFILE"], progress_callback=callback)
    await client.send_file(
        int(chatid),
        file=uploadfile,
        thumb=video["THUMBNAIL"],
        attributes=attributes,
        caption=caption,
    )
    os.remove(video["OUTFILE"])
    os.remove(video["THUMBNAIL"])
    await event.edit(client.getstrings(STRINGS)["complete"])

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
    searchs = client.functions.yt_search(query, limit=50)
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