from . import TLclient
from telethon import __version__ as telever
from TNTSelf import functions
from traceback import format_exc
import platform
import glob
import os
import re
import time
import jdatetime

def load_plugins(files):
    import importlib
    notplugs = {}
    for file in files:
        try:
            filename = file.replace("/", ".").replace(".py" , "")
            importlib.import_module(filename)
        except:
            notplugs.update({os.path.basename(file): format_exc()})
    return notplugs

TLclient.LOGS.info("• Starting Setup Plugins ...")
TLclient.functions = functions
os.environ["TZ"] = "Asia/Tehran"
time.tzset()
jdatetime.set_locale("fa_IR")
TLclient.LOGS.info("• Installing Plugins ...")
#PLUGINS = sorted(glob.glob(f"TNTSelf/plugins/*.py"))
PLUGINS = ["TNTSelf/plugins/Ping.py"]
notplugs = load_plugins(PLUGINS)
installed = len(PLUGINS) - len(notplugs)
TLclient.LOGS.info(f"• Successfully Installed {installed} Plugin From Main Plugins!")
TLclient.LOGS.info(f"• Not Installed {len(notplugs)} Plugin From Main Plugins!")
for plug in notplugs:
    TLclient.LOGS.info(f"• {plug} --->  {notplugs[plug]}")
TLclient.LOGS.info(f"• Python Version: {platform.python_version()}")
TLclient.LOGS.info(f"• Telethon Version: {telever}")
TLclient.LOGS.info(f"• TNTSelf Version: {TLclient.__version__}")
TLclient.LOGS.info("\n----------------------------------------\n  • Starting TNTSelf Was Successful!\n----------------------------------------")

async def send_setup(sinclient):
    try:
        message = f"**👋 TNT Self Has Been Start Now !**\n\n**🧒 User :** {TLclient.functions.mention(sinclient.me)}\n**🤖 Manager :** {TLclient.functions.mention(sinclient.bot.me)}"
        await sinclient.bot.send_message(sinclient.REALM, message)
    except:
        pass

for sinclient in TLclient.clients:
    sinclient.loop.run_until_complete(send_setup(sinclient))
    
TLclient.run_all_clients()