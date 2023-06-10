from FidoSelf import client
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
import requests
import os
import re

YOUTUBE_URL = "https://www.youtube.com/watch?v="
YOUTUBE_REGEX = re.compile(r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})")

VIDEO = "yt-dlp -o '{outfile}' -f 'best[height>={quality}]' {link}"
SONG = "yt-dlp -o '{outfile}' --extract-audio --audio-format mp3 --audio-quality {quality} {link}"
THUMB = "yt-dlp -o '{outfile}' --write-thumbnail --skip-download {link}"

async def yt_downloader(link, type, quality):
    info = YoutubeDL().extract_info(link, download=False)
    videoid = info["id"]
    thumb = client.PATH + "youtube/" + videoid
    cmd = THUMB.format(outfile=thumb, link=link)
    await client.functions.runcmd(cmd)
    thumb = convert_thumb(thumb)
    if type == "video":
        outfile = client.PATH + "youtube/" + videoid + ".mp4"
        cmd = VIDEO.format(outfile=outfile, quality=quality, link=link)
        await client.functions.runcmd(cmd)
    elif type == "music":
        outfile = client.PATH + "youtube/" + videoid + ".mp3"
        cmd = SONG.format(outfile=outfile, quality=quality, link=link)
        await client.functions.runcmd(cmd)
    info["OUTFILE"] = outfile
    info["THUMBNAIL"] = thumb
    return info
        
def get_videoid(url):
    match = YOUTUBE_REGEX.search(url)
    return match.group(1)
    
def convert_thumb(file):
    img = Image.open(file + ".webp")
    img.save(file + ".jpg", format="jpeg")
    os.remove(file + ".webp")
    return file + ".jpg"