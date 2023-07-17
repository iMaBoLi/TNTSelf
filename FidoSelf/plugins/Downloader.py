from FidoSelf import client
import os

__INFO__ = {
    "Category": "Tools",
    "Name": "Download",
    "Info": {
        "Help": "To Download File From Your Links!",
        "Commands": {
            "{CMD}SFile <Link>": {
                "Help": "To Download File",
                "Input": {
                    "<Link>": "Link Of File",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "downloading": "**{STR} Downloading File From Your Link ...**\n\n**{STR} Link:** ( `{}` )\n**{STR} FileName:** ( `{}` )",
    "errordown": "**{STR} Downloading File Is Not Completed!**\n\n**{STR} Error:** ( `{}` )",
    "caption": "**{STR} Link:** ( `{}` )\n\n**{STR} FileName:** ( `{}` )",
}

@client.Command(command="SFile (.*)\,(.*)")
async def downloadfile(event):
    await event.edit(client.STRINGS["wait"])
    filename = event.pattern_match.group(1)
    link = event.pattern_match.group(2)
    await event.edit(client.getstrings(STRINGS)["downloading"].format(link, filename))
    filename = client.PATH + filename
    try:
        file = await client.functions.file_download(link, filename)
    except Exception as error:
        return await event.edit(client.getstrings(STRINGS)["errordown"].format(error))
    caption = client.getstrings(STRINGS)["caption"].format(link, file)
    callback = event.progress(upload=True)
    uploadfile = await client.fast_upload(file, progress_callback=callback)
    await client.send_file(event.chat_id, uploadfile, caption=caption)        
    os.remove(file)