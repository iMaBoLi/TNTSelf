from FidoSelf import client
from FidoSelf.functions.utils import convert_bytes
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

@client.Cmd(pattern=f"(?i)^\{client.cmd}ls(?:\s|$)([\s\S]*)$")
async def ls(event):
    await event.edit(client.get_string("Wait").format(client.str))
    input = "".join(event.text.split(maxsplit=1)[1:])
    path = input or os.getcwd()
    if not os.path.exists(path):
        return await event.edit(f"**{client.str} There Is No Such Directory Or File With The Name :** ( `{input}` )")
    path = Path(input) if input else os.getcwd()
    if os.path.isdir(path):
        if input:
            output = f"**{client.str} Folders And Files In** ( `{path}` ):\n\n"
        else:
            output = f"**{client.str} Folders And Files in Current Directory:**\n\n"
        lists = os.listdir(path)
        files = ""
        folders = ""
        for contents in sorted(lists):
            if str(contents) == "__pycache__":
                continue
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
        output = f"**{client.str} The Details Of Given File:**\n\n"
        icon = get_file_icon(path)
        time2 = time.ctime(os.path.getmtime(path))
        time3 = time.ctime(os.path.getatime(path))
        output += f"**♀️ Location:** `{path}`\n"
        output += f"**🔶 icon:** `{icon}`\n"
        output += f"**♻️ Size:** `{convert_bytes(size)}`\n"
        output += f"**🔃 Last Modified Time:** `{time2}`\n"
        output += f"**🔄 Last Accessed Time:** `{time3}`"
    if len(output) < 1500:
        await event.edit(output) 
    else:
        output = output.replace("*", "").replace("`", "")
        open("ls.txt", "w").write(output)
        await event.reply(f"**{client.str} Results In File‌!**", file="ls.txt")
        await event.delete()
