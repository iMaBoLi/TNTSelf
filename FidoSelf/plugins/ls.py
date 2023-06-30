from FidoSelf import client
from FidoSelf.functions.utils import convert_bytes, convert_time
from pathlib import Path
import os
import time

def get_file_icon(name):
    if str(name).endswith((".mp3", ".flac", ".wav", ".m4a")):
        type = "🎵"
    elif str(name).endswith((".opus")):
        type = "🎙"
    elif str(name).endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
        type = "🖼️"
    elif str(name).endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
        type = "🎞"
    elif str(name).endswith((".zip", ".tar", ".tar.gz", ".rar")):
        type = "🗜"
    elif str(name).endswith((".py")):
        type = "🐍"
    else:
        type = "📝"
    return type

@client.Command(command="Ls ?(.*)?")
async def ls(event):
    await event.edit(client.STRINGS["wait"])
    input = "".join(event.text.split(maxsplit=1)[1:])
    path = input or os.getcwd()
    if not os.path.exists(path):
        return await event.edit(f"**The File With The Name** ( `{input}` ) **Is Not Finded!**")
    path = Path(input) if input else os.getcwd()
    if os.path.isdir(path):
        if input:
            output = f"**Folders And Files In** ( `{path}` ):\n\n"
        else:
            output = "**Folders And Files in Current Directory:**\n\n"
        lists = os.listdir(path)
        files = ""
        folders = ""
        for contents in sorted(lists):
            if str(contents) == "__pycache__": continue
            newpath = os.path.join(path, contents)
            if os.path.isfile(newpath):
                size = os.path.getsize(newpath)
                icon = get_file_icon(contents)
                files += f"{icon} `{contents}` - `{convert_bytes(size)}`\n"
            else:
                folders += f"🗂 `{contents}`\n"
        if files or folders:
            output = output + folders + files
        else:
            output = output + "**Empty Path!**"
    else:
        size = os.path.getsize(path)
        output = "**The Details Of File:**\n\n"
        uptime = convert_time(time.time() - os.path.getmtime(path))
        output += f"    **Location:** `{path}`\n"
        output += f"    **Size:** `{convert_bytes(size)}`\n"
        output += f"    **Update Time:** `{uptime}`\n"
    if len(output) < 4000:
        await event.edit(output) 
    else:
        output = output.replace("*", "").replace("`", "")
        open("ls.txt", "w").write(output)
        await event.respond("**Results In File!**", file="ls.txt")
        await event.delete()
