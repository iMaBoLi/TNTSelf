from FidoSelf import client
import asyncio
import subprocess
import json
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
            "{CMD}UPFilebin": {
                 "Help": "To Upload On FileBin",
                "Reply": ["Media"],
            },
            "{CMD}UPAnon": {
                 "Help": "To Upload On AnonFiles",
                "Reply": ["Media"],
            },
            "{CMD}UPTransfer": {
                 "Help": "To Upload On Transfer",
                "Reply": ["Media"],
            },
            "{CMD}UPAnonymous": {
                 "Help": "To Upload On AnonymousFiles",
                "Reply": ["Media"],
            },
            "{CMD}UPBay": {
                 "Help": "To Upload On BayFiles",
                "Reply": ["Media"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "uploading": "**{STR} Trying Upload File To Site** ( `{}` )",
    "errorupload": "**{STR} The File Is Not Uploaded To Site** ( `{}` )\n\n**{STR} Error:** ( `{}` )",
    "notfound": "**{STR} The Upload File Links Is Not Finded!**",
    "uploadlinks": "**{STR} The File Uploaded To Site** ( `{}` )\n\n**{STR} Upload Link:** ( {} )",
}

@client.Command(command="UP(Fileio|Filebin|Anon|Transfer|Anonymous|Bay|VShare)")
async def uploadsites(event):
    await event.edit(client.STRINGS["wait"])
    site = event.pattern_match.group(1).title()
    if not event.reply_message or not event.reply_message.file:
        return await event.edit(client.STRINGS["replymedia"])
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    file = await client.fast_download(event.reply_message, progress_callback=callback)
    await event.edit(client.getstrings(STRINGS)["uploading"].format(site))
    filename = os.path.basename(file)
    WEBS = {
        "fileio": 'curl -F "file=@{filepath}" https://file.io',
        "anon": 'curl -F "file=@{filepath}" https://api.anonfiles.com/upload',
        "transfer": 'curl --upload-file "{filepath}" https://transfer.sh/' + filename,
        "filebin": 'curl -X POST --data-binary "@{filepath}" -H "filename: {filename}" "https://filebin.net"',
        "anonymous": 'curl -F "file=@{filepath}" https://api.anonymousfiles.io/',
        "vshare": 'curl -F "file=@{filepath}" https://api.vshare.is/upload',
        "bay": 'curl -F "file=@{filepath}" https://bayfiles.com/api/upload',
    }
    cmd = WEBS[site.lower()]
    cmd = cmd.format(filepath=file, filename=filename)
    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    response = stdout.decode().strip()
    error = stdout.decode().strip()
    if not response:
        return await event.edit(client.getstrings(STRINGS)["errorupload"].format(site, error))
    response = json.dumps(json.loads(response), sort_keys=True, indent=4)
    linkregex = re.compile("((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)", re.DOTALL)
    urls = re.findall(linkregex, response)
    if not urls:
        return await event.edit(client.getstrings(STRINGS)["notfound"])
    links = ""
    for url in urls:
        links += f"`{url[0]}` - "
    links = links[:-3]
    text = client.getstrings(STRINGS)["uploadlinks"].format(links)
    await event.edit(text)
    os.remove(file)