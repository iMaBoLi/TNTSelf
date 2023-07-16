from FidoSelf import client
from youtubesearchpython import VideosSearch
from PIL import Image
import random
import re
import os

YOUTUBE_REGEX = re.compile(r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})")
YOUTUBEPL_REGEX = re.compile(r"(?:youtube\.com|youtu\.be)/playlist/(?:[\w-]+\?list=|list/)?([\w-])")

MAIN = "yt-dlp -o '{outfile}' -f {format} {link}"
THUMB = "yt-dlp -o '{outfile}' --write-thumbnail --skip-download {link}"

def yt_info(link):
    from yt_dlp import YoutubeDL
    info = YoutubeDL().extract_info(link, download=False)
    return info

def get_videoid(url):
    match = YOUTUBE_REGEX.search(url)
    return match.group(1)

async def yt_video(link):
    from yt_dlp import YoutubeDL
    filename = get_videoid(link) + str(random.randint(11111, 99999))
    outfile = client.PATH + "youtube/" + filename + ".mp4" 
    OPTS = {
        "progress_hooks": lambda res: client.LOGS.error(res),
        "format": "best(video+audio)",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
            {"key": "FFmpegMetadata"},
        ],
        "outtmpl": outfile,
        "logtostderr": False,
        "quiet": True,
    }
    with YoutubeDL(OPTS) as ytdl:
        ytinfo = ytdl.extract_info(link, download=True)
    info = {}
    info["OUTFILE"] = outfile
    info["THUMBNAIL"] = await yt_thumb(link)
    return info, ytinfo

async def yt_audio(link):
    from yt_dlp import YoutubeDL
    filename = get_videoid(link) + str(random.randint(11111, 99999))
    outfile = client.PATH + "youtube/" + filename
    OPTS = {
        "outtmpl": outfile,
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "format": "bestaudio/best",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            },
            {"key": "EmbedThumbnail"},
            {"key": "FFmpegMetadata"},
        ],
        "quiet": True,
    }
    with YoutubeDL(OPTS) as ytdl:
        ytinfo = ytdl.extract_info(link, download=True)
    info = {}
    info["OUTFILE"] = outfile + ".mp3"
    info["THUMBNAIL"] = await yt_thumb(link)
    return info, ytinfo

async def yt_thumb(link):
    filename = get_videoid(link) + str(random.randint(11111, 99999))
    thumb = client.PATH + "youtube/" + filename
    cmd = THUMB.format(outfile=thumb, link=link)
    await client.functions.runcmd(cmd)
    thumb = convert_thumb(thumb + ".webp")
    return thumb

def convert_thumb(file):
    thumb = file + ".jpg"
    try:
        img = Image.open(file)
        img.save(thumb, format="jpeg")
        os.remove(file)
    except:
        os.rename(file, thumb)
    return thumb
    
def yt_search(query, limit=50):
    results = VideosSearch(query, limit=limit)
    return results.result()["result"]