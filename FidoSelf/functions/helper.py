from FidoSelf import client
import asyncio
import time
import math

async def progress(event, current, total, start, type, file_name=None):
    if type == "down":
        type = "Downloading . . ."
    elif type == "up":
        type = "Uploading . . ."
    now = time.time()
    diff = time.time() - start
    if round(diff % 7.00) == 0 or current == total:
        perc = current * 100 / total
        speed = current / diff
        eta = round((total - current) / speed) * 1000
        strs = "".join("●" for i in range(math.floor(perc / 5)))
        text = f"""
`{client.str} {type}`\n\n
`[ {strs} ]{round(perc, 2)}%`\n\n
**{client.str} File Name:** ( `{file_name or "---"}` )\n
**{client.str} Size:** ( `{client.utils.convert_bytes(current)}` **Of** `{client.utils.convert_bytes(total)}` )\n
**{client.str} Speed:** ( `{client.utils.convert_bytes(speed)}` )\n
**{client.str} ETA:** ( `{client.utils.convert_time(eta) or "---"}` )
"""
        await event.edit(text)

def mention(info):
    if info.username:
        return "@" + info.username
    return f"[{info.first_name}](tg://user?id={info.id})"
