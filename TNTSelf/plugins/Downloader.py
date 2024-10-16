from TNTSelf import client
import requests
import os

__INFO__ = {
    "Category": "Tools",
    "Name": "Download",
    "Info": {
        "Help": "To Download File From Your Links!",
        "Commands": {
            "{CMD}Down <Format>|<Link>": {
                "Help": "To Download File",
                "Input": {
                    "<Format>": "Format Of File",
                    "<Link>": "Link Of Video",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "downloading": "**{STR} Downloading File From Your Link ...**\n\n**{STR} Link:** ( `{}` )\n\n**{STR} FileName:** ( `{}` )",
    "errordown": "**{STR} Downloading File Is Not Completed!**",
    "notdown": "**{STR} The File Is Not Downloaded!**\n\n**{STR} Link:** ( `{}` )",
    "caption": "**{STR} Link:** ( `{}` )\n\n**{STR} FileName:** ( `{}` )",
}

@client.Command(command="Down (.*)\\|(.*)")
async def downloadfile(event):
    await event.edit(client.STRINGS["wait"])
    dtype = event.pattern_match.group(1).lower()
    link = event.pattern_match.group(2)
    filename = link.split("/")[-1]
    filename = filename + "." + dtype
    await event.edit(client.getstrings(STRINGS)["downloading"].format(link, filename))
    filepath = client.PATH + filename
    try:
        resp = requests.get(link)
        filesize = resp.headers["content-length"]
    except:
        return await event.edit(client.getstrings(STRINGS)["errordown"])
    if int(filesize) > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    cmd = f"curl {link} -o {filepath}"
    await client.functions.runcmd(cmd)
    if not os.path.exists(filepath):
        return await event.edit(client.getstrings(STRINGS)["notdown"].format(link))
    caption = client.getstrings(STRINGS)["caption"].format(link, filename)
    callback = event.progress(upload=True)
    uploadfile = await client.fast_upload(filepath, progress_callback=callback)
    await client.send_file(event.chat_id, uploadfile, caption=caption)        
    os.remove(filepath)
    await event.delete()