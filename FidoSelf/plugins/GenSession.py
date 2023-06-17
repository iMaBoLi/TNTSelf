from FidoSelf import client
from telethon import TelegramClient, Button
from telethon.sessions import StringSession
from telethon.errors import (
    PhoneNumberInvalidError,
    PhoneNumberFloodError,
    PhoneNumberBannedError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
)
import random
import re
import os
import time
import requests
import glob

@client.bot.on(events.NewMessage(pattern="(?i)\/GenerateSession", incoming=True, from_users=[client.me.id]))
async def createsession(event):
    async with client.bot.conversation(event.chat_id) as conv:
        send = await event.reply("**📱 Ok, Send Your Phone Number:**\n\n__• Ex: +19307777777 __")
        response = await conv.get_response(send.id)
        phone = response.text
    edit = await event.reply("`♻️ Please Wait . . .`")
    client = TelegramClient(StringSession(), 13367220, "52cdad8b941c04c0c85d28ed6b765825", device_model="• Acc-Manager 🔐")
    await client.connect()
    try:
        scode = await client.send_code_request(phone, force_sms=False)
        await event.reply(str(scode))
        async with client.bot.conversation(event.chat_id) as conv:
            send = await edit.edit(f"**💠 Ok, Send Your Telegram Code For Your Phone:** ( `{phone}` )")
            response = await conv.get_response(send.id)
            phone_code = response.text
    except (PhoneNumberInvalidError, TypeError):
        return await edit.edit("**❌ Your Phone Number Is Invalid!**")
    except PhoneNumberFloodError:
        return await edit.edit("**❓ Your Phone Number Is Flooded!**")
    except PhoneNumberBannedError:
        return await edit.edit("**🚫 Your Phone Number Is Banned!**")
    edit = await event.reply("`♻️ Please Wait . . .`")
    phone_code = phone_code.replace(" ", "")
    try:
        await client.sign_in(phone=phone, code=phone_code, password=None)
        session = client.session.save()
        return await edit.edit(f"**• String Session:**\n\n`{session}`")
    except (PhoneCodeInvalidError, TypeError):
        return await edit.edit("**❌ Your Code Is Invalid, Try Again!**")
    except PhoneCodeExpiredError:
        return await edit.edit("**🚫 Your Code Is Expired, Try Again!**")
    except SessionPasswordNeededError:
        async with client.bot.conversation(event.chat_id) as conv:
            send = await edit.edit(f"**🔐 Ok, Send Your Account 2Fa Password For Your Phone:** ( `{phone}` )")
            response = await conv.get_response(send.id)
            password = response.text
        edit = await event.reply("`♻️ Please Wait . . .`")
        try:
            await client.sign_in(password=password)
            session = client.session.save()
            return await edit.edit(f"**• String Session:**\n\n`{session}`")
        except PasswordHashInvalidError:
            return await edit.edit("**❌ Your Account Password Is Invalid, Try Again!**")
        except Exception as error:
            return await edit.edit(error)
    except Exception as error:
        return await edit.edit(error)