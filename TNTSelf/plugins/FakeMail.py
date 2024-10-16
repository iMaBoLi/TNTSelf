from TNTSelf import client

__INFO__ = {
    "Category": "Funs",
    "Name": "FakeMail",
    "Info": {
        "Help": "To Get Fake Email And Messages!",
        "Commands": {
            "{CMD}FakeMail": {
                "Help": "To Get Fake Email!",
            },
            "{CMD}GetMail <Session>": {
               "Help": "To Get Messages Of FakeMail",
                "Input": {
                    "<Session>" : "Session Of FakeMail"
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "mail": "**{STR} The Fake Email Was Created!**\n\n**{STR} Email:** ( `{}` )\n**{STR} Session:** ( `{}` )",
    "notmes": "**{STR} The Email For Session** ( `{}` ) **Is Not Founded!**",
    "message": "**{STR} The New Email Received!**\n**{STR} From:** ( `{}` )\n**{STR} Subject:** ( `{}` )\n\n`{}`",
}

@client.Command(command="FakeMail")
async def fmail(event):
    await event.edit(client.STRINGS["wait"])
    mail = client.functions.FakeEmail().Mail()
    myemail = mail["mail"]
    session = mail["session"]
    await event.edit(client.getstrings(STRINGS)["mail"].format(myemail, session))

@client.Command(command="GetMail (.*)")
async def mesfmail(event):
    await event.edit(client.STRINGS["wait"])
    session = str(event.pattern_match.group(1))
    inbox = client.functions.FakeEmail(session).inbox()
    if not inbox:
        return await event.edit(client.getstrings(STRINGS)["notmes"].format(session))
    topic = inbox["topic"]
    recemail = inbox["from"]
    message = inbox["message"]
    await event.edit(client.getstrings(STRINGS)["message"].format(recemail, topic, message))