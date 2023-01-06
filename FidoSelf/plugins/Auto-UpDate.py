from FidoSelf.functions.github import Git
import aiocron
import random

@aiocron.crontab("*/1 * * * *")
async def autoupdater():
    git = Git()
    file = "FidoSelf/plugins/__Updater__.py"
    rand = random.randint(11111, 99999)
    text = f"# Auto Updater For Your Self!\n\n# Random Number Is: {str(rand)}"
    open(file, "w").write(text)
    git.create(file, file)
    git.update(file, file)
