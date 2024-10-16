from FidoSelf import client
from somnium import Somnium
from telethon.tl.types import InputMediaWebPage

__INFO__ = {
    "Category": "Tools",
    "Name": "Ai Image",
    "Info": {
        "Help": "To Create Image For Your Prompt White Beautiful Styles!",
        "Commands": {
            "{CMD}SStyles <Style-Name>": {
                "Help": "To Set Style Model",
            },
            "{CMD}GStyles": {
                "Help": "To Get Styles",
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
    "EN": {
        "notid": "**{STR} The Image Style** ( `{}` ) **Is Not Available!**",
        "setid": "**{STR} The Image Style Was Set To** ( `{}` )",
        "styles": "**{STR} The Image Styles:**\n\n",
        "notsetid": "**{STR} The Image Style Is Not Saved!**",
        "generating": "**{STR} Generating Image For Prompt** ( `{}` ) **...**\n\n**{STR} Style:** ( `{}` )",
        "caption": "**{STR} The Image For Prompt** ( `{}` ) **Was Generated!**\n\n**{STR} Style:** ( `{}` )",
    },
    "FA": {
        "notid": "**{STR} استایل عکس** ( `{}` ) **موجود نمی باشد!**",
        "setid": "**{STR} استایل عکس بر روی** ( `{}` ) **ذخیره شد!**",
        "styles": "**{STR} استایل های عکس:**\n\n",
        "notsetid": "**{STR} استایل برای عکس ذخیره نشده است!**",
        "generating": "**{STR} در حال ساخت عکس برای** ( `{}` ) **...**\n\n**{STR} استایل:** ( `{}` )",
        "caption": "**{STR} عکس برای** ( `{}` ) **با موفقیت ساخته شد!**\n\n**{STR} استایل:** ( `{}` )",
    },
}

STYLES = Somnium.Styles()

@client.Command(command="SStyle (.*)")
async def setstyle(event):
    await event.edit(client.STRINGS["wait"])
    stylename = event.pattern_match.group(1)
    if stylename not in STYLES[:48]:
        return await event.edit(client.getstring(STRINGS, "notid").format(stylename))
    client.DB.set_key("STYLE_IMAGE", stylename)
    await event.edit(client.getstring(STRINGS, "setid").format(stylename))

@client.Command(command="GStyles")
async def getstyles(event):
    await event.edit(client.STRINGS["wait"])
    text = client.getstring(STRINGS, "styles")
    count = 1
    for style in STYLES[:48]:
        sid = STYLES[style]
        text += f"**{count} -** `{style}`\n"
        count += 1
    await event.edit(text)

@client.Command(command="GenPhoto (.*)")
async def generatephoto(event):
    await event.edit(client.STRINGS["wait"])
    stylename = client.DB.get_key("STYLE_IMAGE")
    if not stylename:
        return await event.edit(client.getstring(STRINGS, "notsetid"))
    client.loop.create_task(generate(event))

async def generate(event):
    prompt = str(event.pattern_match.group(1))
    stylename = client.DB.get_key("STYLE_IMAGE")
    styleid = STYLES[stylename]
    await event.edit(client.getstring(STRINGS, "generating").format(prompt, stylename))
    file = Somnium.Generate(prompt, int(styleid))
    caption = client.getstring(STRINGS, "caption").format(prompt, stylename)
    await client.send_file(event.chat_id, file, caption=caption)
    await event.delete()