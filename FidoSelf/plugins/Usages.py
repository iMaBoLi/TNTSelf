from FidoSelf import client
from FidoSelf.functions import *
from telethon import events, functions, types, Button
from datetime import datetime
from pathlib import Path
import traceback
import requests
import asyncio
import os
import sys
import io
import glob
import re
import json
import time

@client.Command(command="Logs")
async def logs(event):
    await event.edit(client.getstrings()["wait"])
    if os.path.exists("Fido.log"):
        await event.respond("**The Console Logs File!**", file="Fido.log")
        await event.delete()
    else:
        await event.edit("**The Log File Is Not Available!**")

async def runner(code , event):
    chat = await event.get_chat()
    reply = await event.get_reply_message()
    local = lambda out: print(_format.yaml_format(out))
    exec("async def coderunner(event , local, chat, chat_id, reply): "+ "".join(f"\n {line}" for line in code.split("\n")))
    return await locals()["coderunner"](event , local, chat, chat.id, reply)

@client.Command(command="Run(?:\s|$)([\s\S]*)")
async def runcodes(event):
    edit = await event.reply(f"**Running ...**")
    if event.text[4:]:
        cmd = "".join(event.text.split(maxsplit=1)[1:])
    else:
        return await edit.edit(f"**What Should I Run ?**")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exec = None, None, None
    try:
        await runner(cmd , event)
    except:
        exec = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    result = "Success!"
    if exec:
        result = exec
    elif stderr:
        result = stderr
    elif stdout:
        result = stdout
    if len(result) < 4096:
        await edit.edit(f"**Results:**\n\n`{result}`")
    else:
        file = client.PATH + "OutPut.txt"
        open(file, "w").write(str(result))
        await client.send_file(event.chat_id, file , caption="**Code OutPut!**", reply_to=event.id)
        os.remove(file)
        await edit.delete()

@client.Command(command="Ls ?(.*)?")
async def ls(event):
    await event.edit(client.getstrings()["wait"])
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
                files += f"   `{contents}` - `{convert_bytes(size)}`\n"
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
