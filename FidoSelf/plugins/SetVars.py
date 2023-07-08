from FidoSelf import client

__INFO__ = {
    "Category": "Setting",
    "Name": "Command",
    "Info": {
        "Help": "To Setting Command Starter!",
        "Commands": {
            "{CMD}SetCmd <Text>": {
                "Help": "To Set Cmd",
                "Input": {
                    "<Text": "Command Starter",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)
__INFO__ = {
    "Category": "Setting",
    "Name": "Simbel",
    "Info": {
        "Help": "To Setting Simbel For Self Texts!",
        "Commands": {
            "{CMD}SetSimbel <Text>": {
                "Help": "To Set Simbel",
                "Input": {
                    "<Text": "Simbel Text",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "setcmd": "**{STR} The Command Starter Has Been Set To:** ( `{}` )",
    "setsim": "**{STR} The Simbel For Texts Has Been Set To:** ( `{}` )",
}

@client.Command(command="SetCmd (.*)")
async def cmdstarter(event):
    await event.edit(client.STRINGS["wait"])
    simbel = event.pattern_match.group(1)
    client.DB.set_key("CMD_SIMBEL", simbel)
    await event.edit(client.getstrings(STRINGS)["setcmd"].format(simbel))

@client.Command(command="SetBSimbel (.*)")
async def simbeltexts(event):
    await event.edit(client.STRINGS["wait"])
    simbel = event.pattern_match.group(1)
    client.DB.set_key("EMOJI_SIMBEL", simbel)
    await event.edit(client.getstrings(STRINGS)["setsim"].format(simbel))