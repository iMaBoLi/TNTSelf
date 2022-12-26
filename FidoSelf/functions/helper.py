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

def convert_date(gy, gm, gd):
   g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
   if (gm > 2):
       gy2 = gy + 1
   else:
       gy2 = gy
   days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
   jy = -1595 + (33 * (days // 12053))
   days %= 12053
   jy += 4 * (days // 1461)
   days %= 1461
   if (days > 365):
       jy += (days - 1) // 365
       days = (days - 1) % 365
   if (days < 186):
       jm = 1 + (days // 31)
       jd = 1 + (days % 31)
   else:
      jm = 7 + ((days - 186) // 30)
      jd = 1 + ((days - 186) % 30)
   return [jy, jm, jd]
