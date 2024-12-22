from TNTSelf import tlclient
from TNTSelf.events.Command import Command
from TNTSelf.events.Callback import Callback
from TNTSelf.events.Inline import Inline
from TNTSelf.functions.strings import STRINGS
import os
import time
import jdatetime

def AddVarsToClient():
    setattr(client, "STRINGS", STRINGS)
    setattr(client, "HELP", {})
    setattr(client, "MAX_SIZE", 500000000)
    setattr(client, "PATH", "downloads/")
    
    setattr(client, "Command", Command)
    setattr(client, "Callback", Callback)
    setattr(client, "Inline", Inline)

    os.environ["TZ"] = "Asia/Tehran"
    time.tzset()
    jdatetime.set_locale("fa_IR")