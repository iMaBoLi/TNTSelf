from . import tlclient
from telethon import __version__ as telever
from TNTSelf import functions
from TNTSelf.functions import load_plugins
import platform

tlclient.LOGS.info("• Starting Setup Plugins ...")
tlclient.functions = functions
tlclient.LOGS.info("• Installing Plugins ...")
plugs, notplugs = load_plugins(tlclient.PLUGINS)
tlclient.LOGS.info(f"• Successfully Installed {len(plugs)} Plugin From Main Plugins!")
tlclient.LOGS.info(f"• Not Installed {len(notplugs)} Plugin From Main Plugins!")
for plug in notplugs:
    tlclient.LOGS.info(f"• {plug}")
tlclient.LOGS.info(f"• Python Version: {platform.python_version()}")
tlclient.LOGS.info(f"• Telethon Version: {telever}")
tlclient.LOGS.info(f"• TNTSelf Version: {tlclient.__version__}")
tlclient.LOGS.info("\n----------------------------------------\n  • Starting TNTSelf Was Successful!\n----------------------------------------")

tlclient.run_all_clients()

async def send_setup(client):
    message = f"**👋 TNT Self Has Been Start Now !**\n\n**🧒 User :** {tlclient.functions.mention(client.me)}\n**🤖 Manager :** {tlclient.functions.mention(client.bot.me)}"
    await client.bot.send_message(client.REALM, message)

for client in tlclient.clients:
    client.loop.run_until_complete(send_setup(client))