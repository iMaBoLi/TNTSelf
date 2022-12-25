from FidoSelf import client
from youtubesearchpython import VideosSearch
from telethon.tl.types import InputWebDocument as wb

@client.Inline(pattern="yt\:(.*)")
async def ytsearch(event):
    string = str(event.pattern_match.group(1))
    results = []
    search = VideosSearch(string, limit=50)
    nub = search.result()
    nibba = nub["result"]
    for v in nibba:
        ids = v["id"]
        link = ids
        title = v["title"]
        duration = v["duration"]
        views = v["viewCount"]["short"]
        publisher = v["channel"]["name"]
        published_on = v["publishedTime"]
        description = (
            v["descriptionSnippet"][0]["text"]
            if v.get("descriptionSnippet")
            and len(v["descriptionSnippet"][0]["text"]) < 500
            else "None"
        )
        thumb = f"https://i.ytimg.com/vi/{ids}/hqdefault.jpg"
        text = f"**Title: [{title}]({link})**\n\n"
        text += f"`Description: {description}\n\n"
        text += f"「 Duration: {duration} 」\n"
        text += f"「 Views: {views} 」\n"
        text += f"「 Publisher: {publisher} 」\n"
        text += f"「 Published on: {published_on} 」`"
        desc = f"{title}\n{duration}"
        file = wb(thumb, 0, "image/jpeg", [])
        results.append(
            await event.builder.article(
                type="photo",
                title=title,
                description=desc,
                thumb=file,
                content=file,
                text=text,
                include_media=True,
            ),
        )
    await event.answer(results[:50])
