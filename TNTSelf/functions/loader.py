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
            importlib.import_module(filename)
            plugs.append(os.path.basename(file))
        except:
            notplugs.update({os.path.basename(file): format_exc()})
    return plugs, notplugs