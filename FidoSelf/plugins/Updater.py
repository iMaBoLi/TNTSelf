from FidoSelf import client
import shutil

STRINGS = {
    "update": "**The Plugin With Name** ( `{}` ) **Has Been Updated!**",
}

@client.Command(command="Update")
async def update(event):
    await event.edit(client.STRINGS["wait"])
    git = client.functions.Git()
    link = git.repo.get_archive_link("zipball", "DEV")
    await client.functions.runcmd(f"curl {link} -o Fido.zip")
    await client.functions.runcmd("unzip Fido.zip")
    shutil.rmtree("/app/FidoSelf/")
    shutil.copytree("/app/", "/app/FidoSelf/")
    await event.edit(STRINGS["update"].format(filename))