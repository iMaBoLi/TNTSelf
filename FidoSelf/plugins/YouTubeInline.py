from FidoSelf import client
from youtubesearchpython import VideosSearch

@client.Inline(pattern="yt\:(.*)")
async def ytsearch(event):
    string = str(event.pattern_match.group(1))
    results = []
    searchs = VideosSearch(string, limit=10).result()["result"]
    for vid in searchs:
        link = vid["link"]
        title = vid["title"]
        ids = vid["id"]
        duration = vid["duration"]
        thumb = f"https://img.youtube.com/vi/{ids}/hqdefault.jpg"
        text = f"**{client.str} Title:** ( `{title}`)\n\n**• [Link]({link}) •**\n\n**{client.str} Duration:** (`{duration}` )"
        desc = f"Title : {title}\nDuration : {duration}"
        results.append(
            event.builder.document(
                file=thumb,
                title=title,
                description=desc,
                text=text,
                include_media=True,
            ),
        )
    await event.answer(results)
