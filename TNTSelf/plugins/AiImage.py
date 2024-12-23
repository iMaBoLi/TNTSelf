from TNTSelf import client
from somnium import Somnium
from telethon.tl.types import InputMediaWebPage

STYLES = Somnium.Styles()
STYLES = [:50]

__INFO__ = {
    "Category": "Tools",
    "Name": "Ai Image",
    "Info": {
        "Help": "To Create Image For Your Prompt White Beautiful Styles!",
        "Commands": {
            "{CMD}SStyles <Style-Name>": {
                "Help": "To Set Style Model",
                "Vars": [style for style in STYLES],
            },
            "{CMD}GenPhoto <Prompt>": {
                "Help": "To Generating Photo",
                "Input": {
                    "<Prompt>": "Your Prompt For Generate Photo",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notid": "**{STR} The Image Style** ( `{}` ) **Is Not Available!**",
    "setid": "**{STR} The Image Style Was Set To** ( `{}` )",
    "styles": "**{STR} The Image Styles:**\n\n",
    "notsetid": "**{STR} The Image Style Is Not Saved!**",
    "generating": "**{STR} Generating Image For Prompt** ( `{}` ) **...**\n\n**{STR} Style:** ( `{}` )",
    "caption": "**{STR} The Image For Prompt** ( `{}` ) **Was Generated!**\n\n**{STR} Style:** ( `{}` )",
}

@client.Command(command="SStyle (.*)")
async def setstyle(event):
    await event.edit(client.STRINGS["wait"])
    stylename = event.pattern_match.group(1)
    if stylename not in STYLES:
        return await event.edit(client.getstrings(STRINGS)["notid"].format(stylename))
    event.client.DB.set_key("STYLE_IMAGE", stylename)
    await event.edit(client.getstrings(STRINGS)["setid"].format(stylename))

@client.Command(command="GenPhoto (.*)")
async def generatephoto(event):
    await event.edit(client.STRINGS["wait"])
    stylename = event.client.DB.get_key("STYLE_IMAGE")
    if not stylename:
        return await event.edit(client.getstrings(STRINGS)["notsetid"])
    event.client.loop.create_task(generate(event))

async def generate(event):
    prompt = str(event.pattern_match.group(1))
    stylename = event.client.DB.get_key("STYLE_IMAGE")
    styleid = STYLES[stylename]
    await event.edit(client.getstrings(STRINGS)["generating"].format(prompt, stylename))
    file = Somnium.Generate(prompt, int(styleid))
    caption = client.getstrings(STRINGS)["caption"].format(prompt, stylename)
    await event.client.send_file(event.chat_id, file, caption=caption)
    await event.delete()