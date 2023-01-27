from FidoSelf import client
from FidoSelf.functions import *
from telethon import events, functions, types, Button
from datetime import datetime
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

async def runner(code , event):
    chat = await event.get_chat()
    reply = await event.get_reply_message()
    local = lambda _x: print(_format.yaml_format(_x))
    exec("async def coderunner(event , local, chat_id, reply): "+ "".join(f"\n {l}" for l in code.split("\n")))
    return await locals()["coderunner"](event , local, chat.id, reply)

@client.bot.on(events.NewMessage(pattern=f"(?i)^(\.|\/|\,)Run(?:\s|$)([\s\S]*)$"))
async def runcodes(event):
    edit = await event.reply(f"`• Running ...`")
    if event.text[4:]:
        cmd = "".join(event.text.split(maxsplit=1)[1:])
    else:
        return await edit.edit(f"**• What Should I Run ?**")
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
    result = "Success‌!"
    if exec:
        result = exec
    elif stderr:
        result = stderr
    elif stdout:
        result = stdout
    if len(result) < 4096:
        await edit.edit(f"**• Results:**\n\n`{result}`")
    else:
        file = "OutPut.txt"
        open(file, "w").write(str(result))
        await client.send_file(event.chat_id, file , caption="**• Your Code OutPut!**")
        os.remove(file)
        await edit.delete()
