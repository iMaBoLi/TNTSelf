from FidoSelf.functions.github import Git
import aiocron
import random
from datetime import datetime

@aiocron.crontab("*/60 * * * *")
async def autoupdater():
    time = datetime.now().strftime("%H")
    if time == "00" or (int(time) % 3) == 0:
        git = Git()
        file = "FidoSelf/plugins/__MongoUpdater__"
        rand = random.randint(11111111, 99999999)
        text = f"# Auto Updater For Your Self!\n\n# Random Number Is: {str(rand)}\n\n# Good Luck!!"
        git.create(file, text)
        git.update(file, text)
