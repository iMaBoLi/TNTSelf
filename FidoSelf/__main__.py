from . import client
from telethon import __version__ as telever
from FidoSelf import functions
from FidoSelf.functions import AddVarsToClient, load_plugins, DownloadFiles, runcmd
import platform

async def setup():
    client.LOGS.info("• Installing Youtube Downloader ...")
    await runcmd("pip install git+https://github.com/yt-dlp/yt-dlp")
    client.LOGS.info("• Adding Coustom Vars To Client ...")
    await AddVarsToClient()
    client.functions = functions
    client.LOGS.info("• Installing Main Plugins ...")
    plugs, notplugs = load_plugins(client.PLUGINS)
    client.LOGS.info(f"• Successfully Installed {len(plugs)} Plugin From Main Plugins!")
    client.LOGS.info(f"• Not Installed {len(notplugs)} Plugin From Main Plugins!")
    client.LOGS.info("• DownLoading Files To Server ...")
    await DownloadFiles()
    update = client.DB.get_key("UPDATE") or True
    if update:
        try:
            send = await client.bot.send_message(client.REALM, f"**👋 Fido Self Has Been Start Now !**\n\n**🧒 UserMode :** {client.mention(client.me)}\n**🤖 Manager :** {client.mention(client.bot.me)}")
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
            res = await runcmd('git log --pretty=format:"[%an]: %s" -3')
            if res[0]:
                await send.reply(f"**• Github Commits:**\n\n`{res[0]}`")
        except:
            pass
    client.LOGS.info(f"• Python Version: {platform.python_version()}")
    client.LOGS.info(f"• Telethon Version: {telever}")
    client.LOGS.info(f"• FidoSelf Version: {client.__version__}")
    client.LOGS.info("\n----------------------------------------\n  • Starting FidoSelf Was Successful!\n----------------------------------------")

client.bot.loop.run_until_complete(setup())
client.run_until_disconnected()
