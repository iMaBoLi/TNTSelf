from TNTSelf import client
from TNTSelf.functions import *
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
    await event.edit(client.STRINGS["wait"])
    if os.path.exists("TNT.log"):
        text = open("TNT.log", "r").read()
        open("TNT.txt", "w").write(str(text))
        await event.respond("**The Console Logs File!**", file="TNT.txt")
        await event.delete()
    else:
        await event.edit("**The Log File Is Not Available!**")
        
@client.Command(command="File (.*)")
async def file(event):
    await event.edit(client.STRINGS["wait"])
    file = event.pattern_match.group(1)
    if os.path.exists(file):
        await event.respond(f"**The {file} File!**", file=file)
        await event.delete()
    else:
        await event.edit(f"**The File {file} Is Not Available!**")
        
async def runner(code , event):
    chat = await event.get_chat()
    reply = await event.get_reply_message()
    local = lambda out: print(_format.yaml_format(out))
    exec("async def coderunner(event , local, chat, chat_id, reply): "+ "".join(f"\n {line}" for line in code.split("\n")))
    return await locals()["coderunner"](event , local, chat, chat.id, reply)

@client.Command(command="Run(?:\\s|$)([\\s\\S]*)")
async def runcodes(event):
    reply = await event.reply(f"**Running ...**")
    if event.text[4:]:
        cmd = "".join(event.text.split(maxsplit=1)[1:])
    else:
        return await reply.edit(f"**What Should I Run ?**")
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
    error = ""
    if exec:
        error = exec
    elif stderr:
        error = stderr
    elif stdout:
        result = stdout
    if error:
        if len(error) < 3000:
            await reply.edit(f"**Errors:**\n\n`{error}`")
        else:
            file = event.client.PATH + "Error.txt"
            open(file, "w").write(str(error))
            await event.client.send_file(event.chat_id, file , caption="**Code Errors!**", reply_to=event.id)
            os.remove(file)
            await reply.delete()
    else:
        if len(result) < 3000:
            await reply.edit(f"**Results:**\n\n`{result}`")
        else:
            file = event.client.PATH + "Result.txt"
            open(file, "w").write(str(result))
            await event.client.send_file(event.chat_id, file , caption="**Code Results!**", reply_to=event.id)
            os.remove(file)
            await reply.delete()

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
        uptime = client.functions.convert_time(time.time() - os.path.getmtime(path))
        output += f"    **Location:** `{path}`\n"
        output += f"    **Size:** `{client.functions.convert_bytes(size)}`\n"
        output += f"    **Update Time:** `{uptime}`\n"
    if len(output) < 4000:
        await event.edit(output) 
    else:
        output = output.replace("*", "").replace("`", "")
        open("FileList.txt", "w").write(output)
        await event.respond("**Results In File!**", file="FileList.txt")
        await event.delete()

