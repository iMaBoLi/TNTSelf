from FidoSelf import client
from FidoSelf.functions.utils import runcmd
from telethon import events, functions, types, Button
import traceback
import requests
import asyncio
import os
import sys
import io
import glob
import re
import json

async def runner(code , event):
    chat = await event.get_chat()
    reply = await event.get_reply_message()
    local = lambda _x: print(_format.yaml_format(_x))
    exec("async def coderunner(event , local, chat_id, reply): "+ "".join(f"\n {l}" for l in code.split("\n")))
    return await locals()["coderunner"](event , local, chat.id, reply)

@client.Cmd(pattern=f"(?i)^\{client.cmd}run(?:\s|$)([\s\S]*)$", sudo=False)
async def runcodes(event):
    await event.edit(f"`{client.str} Running ...`")
    if event.text[4:]:
        cmd = "".join(event.text.split(maxsplit=1)[1:])
    else:
        return await event.edit(f"**{client.str} What Should I Run ?**")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await runner(cmd , event)
    except Exception as e:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    result = None
    if exc:
        result = exc
        res = "Errors"
    elif stderr:
        result = stderr
        res = "Errors"
    elif stdout:
        result = stdout
        res = "Results"
    else:
        result = "Success‌!"
        res = "Results"
    out = f"""
**{client.str} Code :** 
`{event.text}`

**{client.str} {res} :** 
`{result}`
"""
    if len(out) < 4096:
        await event.edit(out)
    else:
        f = open(f"{res}.txt", "w")
        f.write(str(result))
        try:
            await client.send_file(event.chat_id, f"{res}.txt" , caption=f"""
**{client.str} Code :** 
`{event.text}`

**{client.str} {res} :** 
**In File‌!**
""")
        except:
            out = f"""
{client.str} Code:
{event.text}

{client.str} {res}: 
{result}
"""
            f = open(f"{res}.txt", "w")
            f.write(str(out))
            await client.send_file(event.chat_id, f"{res}.txt" , caption=f"**{client.str} {res} :** \n\n**In File‌!**")
        os.remove(f"{res}.txt")
        await event.delete()
