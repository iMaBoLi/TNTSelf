from FidoSelf import client
from somnium import Somnium

__INFO__ = {
    "Category": "Tools",
    "Name": "Ai Image",
    "Info": {
        "Help": "To Create Image For Your Text White Beautiful Styles!",
        "Commands": {
            "{CMD}CPhoto <Style>,<Text>": {
                "Help": "To Create Photo",
                "Input": {
                    "<Style>": "Style Id ( Get From Styles )",
                    "<Text>": "Your Text For Create Photo",
                },
            },
            "{CMD}GStyles": {
                "Help": "To Get Styles",
            }
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "generating": "**{STR} Creating Image For** ( `{}` ) **And Style** ( `{}` ) **...**",
    "caption": "**{STR} The Image For** ( `{}` ) **And Style** ( `{}` ) **Created!**",
    "styles": "**{STR} The Styles For Creating Photo:**\n\n( {} )"
}

@client.Command(command="CPhoto (\d*),(.*)")
async def generatephoto(event):
    await event.edit(client.STRINGS["wait"])
    client.loop.create_task(generate(event))
    
async def generate(event):
    style = int(event.pattern_match.group(1))
    query = str(event.pattern_match.group(2))
    await event.edit(client.getstrings(STRINGS)["generating"].format(query, style))
    file = Somnium.Generate(query, style)
    caption = client.getstrings(STRINGS)["caption"].format(query, style)
    await client.send_file(event.chat_id, file, caption=caption)
    await event.delete()
    
@client.Command(command="GStyles")
async def getstyles(event):
    await event.edit(client.STRINGS["wait"])
    link = "https://graph.org/List-Of-Styles-06-05"
    await event.edit(client.getstrings(STRINGS)["styles"].format(link))