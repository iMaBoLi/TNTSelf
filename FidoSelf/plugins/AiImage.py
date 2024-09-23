from FidoSelf import client
from somnium import Somnium
from telethon.tl.types import InputMediaWebPage

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
    "notid": "**{STR} The Image Style** ( `{}` ) **Is Not Available!**",
    "setid": "**{STR} The Image Style Id Was Set To** ( `{}` )",
    "styles": "**{STR} The Styles Name And ID:**\n\n",
    "notsetid": "**{STR} The Style Id Is Not Available!**",
    "generating": "**{STR} Generating Image For Prompt** ( `{}` ) **...**\n\n**{STR} Style:** ( `{}` )",
    "caption": "**{STR} The Ai Image For Prompt** ( `{}` ) **Was Created!**\n\n**{STR} Style:** ( `{}` )",
}

STYLES = Somnium.Styles()

@client.Command(command="SStyle (.*)")
async def setstyle(event):
    await event.edit(client.STRINGS["wait"])
    stylename = event.pattern_match.group(1)
    if stylename not in STYLES:
        return await event.edit(client.getstrings(STRINGS)["notid"].format(stylename))
    client.DB.set_key("STYLE_IMAGE", stylename)
    await event.edit(client.getstrings(STRINGS)["setid"].format(stylename))

@client.Command(command="GStyles")
async def getstyles(event):
    await event.edit(client.STRINGS["wait"])
    text = client.getstrings(STRINGS)["styles"]
    count = 1
    for style in STYLES:
        sid = STYLES[style]
        text += f"**{count} -** `{style}`\n"
        count += 1
    await event.edit(text)

@client.Command(command="GPhoto (.*)")
async def generatephoto(event):
    await event.edit(client.STRINGS["wait"])
    stylename = client.DB.get_key("STYLE_IMAGE")
    if not stylename:
        return await event.edit(client.getstrings(STRINGS)["notsetid"])
    client.loop.create_task(generate(event))

async def generate(event):
    prompt = str(event.pattern_match.group(1))
    stylename = client.DB.get_key("STYLE_IMAGE")
    styleid = STYLES[stylename]
    await event.edit(client.getstrings(STRINGS)["generating"].format(prompt, stylename))
    file = Somnium.Generate(prompt, int(styleid))
    caption = client.getstrings(STRINGS)["caption"].format(prompt, stylename)
    await client.send_file(event.chat_id, file, caption=caption)
    await event.delete()