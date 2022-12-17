from pathlib import Path
from traceback import format_exc
import os
import sys
import time
import logging
import math
import importlib
import glob
import shlex
import asyncio
import functools
import re
import random
import logging

LOADED_PLUGS = []
NOT_LOADED_PLUGS = {}

def shuffle(list, count=5):
    for i in range(count):
        r = random.random()
        random.shuffle(list, lambda: r)
    return list

async def runcmd(cmd):
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    return stdout.decode("utf-8", "replace").strip(), stderr.decode("utf-8", "replace").strip()

def chunks(elements, size):
    n = max(1, size)
    return (elements[i:i + n] for i in range(0, len(elements), n))

def load_plugins(folder):
    files = sorted(glob.glob(f"{folder}/*.py"))
    for name in files:
        plugin_name = os.path.basename(name)
        filename = plugin_name.replace(".py" , "")
        try:
            path = Path(f"{folder}/{plugin_name}")
            name = "{}.{}".format(folder.replace("/", "."), filename)
            spec = importlib.util.spec_from_file_location(name, path)
            load = importlib.util.module_from_spec(spec)
            load.logger = logging.getLogger(plugin_name)
            spec.loader.exec_module(load)
            sys.modules[name] = load
            LOADED_PLUGS.append(filename)
        except:
            NOT_LOADED_PLUGS.update({filename: format_exc()})
            
def convert_bytes(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s%s" % (s, size_name[i])

def convert_time(seconds, mili=False):
    if mili:
        seconds = int(seconds) / 1000
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    result = (
        ((str(weeks) + "w:") if weeks else "")
        + ((str(days) + "d:") if days else "")
        + ((str(hours) + "h:") if hours else "")
        + ((str(minutes) + "m:") if minutes else "")
        + ((str(seconds) + "s") if seconds else "")
    )
    if result.endswith(":"):
        return result[:-1]
    return result
