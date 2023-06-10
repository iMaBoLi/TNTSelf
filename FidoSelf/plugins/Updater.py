from FidoSelf import client
from FidoSelf.functions.github import Git
import aiocron
import time

@aiocron.crontab("*/1 * * * *")
async def updater():
    git = Git()
    file = "__Mogenius__"
    start = client.START_TIME
    end = time.time()
    timer = round(end - start)
    if timer > 14100:
        content = "#Fido-Self"
        git.create(file, content)
        git.delete(file)