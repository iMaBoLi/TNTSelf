from . import client, START_TIME, __version__
from telethon import __version__ as telever
from FidoSelf.functions.utils import load_plugins, LOADED_PLUGS, NOT_LOADED_PLUGS
from FidoSelf.functions.misc import stimezone, addvars
import time
import platform

async def setup():
    client.LOGS.info("• Adding Coustom Vars To Client ...")
    await addvars()
    client.LOGS.info("• Setting Your TimeZone ...")
    stimezone()
    client.LOGS.info("• Installing Main Plugins ...")
    load_plugins("FidoSelf/plugins")
    client.LOGS.info(f"• Successfully Installed {len(LOADED_PLUGS)} From Main Plugins!")
    endtime = client.utils.convert_time(time.time() - START_TIME)
    try:
        send = await client.bot.send_message((client.realm or client.me.id), f"**👋 Fido Self Has Been Start Now !**\n\n**🧒 UserMode :** {client.mention(client.me)}\n**🤖 Manager :** {client.mention(client.bot.me)}\n\n__Took In: {endtime}__")
        if LOADED_PLUGS:
            text = f"**✅ Loaded Plugins :**\n\n"
            for plug in LOADED_PLUGS:
                text += f"{client.str} `{plug}`\n"
            await send.reply(text)
        if NOT_LOADED_PLUGS:
            for plug in NOT_LOADED_PLUGS:
                text = f"**❌ Unloaded Plugin :**\n\n"
                text += f"{client.str} `{plug}` - ( `{NOT_LOADED_PLUGS[plug]}` )\n"
                await send.reply(text)
        res = await client.utils.runcmd('git log --pretty=format:"[%an]: %s" -20')
        await send.reply(f"**{client.str} The Github Commits:**\n\n`{res[0]}`")
    except:
        pass
    client.LOGS.info(f"• Took In ( {endtime} )")
    client.LOGS.info(f"• Python Version: {platform.python_version()}")
    client.LOGS.info(f"• Telethon Version: {telever}")
    client.LOGS.info(f"• FidoSelf Version: {__version__}")
    client.LOGS.info("\n----------------------------------------\n  • Starting FidoSelf Was Successful!\n----------------------------------------")

client.bot.loop.run_until_complete(setup())
client.run_until_disconnected()
