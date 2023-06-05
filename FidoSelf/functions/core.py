from FidoSelf import client
from telethon.types import Message
import re

def check_cmd(event):
    if not event.text: return False
    commands = client.DB.get_key("SELFCOMMANDS") or []
    for command in commands:
        search = re.search(command, event.text)
        if search:
            return True
    return False

setattr(Message, "checkCmd", check_cmd)

async def DownloadFiles():
    foshs = client.DB.get_key("FOSHS_FILE")
    if foshs:
        get = await client.get_messages(int(foshs["chat_id"]), ids=int(foshs["msg_id"]))
        await get.download_media("FOSHS.txt")
    foshs = client.DB.get_key("FOSHS_FILE")