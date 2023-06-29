from FidoSelf import client
from traceback import format_exc
import importlib
import glob
import os
import re

def get_plugins():
    files = sorted(glob.glob(f"FidoSelf/plugins/*.py"))
    return files

def load_plugins(files, reload=False):
    plugs = []
    notplugs = {}
    for file in files:
        try:
            filename = file.replace("/", ".").replace(".py" , "")
            module = importlib.import_module(filename)
            if reload:
                importlib.reload(module)
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