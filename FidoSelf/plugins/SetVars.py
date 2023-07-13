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
            "{CMD}DelCmd": {
                "Help": "To Delete Cmd",
                "Note": "Command Starter Set To Default ( `.` )",
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
    "setcmd": "**{STR} The Command Starter Was Set To:** ( `{}` )\n\n**{STR} Reloading ...**",
    "delcmd": "**{STR} The Command Starter Was Deleted And Set To:** ( `{}` )\n\n**{STR} Reloading ...**",
    "setsim": "**{STR} The Simbel For Texts Was Set To:** ( `{}` )",
}

RUNCMD = "python3 -m FidoSelf"

@client.Command(command="SetCmd (.*)")
async def cmdstarter(event):
    await event.edit(client.STRINGS["wait"])
    simbel = event.pattern_match.group(1)
    client.DB.set_key("CMD_SIMBEL", simbel)
    await event.edit(client.getstrings(STRINGS)["setcmd"].format(simbel))
    await client.functions.runcmd(RUNCMD)

@client.Command(pattern="(?i)^\.DelCmd$")
async def delcmdstarter(event):
    await event.edit(client.STRINGS["wait"])
    client.DB.set_key("CMD_SIMBEL", ".")
    await event.edit(client.getstrings(STRINGS)["delcmd"].format("."))
    await client.functions.runcmd(RUNCMD)

@client.Command(command="SetSimbel (.*)")
async def simbeltexts(event):
    await event.edit(client.STRINGS["wait"])
    simbel = event.pattern_match.group(1)
    client.DB.set_key("EMOJI_SIMBEL", simbel)
    await event.edit(client.getstrings(STRINGS)["setsim"].format(simbel))