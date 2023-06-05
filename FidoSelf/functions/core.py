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