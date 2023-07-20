from FidoSelf import client
from youtubesearchpython import VideosSearch
from PIL import Image
import secrets
import re
import os

YOUTUBE_REGEX = re.compile(r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})")

MAIN = "yt-dlp -o '{outfile}' --write-thumbnail -f {format} --max-filesize {size} {link}"
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
    videoid = get_videoid(link) 
    token = secrets.token_hex(nbytes=5)
    outfile = client.PATH + "youtube/" + f"{token} - {videoid}.mp4"
    cmd = MAIN.format(outfile=outfile, format="best", size=client.MAX_SIZE, link=link)
    await client.functions.runcmd(cmd)
    return outfile

async def yt_audio(link):
    from yt_dlp import YoutubeDL
    videoid = get_videoid(link) 
    token = secrets.token_hex(nbytes=5)
    outfile = client.PATH + "youtube/" + f"{token} - {videoid}.mp3"
    cmd = MAIN.format(outfile=outfile, format="bestaudio", size=client.MAX_SIZE, link=link)
    await client.functions.runcmd(cmd)
    return outfile

async def yt_thumb(link):
    videoid = get_videoid(link)
    token = secrets.token_hex(nbytes=5)
    thumb = client.PATH + "youtube/" + f"{token} - {videoid}"
    cmd = THUMB.format(outfile=thumb, link=link)
    await client.functions.runcmd(cmd)
    thumb = convert_thumb(thumb)
    return thumb

def convert_thumb(file):
    thumb = file + ".jpg"
    try:
        img = Image.open(file + ".webp")
        img.save(thumb, format="jpeg")
        os.remove(file + ".webp")
    except:
        os.rename(file + ".webp", thumb)
    return thumb
    
def yt_search(query, limit=50):
    results = VideosSearch(query, limit=limit)
    return results.result()["result"]