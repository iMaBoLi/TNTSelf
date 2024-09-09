from FidoSelf import client
import os
import re

__INFO__ = {
    "Category": "Tools",
    "Name": "Upload Site",
    "Info": {
        "Help": "To Upload Your Files In Upload Sites!",
        "Commands": {
            "{CMD}UPFileio": {
                 "Help": "To Upload On Fileio",
                "Reply": ["Media"],
            },
            "{CMD}UPX0at": {
                 "Help": "To Upload On X0at",
                "Reply": ["Media"],
            },
            "{CMD}UPTransfer": {
                 "Help": "To Upload On Transfer",
                "Reply": ["Media"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "uploading": "**{STR} Trying Upload File To Site** ( `{}` ) **...**",
    "uploadlink": "**{STR} The File Uploaded To Site** ( `{}` )\n\n**{STR} Upload Link:** ( `{}` )",
}

@client.Command(command="UP(Fileio|X0at|Transfer)")
async def uploadsites(event):
    await event.edit(client.STRINGS["wait"])
    uploadsite = event.pattern_match.group(1)
    if not event.reply_message or not event.reply_message.file:
        return await event.edit(client.STRINGS["replymedia"])
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    file = await client.fast_download(event.reply_message, progress_callback=callback)
    await event.edit(client.getstrings(STRINGS)["uploading"].format(uploadsite.title()))
    SITES = {
        "fileio": {"url": "https://file.io", "json": True},
        "x0at": {"url": "https://x0.at/", "json": False},
        "transfer": {"url": "https://transfer.sh", "json": False},
    }
    upsite = uploadsite.lower()
    url = SITES[upsite]["url"]
    opfile = open(file, "rb").read()
    result = await client.functions.request(url, data={"file": opfile}, post=True, re_json=SITES[upsite]["json"])
    if upsite in ["x0at", "transfer"]:
        link = result
    elif upsite == "fileio":
        link = result["link"]
    text = client.getstrings(STRINGS)["uploadlink"].format(uploadsite.title(), link)
    await event.edit(text)
    os.remove(file)