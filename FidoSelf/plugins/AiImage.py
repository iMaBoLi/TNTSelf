from FidoSelf import client
from somnium import Somnium
from telethon.tl.types import InputMediaWebPage
from FidoSelf.functions import STYLES

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
        },1
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notid": "**{STR} The Image Style Id** ( `{}` ) **Is Not Available!**",
    "setid": "**{STR} The Image Style Id Was Set To** ( `{}` - `{}` )",
    "styles": "**{STR} The Styles Name And ID:**\n\n"
    "generating": "**{STR} Generating Image For Prompt** ( `{}` ) **...**\n\n**{STR} Style:** ( `{}` - `{}` )",
    "caption": "**{STR} The Ai Image For Prompt** ( `{}` ) **Was Created!**\n\n**{STR} Style:** ( `{}` - `{}` )",
}

@client.Command(command="SStyle (\\d*)")
async def setstyle(event):
    await event.edit(client.STRINGS["wait"])
    styleid = event.pattern_match.group(1)
    if str(styleid) not in STYLES:
        return await event.edit(client.getstrings(STRINGS)["notid"].format(styleid))
    client.DB.set_key("STYLEID_IMAGE", styleid)
    name = STYLES[str(styleid)]["Name"]
    link = STYLES[str(styleid)]["Link"]
    media = InputMediaWebPage(url=link)
    await event.respond(client.getstrings(STRINGS)["setid"].format(name, styleid), file=media)
    await event.delete()

@client.Command(command="GStyles")
async def getstyles(event):
    await event.edit(client.STRINGS["wait"])
    text = client.getstrings(STRINGS)["styles"]
    count = 1
    for style in STYLES:
        name = STYLES[style]["Name"]
        text += f"**{count} -** ( `{name}` ) [ `{style}` ]\n"
        count += 1
    await event.edit(text)

@client.Command(command="GPhoto ([\s\S]*)")
async def generatephoto(event):
    await event.edit(client.STRINGS["wait"])
    client.loop.create_task(generate(event))
    
async def generate(event):
    prompt = str(event.pattern_match.group(2))
    styleid = client.DB.get_key("STYLEID_IMAGE") or 1
    sname = STYLES[str(styleid)]["Name"]
    await event.edit(client.getstrings(STRINGS)["generating"].format(prompt, name, styleid))
    file = Somnium.Generate(prompt, int(styleid))
    caption = client.getstrings(STRINGS)["caption"].format(prompt, name, styleid)
    await client.send_file(event.chat_id, file, caption=caption)
    await event.delete()