from FidoSelf import client
import requests
import os

__INFO__ = {
    "Category": "Tools",
    "Name": "Download",
    "Info": {
        "Help": "To Download File From Your Links!",
        "Commands": {
            "{CMD}DVideo <Link>": {
                "Help": "To Download Video",
                "Input": {
                    "<Link>": "Link Of Video",
                },
            },
            "{CMD}DMusic <Link>": {
                "Help": "To Download Music",
                "Input": {
                    "<Link>": "Link Of Music",
                },
            },
            "{CMD}DPhoto <Link>": {
                "Help": "To Download Photo",
                "Input": {
                    "<Link>": "Link Of Photo",
                },
            },
            "{CMD}DTxt <Link>": {
                "Help": "To Download Txt File",
                "Input": {
                    "<Link>": "Link Of Txt File",
                },
            },
            "{CMD}DApk <Link>": {
                "Help": "To Download Apk",
                "Input": {
                    "<Link>": "Link Of Apk",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "downloading": "**{STR} Downloading {} From Your Link ...**\n\n**{STR} Link:** ( `{}` )\n\n**{STR} FileName:** ( `{}` )",
    "errordown": "**{STR} Downloading {} Is Not Completed!**\n\n**{STR} Error:** ( `{}` )",
    "notdown": "**{STR} The {} Is Not Downloaded!**\n\n**{STR} Link:** ( `{}` )",
    "caption": "**{STR} Link:** ( `{}` )\n\n**{STR} FileName:** ( `{}` )",
}

@client.Command(command="D(Video|Music|Photo|Txt|Apk) (.*)")
async def downloadfile(event):
    await event.edit(client.STRINGS["wait"])
    dtype = event.pattern_match.group(1).title()
    link = event.pattern_match.group(2)
    TYPES = {
        "Video": ".mp4",
        "Music": ".mp3",
        "Photo": ".jpg",
        "Txt": ".txt",
        "Apk": ".apk",
    }
    filename = link.split("/")[-1]
    filename = filename + TYPES[dtype]
    await event.edit(client.getstrings(STRINGS)["downloading"].format(dtype, link, filename))
    filepath = client.PATH + filename
    try:
        resp = requests.get(link)
        filesize = resp.headers["content-length"]
    except Exception as error:
        return await event.edit(client.getstrings(STRINGS)["errordown"].format(dtype, error))
    if int(filesize) > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    cmd = f"curl {link} -o {filepath}"
    await client.functions.runcmd(cmd)
    if not os.path.exists(filepath):
        return await event.edit(client.getstrings(STRINGS)["notdown"].format(dtype, link))
    caption = client.getstrings(STRINGS)["caption"].format(link, filename)
    callback = event.progress(upload=True)
    uploadfile = await client.fast_upload(filepath, progress_callback=callback)
    await client.send_file(event.chat_id, uploadfile, caption=caption)        
    os.remove(filepath)
    await event.delete()