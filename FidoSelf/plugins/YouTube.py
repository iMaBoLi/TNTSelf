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
    "downvideo": "**{STR} Downloadig Video From Youtube ...**\n\n**{STR} Link:** ( `{}` )",
    "downaudio": "**{STR} Downloadig Audio From Youtube ...**\n\n**{STR} Link:** ( `{}` )",
    "caption": "**{STR} Title:** ( `{}` )\n**{STR} Uploader:** ( `{}` )\n**{STR} Views:** ( `{}` )\n**{STR} Duration:** ( `{}` )\n**{STR} Description:** ( `{}` )",
    "description": "**{STR} Description:** ( `{}` )",
    "ytclick": "**{STR} Click To Follow Button To Get Search Results For Query:** ( `{}` )",
    "ytsearch": "**{STR} Link:** ( {} )\n**{STR} Title:** ( `{}` )\n**{STR} Uploader:** ( `{}` )\n**{STR} Views:** ( `{}` )\n**{STR} Size:** ( `{}` )\n**{STR} Duration:** ( `{}` )",
}
    
@client.Command(command="Yt(Video|Audio) (.*)")
async def ytdownloader(event):
    await event.edit(client.STRINGS["wait"])
    downtype = event.pattern_match.group(1).title()
    link = event.pattern_match.group(2)
    if not client.functions.YOUTUBE_REGEX.search(link):
        return await event.edit(client.getstrings(STRINGS)["linkinv"].format(link))
    if downtype == "Video":
        await event.edit(client.getstrings(STRINGS)["downvideo"].format(link))
        file, ytinfo = await client.functions.yt_video(link)
        attributes = [types.DocumentAttributeVideo(duration=ytinfo["duration"], w=720, h=720, supports_streaming=True)]
    if downtype == "Audio":
        await event.edit(client.getstrings(STRINGS)["downaudio"].format(link))
        file, ytinfo = await client.functions.yt_audio(link)
        attributes = [types.DocumentAttributeAudio(duration=ytinfo["duration"], voice=False, title=ytinfo["title"], performer=ytinfo["uploader"])]
    filesize = convert_bytes(os.path.getsize(file["OUTFILE"]))
    caption = client.getstrings(STRINGS)["caption"].format(ytinfo["title"], ytinfo["uploader"], ytinfo["view_count"], filesize, ytinfo["duration_string"])
    callback = client.progress(event, upload=True)
    uploadfile = await client.fast_upload(file["OUTFILE"], progress_callback=callback)
    await client.send_file(event.chat_id, file=uploadfile, thumb=file["THUMBNAIL"], attributes=attributes, caption=caption)
    description = ytinfo["description"]
    if len(description) < 3900:
        description = client.getstrings(STRINGS)["description"].format(description)
        await send.reply(description)
    os.remove(file["OUTFILE"])
    os.remove(file["THUMBNAIL"])
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