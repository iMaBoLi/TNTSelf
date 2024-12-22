from . import tlclient
from telethon import __version__ as telever
from TNTSelf import functions
from traceback import format_exc
import platform
import importlib
import glob
import os
import re

def load_plugins(files):
    notplugs = {}
    for file in files:
        try:
            filename = file.replace("/", ".").replace(".py" , "")
            importlib.import_module(filename)
        except:
            notplugs.update({os.path.basename(file): format_exc()})
    return notplugs

tlclient.LOGS.info("• Starting Setup Plugins ...")
client.functions = functions
functions.add_vars(tlclient)
tlclient.LOGS.info("• Installing Plugins ...")
PLUGINS = sorted(glob.glob(f"TNTSelf/plugins/*.py"))
notplugs = load_plugins(PLUGINS)
tlclient.LOGS.info(f"• Successfully Installed {len(plugs)} Plugin From Main Plugins!")
tlclient.LOGS.info(f"• Not Installed {len(notplugs)} Plugin From Main Plugins!")
for plug in notplugs:
    tlclient.LOGS.info(f"• {plug} --->  {notplugs[plug]}")
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