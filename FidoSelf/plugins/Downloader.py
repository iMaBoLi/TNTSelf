from FidoSelf import client
import os

__INFO__ = {
    "Category": "Tools",
    "Name": "Download",
    "Info": {
        "Help": "To Download File From Your Links!",
        "Commands": {
            "{CMD}SFile <Name>:<Link>": {
                "Help": "To Download File",
                "Input": {
                    "<Name>": "Name Of File",
                    "<Link>": "Link Of File",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "downloading": "**{STR} Downloading File From Your Link ...**\n\n**{STR} Link:** ( `{}` )\n\n**{STR} FileName:** ( `{}` )",
    "errordown": "**{STR} Downloading File Is Not Completed!**\n\n**{STR} Error:** ( `{}` )",
    "caption": "**{STR} Link:** ( `{}` )\n\n**{STR} FileName:** ( `{}` )",
}

@client.Command(command="SFile (.*) (.*)")
async def downloadfile(event):
    await event.edit(client.STRINGS["wait"])
    filename = event.pattern_match.group(1)
    link = event.pattern_match.group(2)
    await event.edit(client.getstrings(STRINGS)["downloading"].format(link, filename))
    filepath = client.PATH + filename
    cmd = f"curl {link} -o {filepath}"
    result, error = await client.functions.runcmd(cmd)
    if error:
        await event.edit(client.getstrings(STRINGS)["errordown"].format(error))
    if os.path.exists(filepath):
        caption = client.getstrings(STRINGS)["caption"].format(link, filename)
        callback = event.progress(upload=True)
        uploadfile = await client.fast_upload(filepath, progress_callback=callback)
        await client.send_file(event.chat_id, uploadfile, caption=caption)        
        os.remove(filepath)