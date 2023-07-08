from FidoSelf import client

__INFO__ = {
    "Category": "Setting",
    "Name": "Reload",
    "Info": {
        "Help": "To Reload Your Self!",
        "Commands": {
            "{CMD}Reload": {
                "Help": "To Reload Self",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "reload": "**{STR} The Self Was Reloading ...**",
}

RUNCMD = "python3 -m FidoSelf"

@client.Command(command="Reload")
async def reloadself(event):
    await event.edit(client.STRINGS["wait"])
    await event.edit(client.getstrings(STRINGS)["reload"])
    await client.functions.runcmd(RUNCMD)