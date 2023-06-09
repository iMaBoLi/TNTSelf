from youtubesearchpython import VideosSearch
import yt_dlp
import os
import re

YOUTUBE_URL = "https://www.youtube.com/watch?v="
YOUTUBE_REGEX = re.compile(r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})")

song_dl = "yt-dlp --force-ipv4 --write-thumbnail --add-metadata --embed-thumbnail -o './temp/%(title)s.%(ext)s' --extract-audio --audio-format mp3 --audio-quality {QUALITY} {video_link}"
thumb_dl = "yt-dlp --force-ipv4 -o './temp/%(title)s.%(ext)s' --write-thumbnail --skip-download {video_link}"
video_dl = "yt-dlp --force-ipv4 --write-thumbnail --add-metadata --embed-thumbnail -o './temp/%(title)s.%(ext)s' -f 'best[height<=480]' {video_link}"
name_dl = "yt-dlp --force-ipv4 --get-filename -o './temp/%(title)s.%(ext)s' {video_link}"

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