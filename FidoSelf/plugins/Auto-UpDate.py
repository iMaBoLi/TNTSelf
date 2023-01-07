from FidoSelf.functions.github import Git
import aiocron
import random

@aiocron.crontab("*/60 * * * *")
async def autoupdater():
    git = Git()
    file = "FidoSelf/plugins/__MongoUpdater__"
    rand = random.randint(11111111, 99999999)
    text = f"# Auto Updater For Your Self!\n\n# Random Number Is: {str(rand)}\n\n# Good Luck!!"
    open(file, "w").write(text)
    git.create(file, file)
    git.delete(file)
