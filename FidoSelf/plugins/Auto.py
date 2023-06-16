from FidoSelf import client
import aiocron
import time

@client.Command(command="AddChat")
async def addauto(event):
    await event.edit(client.STRINGS["wait"])
    CHATS = client.DB.get_key("AUTO_CHATS")
    ntime = time.time()
    CHATS.update({event.chat_id: ntime})
    client.DB.set_key("AUTO_CHATS", CHATS)
    await event.delete()
    
@aiocron.crontab("*/1 * * * *")
async def autosender():
    CHATS = client.DB.get_key("AUTO_CHATS")
    Baner = """
    🩵 سلف با امکانات فوق العاده خفن!

• هر چی که بگین داره!

• آپدیت های فراوان به صورت روزانه!

• ران کردن روی سرور پر سرعت با قیمت مناسب!

• برای دیدن امکانات پیوی!
    """
    for chatid in CHATS:
        ltime = CHATS[chatid]
        ntime = time.time()
        if ntime > (ltime + 60):
            await client.send_message(chatid, Baner)
            CHATS[chatid] = ntime
            client.DB.set_key("AUTO_CHATS", CHATS)