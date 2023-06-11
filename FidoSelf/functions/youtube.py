from FidoSelf import client
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
from PIL import Image
import random
import os
import re

YOUTUBE_URL = "https://www.youtube.com/watch?v="
YOUTUBE_REGEX = re.compile(r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})")

MAIN = "yt-dlp -o '{outfile}' -f {format} {link}"
THUMB = "yt-dlp -o '{outfile}' --write-thumbnail --skip-download {link}"

def yt_info(link):
    info = YoutubeDL().extract_info(link, download=False)
    return info

def get_videoid(url):
    match = YOUTUBE_REGEX.search(url)
    return match.group(1)

async def yt_downloader(link, format, ext):
    filename = get_videoid(link) + str(random.randint(11111, 99999))
    outfile = client.PATH + "youtube/" + filename + "." + ext
    cmd = MAIN.format(outfile=outfile, format=format, link=link)
    await client.functions.runcmd(cmd)
    info = {}
    info["OUTFILE"] = outfile
    thumb = await yt_thumb(link)
    info["THUMBNAIL"] = thumb
    return info

def yt_search(query, limit=50):
    results = VideosSearch(query, limit=limit)
    return results.result()["result"]
    
def get_formats(link):
    info = yt_info(link)
    videoformats = {}
    audioformats = {}
    for format in info["formats"]:
        if format["ext"] == "mp4" and and format["filesize"] and format["audio_channels"]:
            videoformats.update({format["format_id"]: {"ext": format["ext"], "filesize": format["filesize"], "format": format["format_note"]}})
        if format["ext"] == "m4a" and format["filesize"]:
            if format["format_note"] == "low":
                audioformats.update({format["format_id"]: {"ext": "mp3", "filesize": format["filesize"], "format": "128K"}})
            elif format["format_note"] == "medium":
                audioformats.update({format["format_id"]: {"ext": "mp3", "filesize": format["filesize"], "format": "320K"}})
    return videoformats, audioformats

async def yt_thumb(link):
    filename = get_videoid(link) + str(random.randint(11111, 99999))
    thumb = client.PATH + "youtube/" + filename
    cmd = THUMB.format(outfile=thumb, link=link)
    await client.functions.runcmd(cmd)
    thumb = convert_thumb(thumb)
    return thumb
    
def convert_thumb(file):
    img = Image.open(file + ".webp")
    img.save(file + ".jpg", format="jpeg")
    os.remove(file + ".webp")
    return file + ".jpg"