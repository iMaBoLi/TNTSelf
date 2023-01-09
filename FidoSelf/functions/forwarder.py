from FidoSelf import client
from telethon import TelegramClient

async def save_files(message):
    if not client.backch:
        return (False, client.get_string("LogCh_1"))
    try:
        chat = int(client.backch)
        send = await client.send_message(chat, message)
        info = {"chat_id": send.chat_id, "msg_id": send.id}
        return (True, info)
    except:
        return (False, client.get_string("LogCh_2"))
