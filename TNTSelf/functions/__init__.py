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
from TNTSelf.functions.fasttelethon import fast_updown
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
        setattr(sinclient, "fast", fast_updown(sinclient))
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
    
from github import Github
import base64

BRANCH = "master"

class Git:
    def __init__(self):
        self.gittoken = "Z2hwX0szY0lCc1JsbFptV0w0a0FPTXR2cVp1dUFIV0dPcDJjMmZkdw=="
        self.repo = "iMaBoLi/TNTSelf"
        self.token = base64.b64decode(token).decode('utf-8')
        self.git = Github(self.token)
        self.repo = self.git.get_repo(self.repo)

    def create(self, newfile, content, branch=BRANCH):
        try:
            self.repo.create_file(newfile, f"Create {newfile.split('/')[-1]}", content, branch=branch)
            return True
        except Exception as error:
            return error

    def update(self, file, content, branch=BRANCH):
        try:
            contents = self.repo.get_contents(file, ref=branch)
            self.repo.update_file(contents.path,  f"Update {file.split('/')[-1]}", content, contents.sha, branch=branch)
            return True
        except Exception as error:
            return error

    def delete(self, file, branch=BRANCH):
        try:
            contents = self.repo.get_contents(file, ref=branch)
            self.repo.delete_file(contents.path,  f"Remove {file.split('/')[-1]}", contents.sha, branch=branch)
            return True
        except Exception as error:
            return error