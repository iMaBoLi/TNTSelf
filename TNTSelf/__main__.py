from . import client
from telethon import __version__ as telever
from TNTSelf import functions
from TNTSelf.functions import AddVarsToClient, load_plugins, DownloadFiles, runcmd
import platform

async def setup():
    client.LOGS.info("• Adding Coustom Vars To Client ...")
    await AddVarsToClient()
    client.functions = functions
    client.LOGS.info("• DownLoading Files To Server ...")
    await DownloadFiles()
    client.LOGS.info("• Installing Main Plugins ...")
    plugs, notplugs = load_plugins(client.PLUGINS)
    client.LOGS.info(f"• Successfully Installed {len(plugs)} Plugin From Main Plugins!")
    client.LOGS.info(f"• Not Installed {len(notplugs)} Plugin From Main Plugins!")
    update = client.DB.get_key("UPDATE") or True
    if update:
        try:
            send = await client.bot.send_message(client.REALM, f"**👋 TNT Self Has Been Start Now !**\n\n**🧒 UserMode :** {client.functions.mention(client.me)}\n**🤖 Manager :** {client.functions.mention(client.bot.me)}")
            if plugs:
                text = "**✅ Loaded Plugins :**\n\n"
                for plug in plugs:
                    text += f"`{plug}`\n"
                #await send.reply(text)
            if notplugs:
                text = "**❌ Unloaded Plugins :**\n\n"
                ftext = ""
                for plug in notplugs:
                    text += f"`{plug}`\n"
                    ftext += f"{notplugs[plug]}\n\n"
                await send.reply(text)
                file = "NotPlugs.txt"
                open(file, "w").write(ftext)
                await send.reply(file=file)
            res = await runcmd('git log --pretty=format:"[%an]: %s" -10')
            if res[0]:
                await send.reply(f"**• Github Commits:**\n\n`{res[0]}`")
        except:
            pass
    client.LOGS.info(f"• Python Version: {platform.python_version()}")
    client.LOGS.info(f"• Telethon Version: {telever}")
    client.LOGS.info(f"• TNTSelf Version: {client.__version__}")
    client.LOGS.info("\n----------------------------------------\n  • Starting TNTSelf Was Successful!\n----------------------------------------")

client.bot.loop.run_until_complete(setup())
client.run_all_clients()
