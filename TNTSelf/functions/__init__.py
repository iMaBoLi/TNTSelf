from TNTSelf import client
from TNTSelf.events.Command import Command
from TNTSelf.events.Callback import Callback
from TNTSelf.events.Inline import Inline
from TNTSelf.functions.database import *
from TNTSelf.functions.helper import *
from TNTSelf.functions.utils import *
from TNTSelf.functions.core import *
from TNTSelf.functions.tools import *
from TNTSelf.functions.youtube import *
from TNTSelf.functions.strings import *
from TNTSelf.functions.data import *
from TNTSelf.functions.fasttelethon import *
import os
import time
import jdatetime

def add_vars():
    setattr(client, "DB", DATABASE(0))
    setattr(client, "STRINGS", STRINGS)
    setattr(client, "getstrings", getstrings)
    setattr(client, "COMMANDS", [])
    setattr(client, "HELP", {})
    setattr(client, "MAX_SIZE", 500000000)
    for sinclient in client.clients:
        setattr(sinclient, "fast_download", download_file)
        setattr(sinclient, "fast_upload", upload_file)
    MAINPATH = "downloads/"
    if not os.path.exists(MAINPATH):
        os.mkdir(MAINPATH)
    setattr(client, "MAINPATH", MAINPATH)
    for sinclient in client.clients:
        PATH = MAINPATH + str(sinclient.me.id) + "/"
        if not os.path.exists(PATH):
            os.mkdir(PATH)
        setattr(sinclient, "PATH", PATH)
    
    setattr(client, "Command", Command)
    setattr(client, "Callback", Callback)
    setattr(client, "Inline", Inline)

    os.environ["TZ"] = "Asia/Tehran"
    time.tzset()
    jdatetime.set_locale("fa_IR")