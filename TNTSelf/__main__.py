from . import Clients
from telethon import __version__ as telever
from TNTSelf import functions
from traceback import format_exc
import platform
import importlib
import glob
import os
import re
import time
import jdatetime

def load_plugins(files):
    notplugs = {}
    for file in files:
        try:
            filename = file.replace("/", ".").replace(".py" , "")
            importlib.import_module(filename)
        except:
            notplugs.update({os.path.basename(file): format_exc()})
    return notplugs

Clients.LOGS.info("• Starting Setup Plugins ...")
Clients.functions = functions
os.environ["TZ"] = "Asia/Tehran"
time.tzset()
jdatetime.set_locale("fa_IR")
Clients.LOGS.info("• Installing Plugins ...")
#PLUGINS = sorted(glob.glob(f"TNTSelf/plugins/*.py"))
PLUGINS = ["TNTSelf/plugins/Ping.py"]
notplugs = load_plugins(PLUGINS)
installed = len(PLUGINS) - len(notplugs)
Clients.LOGS.info(f"• Successfully Installed {installed} Plugin From Main Plugins!")
Clients.LOGS.info(f"• Not Installed {len(notplugs)} Plugin From Main Plugins!")
for plug in notplugs:
    Clients.LOGS.info(f"• {plug} --->  {notplugs[plug]}")
Clients.LOGS.info(f"• Python Version: {platform.python_version()}")
Clients.LOGS.info(f"• Telethon Version: {telever}")
Clients.LOGS.info(f"• TNTSelf Version: {Clients.__version__}")
Clients.LOGS.info("\n----------------------------------------\n  • Starting TNTSelf Was Successful!\n----------------------------------------")

async def send_setup(sinclient):
    try:
        message = f"**👋 TNT Self Has Been Start Now !**\n\n**🧒 User :** {Clients.functions.mention(sinclient.me)}\n**🤖 Manager :** {Clients.functions.mention(sinclient.bot.me)}"
        await sinclient.bot.send_message(sinclient.REALM, message)
    except:
        pass

for sinclient in Clients.clients:
    sinclient.loop.run_until_complete(send_setup(sinclient))
    
Clients.run_all_clients()