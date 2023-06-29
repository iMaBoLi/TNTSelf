from FidoSelf import client
from traceback import format_exc
from importlib import import_module
import glob
import os
import re

def get_plugins():
    files = sorted(glob.glob(f"FidoSelf/plugins/*.py"))
    return files

def load_plugins(files):
    plugs = []
    notplugs = {}
    for file in files:
        try:
            filename = file.replace("/", ".").replace(".py" , "")
            import_module(filename)
            plugs.append(os.path.basename(file))
        except:
            notplugs.update({os.path.basename(file): format_exc()})
    return plugs, notplugs

def remove_handlers(file):
    data = open(file, "r").read()
    finds = re.findall("def (.*)\(", data)
    for find in finds:
        if find in client.HANDLERS:
            client.remove_event_handler(client.HANDLERS[find])
            del client.HANDLERS[find]