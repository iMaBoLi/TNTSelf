from FidoSelf import client
from yt_dlp import YoutubeDL

@client.run_async
def del(url, opts):
    return YoutubeDL(opts).download([url])

@client.Cmd(pattern="\.dl (.*)")
async def ytdltest(event):
    await event.edit(".....!")
    OPTS = {
    "format": "bestaudio",
    "addmetadata": True,
    "key": "FFmpegMetadata",
    "prefer_ffmpeg": True,
    "geo_bypass": True,
    "outtmpl": f"%(id)s.mp3",
    "logtostderr": False,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "best",
        },
        {"key": "FFmpegMetadata"},
     ],
    }
    url = event.pattern_match.group(1)
    await del(url, OPTS)
    await event.edit("Ok!")
