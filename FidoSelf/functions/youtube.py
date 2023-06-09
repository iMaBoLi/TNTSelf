from FidoSelf import client
from youtubesearchpython import VideosSearch
import yt_dlp
import os
import re

YOUTUBE_URL = "https://www.youtube.com/watch?v="
YOUTUBE_REGEX = re.compile(r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})")

VIDEO = "yt-dlp --force-ipv4 --write-thumbnail --add-metadata --embed-thumbnail -o '{outfile}' -f 'best[height=={quality}}]' {link}"
SONG = "yt-dlp --force-ipv4 --write-thumbnail --add-metadata --embed-thumbnail -o '{outfile}' --extract-audio --audio-format mp3 --audio-quality {quality} {link}"
THUMB = "yt-dlp --force-ipv4 -o '{outfile}' --write-thumbnail --skip-download {link}"

async def yt_downloader(link, type, quality, outfile):
    if type == "video":
        cmd = VIDEO.format(link=link, quality=quality, outfile=outfile)
        await client.functions.runcmd(cmd)
        return outfile
    elif type == "music":
        cmd = SONG.format(link=link, quality=quality, outfile=outfile)
        await client.functions.runcmd(cmd)
        return outfile
        
def get_videoid(url):
    match = YOUTUBE_REGEX.search(url)
    return match.group(1)

def get_downinfo(type):
    choice = "bestvideo+bestaudio/best"
    disp = "best(video+audio)"
    if type == "mkv":
        choice = "bestvideo+bestaudio/best"
        disp = "best(video+audio)"
    elif type == "mp4":
        choice = "bestvideo[ext=webm]+251/bestvideo[ext=mp4]+(258/256/140/bestaudio[ext=m4a])/bestvideo[ext=webm]+(250/249)/best"
        disp = "best(video+audio)[webm/mp4]"
    elif type == "mp3":
        choice = "320"
        disp = "320 Kbps"
    return choice, disp