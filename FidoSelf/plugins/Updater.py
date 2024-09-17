from FidoSelf import client
import shutil, glob, os

STRINGS = {
    "complete": "**{STR} Successfuly Updated And Restarting ...**"
}

@client.Command(command="Update")
async def update(event):
    await event.edit(client.STRINGS["wait"])
    git = client.functions.Git()
    link = git.repo.get_archive_link("zipball", "master")
    await client.functions.runcmd(f"curl {link} -o Fido.zip")
    await client.functions.runcmd("unzip Fido.zip -d ../")
    path = glob.glob("../iMaBoLi*")[0]
    os.rename(path, "../app")
    await event.edit(client.getstrings(STRINGS)["complete"])
    os.remove("Fido.zip")
    await client.functions.runcmd("python3 -m FidoSelf")