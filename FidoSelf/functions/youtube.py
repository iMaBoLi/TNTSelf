from FidoSelf import client
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
from PIL import Image
import random
import os
import re

YOUTUBE_URL = "https://www.youtube.com/watch?v="
YOUTUBE_REGEX = re.compile(r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})")

VIDEO = "yt-dlp -o '{outfile}' -f 'best[height>={quality}]' {link}"
SONG = "yt-dlp -o '{outfile}' --extract-audio --audio-format mp3 --audio-quality {quality} {link}"
THUMB = "yt-dlp -o '{outfile}' --write-thumbnail --skip-download {link}"

def yt_info(link):
    info = YoutubeDL().extract_info(link, download=False)
    return info

async def yt_downloader(link, type, quality):
    filename = get_videoid(link) + str(random.randint(11111, 99999))
    thumb = await yt_thumb(link)
    if type == "video":
        outfile = client.PATH + "youtube/" + filename + ".mp4"
        cmd = VIDEO.format(outfile=outfile, quality=quality, link=link)
        await client.functions.runcmd(cmd)
    elif type == "music":
        outfile = client.PATH + "youtube/" + filename + ".mp3"
        cmd = SONG.format(outfile=outfile, quality=quality, link=link)
        await client.functions.runcmd(cmd)
    info = {}
    info["OUTFILE"] = outfile
    info["THUMBNAIL"] = thumb
    return info

async def yt_thumb(link):
    filename = get_videoid(link) + str(random.randint(11111, 99999))
    thumb = client.PATH + "youtube/" + filename
    cmd = THUMB.format(outfile=thumb, link=link)
    await client.functions.runcmd(cmd)
    thumb = convert_thumb(thumb)
    return thumb

def get_videoid(url):
    match = YOUTUBE_REGEX.search(url)
    return match.group(1)
    
def convert_thumb(file):
    img = Image.open(file + ".webp")
    img.save(file + ".jpg", format="jpeg")
    os.remove(file + ".webp")
    return file + ".jpg"
    
def yt_search(query, limit=50):
    results = VideosSearch(query, limit=limit)
    return results.result()["result"]
    
def get_formats(link):
    info = yt_info(link)
    videoformats = {}
    audioformats = {}
    for format in info["formats"]:
        if format["ext"] in ["mp4", "webp"] or (format["ext"] in ["webm"] and str(format["video_ext"]) in ["webm"]):
            formatname = format["format"].split(" - ")[1]
            videoformats.update({format["format_id"]: {"ext": format["ext"], "filesize": format["filesize"], "format": formatname, "format_note": format["format_note"], "resolution": format["resolution"], "width": format["width"], "height": format["height"]}})
        if format["ext"] in ["m4a"]:
            formatname = format["format"].split(" - ")[1]
            audioformats.update({format["format_id"]: {"ext": format["ext"], "filesize": format["filesize"], "format": formatname, "format_note": format["format_note"], "resolution": format["resolution"], "width": format["width"], "height": format["height"]}})
    return videoformats, audioformats