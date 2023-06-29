from FidoSelf import client
from FidoSelf.functions.github import Git
import base64
import os

STRINGS = {
    "notfile": "**The Plugin With Name** ( `{}` ) **Is Not Available!**",
    "update": "**The Plugin With Name** ( `{}` ) **Has Been Updated!**",
}

@client.Command(command="Update (.*)")
async def update(event):
    await event.edit(client.STRINGS["wait"])
    filename = event.pattern_match.group(1)
    filename = "FidoSelf/plugins/" + filename + ".py"
    if not os.path.exists(filename):
        return await event.edit(STRINGS["notfile"].format(filename))
    content = Git().repo.get_contents(filename, ref="DEV")
    content = base64.b64decode(content.content).decode('utf-8')
    client.functions.remove_handlers(filename)
    open(filename, "w").write(content)
    client.functions.load_plugins([filename], reload=True)
    await event.edit(STRINGS["update"].format(filename))