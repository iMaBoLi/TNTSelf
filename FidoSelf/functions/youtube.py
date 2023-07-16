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

async def yt_video(event, link):
    from yt_dlp import YoutubeDL
    randnum = str(random.randint(11111, 99999))
    outfile = client.PATH + "youtube/" + f"{randnum} - %(id)s.%(ext)s"
    OPTS = {
        "progress_hooks": [lambda result: client.yt_progress(event, result)],
        "outtmpl": outfile,
        "format": "best[ext=mp4]",
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
        "logtostderr": False,
        "quiet": True,
    }
    OPTS2 = {
            "format": "best[ext=mp4]",
            "outtmpl": outfile,
            "writethumbnail": True
        }
    with YoutubeDL(OPTS2) as ytdl:
        ytinfo = ytdl.extract_info(link, download=False)
        ytdl.process_info(ytinfo)
        outvideo = ytdl.prepare_filename(ytinfo)
    info = {}
    info["OUTFILE"] = outvideo
    info["THUMBNAIL"] = await yt_thumb(link)
    return info, ytinfo

async def yt_audio(event, link):
    from yt_dlp import YoutubeDL
    randnum = str(random.randint(11111, 99999))
    outfile = client.PATH + "youtube/" + f"{randnum} - %(id)s.%(ext)s"
    OPTS = {
        "progress_hooks": [lambda result: client.yt_progress(event, result)],
        "outtmpl": outfile,
        "format": "bestaudio",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
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
        "logtostderr": False,
        "quiet": True,
    }
    with YoutubeDL(OPTS) as ytdl:
        ytinfo = ytdl.extract_info(link, download=False)
        ytdl.process_info(ytinfo)
        outaudio = ytdl.prepare_filename(ytinfo)
    info = {}
    info["OUTFILE"] = outaudio
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