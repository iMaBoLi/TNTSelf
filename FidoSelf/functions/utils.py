from FidoSelf import client
from traceback import format_exc
from importlib import import_module
import asyncio
import shlex
import math
import glob
import random
import os

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

def reverse(mylist):
    result = []
    for element in mylist:
        if isinstance(element, list):
            result.append(list(reversed(element)))
        else:
            result.append(element)
    return result

def load_plugins(folder):
    files = sorted(glob.glob(f"{folder}/*.py"))
    for file in files:
        try:
            filename = file.replace("/", ".").replace(".py" , "")
            load = import_module(filename)
            LOADED_PLUGS.append(os.path.basename(file))
        except:
            NOT_LOADED_PLUGS.update({os.path.basename(file): format_exc()})

def convert_bytes(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s%s" % (s, size_name[i])

def convert_time(seconds):
    if int(seconds) == 0:
        return "0s"
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
