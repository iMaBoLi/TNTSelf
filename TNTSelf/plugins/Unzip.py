from TNTSelf import client
from zipfile import ZipFile
import os

__INFO__ = {
    "Category": "Tools",
    "Name": "Unzip",
    "Info": {
        "Help": "To Unzip Your Zip Files And Send Files!",
        "Commands": {
            "{CMD}Unzip": {
                "Help": "To Unzip Your Zip",
                "Reply": ["Zip File"]
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "unziping": "**{STR} Unziping Your Zip File ...**",
    "sending": "**{STR} Sending Your Extracted Zip Files ...**\n**{STR} Count:** ( `{}` )",
    "caption": "**{STR} File Location:** ( `{}` )",
}

@client.Command(command="Unziipp")
async def unzip(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["File"]):
        return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    client.loop.create_task(unzipfile(event))

async def unzipfile(event):
    callback = event.progress(download=True)
    zfile = client.PATH + "MainZip.zip"
    await event.reply_message.download_media(zfile, progress_callback=callback)
    await event.edit(client.getstrings(STRINGS)["unziping"])
    zipObj = ZipFile(zfile)
    zipObj.extractall(client.PATH)
    zipObj.close()
    zippath = client.PATH + "Zip/"
    files = [os.path.join(dirpath, file) for (dirpath, dirnames, filenames) in os.walk(zippath) for file in filenames]
    await event.edit(client.getstrings(STRINGS)["sending"].format(len(files)))
    for file in files:
        callback = event.progress(upload=True)
        caption = client.getstrings(STRINGS)["caption"].format(file)
        await client.send_file(event.chat_id, file, caption=caption, progress_callback=callback)
    os.remove(zfile)
    await client.functions.runcmd(f"rm -rf {zippath}")
    await event.delete()