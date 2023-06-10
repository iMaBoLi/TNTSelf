from FidoSelf import client
from FidoSelf.functions.github import Git
import aiocron
import time
import os

@aiocron.crontab("*/1 * * * *")
async def updater():
    git = Git()
    file = "__Mogenius__"
    start = client.START_TIME
    end = time.time()
    timer = round(end - start)
    if timer > 14000:
        if os.path.exists(file):
            return git.delete(file)
        content = "#FidoSelf"
        git.create(file, content)