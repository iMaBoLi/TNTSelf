from FidoSelf import client
from somnium import Somnium

__INFO__ = {
    "Category": "Tools",
    "Plugname": "ai Image",
    "Pluginfo": {
        "Help": "Create Image For Your Text White Beautiful Styles!",
        "Commands": {
            "{CMD}CPhoto '<StyleID>' <Text>": None,
            "{CMD}GStyles": "To Get StylesID For Create Images!",
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "gen": "**Creating Image For Query** ( `{}` ) **And StyleID** ( `{}` ) **...**",
    "caption": "**The Image For Query** ( `{}` ) **And StyleID** ( `{}` ) **Created!**",
    "styles": "**The Styles For Creating Photo:** ( {} )\n\n**Use From StylesID For Create Photos!**",
}

@client.Command(command="CPhoto \'(\d*)\' (.*)")
async def generatephoto(event):
    await event.edit(client.STRINGS["wait"])
    client.loop.create_task(generate(event))
    
async def generate(event):
    style = event.pattern_match.group(1)
    query = event.pattern_match.group(2)
    await event.edit(STRINGS["gen"].format(query, style))
    file = Somnium.Generate(query, style)
    caption = STRINGS["caption"].format(query, style)
    await client.send_file(event.chat_id, file, caption=caption)
    await event.delete()
    
@client.Command(command="GStyles")
async def getstyles(event):
    await event.edit(client.STRINGS["wait"])
    link = "https://graph.org/List-Of-Styles-06-05"
    await event.edit(STRINGS["styles"].format(link))