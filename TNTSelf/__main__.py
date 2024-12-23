from . import client
from TNTSelf import functions
from telethon import __version__
from traceback import format_exc
import platform
import importlib
import glob
import os

def load_plugins(files):
    notplugs = {}
    for file in files:
        try:
            filename = file.replace("/", ".").replace(".py" , "")
            importlib.import_module(filename)
        except:
            notplugs.update({os.path.basename(file): format_exc()})
    return notplugs

client.LOGS.info("• Starting Setup Plugins ...")
client.add_coustom_vars()
client.functions = functions
client.LOGS.info("• Installing Plugins ...")
PLUGINS = sorted(glob.glob(f"TNTSelf/plugins/*.py"))
#PLUGINS = ["TNTSelf/plugins/Ping.py", "TNTSelf/plugins/NameTime.py", "TNTSelf/plugins/ManageTime.py"]
notplugs = load_plugins(PLUGINS)
installed = len(PLUGINS) - len(notplugs)
client.LOGS.info(f"• Successfully Installed {installed} Plugin From Main Plugins!")
client.LOGS.info(f"• Not Installed {len(notplugs)} Plugin From Main Plugins!")
#for plug in notplugs:
    #client.LOGS.info(f"• {plug} --->  {notplugs[plug]}")
client.LOGS.info(f"• Python Version: {platform.python_version()}")
client.LOGS.info(f"• Telethon Version: {__version__}")
client.LOGS.info(f"• TNTSelf Version: {client.__version__}")
client.LOGS.info("\n----------------------------------------\n  • Starting TNTSelf Was Successful!\n----------------------------------------")

async def send_setup(sinclient):
    try:
        message = f"**👋 TNT Self Has Been Start Now !**\n\n**🧒 User :** {client.functions.mention(sinclient.me)}\n**🤖 Manager :** {client.functions.mention(sinclient.bot.me)}"
        await sinclient.bot.send_message(sinclient.REALM, message)
    except:
        pass

for sinclient in client.clients:
    sinclient.loop.run_until_complete(send_setup(sinclient))
    
client.run_all_clients()