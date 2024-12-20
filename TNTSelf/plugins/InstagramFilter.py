from TNTSelf import client
from PIL import Image
import pilgram
import os

FILTERS = {
    "1977": pilgram._1977,
    "aden": pilgram.aden,
    "brannan": pilgram.brannan,
    "brooklyn": pilgram.brooklyn,
    "clarendon": pilgram.clarendon,
    "earlybird": pilgram.earlybird,
    "gingham": pilgram.gingham,
    "hudson": pilgram.hudson,
    "inkwell": pilgram.inkwell,
    "kelvin": pilgram.kelvin,
    "lark": pilgram.lark,
    "lofi": pilgram.lofi,
    "maven": pilgram.maven,
    "mayfair": pilgram.mayfair,
    "moon": pilgram.moon,
    "nashville": pilgram.nashville,
    "perpetua": pilgram.perpetua,
    "reyes": pilgram.reyes,
    "rise": pilgram.rise,
    "slumber": pilgram.slumber,
    "stinson": pilgram.stinson,
    "toaster": pilgram.toaster,
    "valencia": pilgram.valencia,
    "walden": pilgram.walden,
    "willow": pilgram.willow,
    "xpro2": pilgram.xpro2,
}

__INFO__ = {
    "Category": "Convert",
    "Name": "Instagram Filter",
    "Info": {
        "Help": "To Add Instagram Filters To Photo!",
        "Commands": {
            "{CMD}SF<Filter>": {
                "Help": "To Add Filter",
                "Input": {
                    "<Filter>": "Name Of Filter",
                },
                "Vars": [fil.title() for fil in FILTERS]
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "filter": "**{STR} The Instagram Filter** ( `{}` ) **Added To Your Photo!**"
}

CMDS = ""
for filter in FILTERS:
    CMDS += filter.title() + "|"
CMDS = CMDS[:-1]

@client.Command(command=f"SF({CMDS})")
async def filterinphoto(event):
    await event.edit(client.STRINGS["wait"])
    mode = str(event.pattern_match.group(1).lower())
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = client.PATH + f"FilterPhoto-{str(mode)}.jpg"
    img = Image.open(photo)
    funct = FILTERS[mode]
    funct(img).save(newphoto)
    await client.send_file(event.chat_id, newphoto, caption=client.getstrings(STRINGS)["filter"].format(mode.title()))        
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()