from FidoSelf import client
import os

@client.Command(command="SDown (.*)")
async def downloader(event):
    await event.edit(client.STRINGS["wait"])
    link = event.pattern_match.group(1)
    file = await event.file_download(link)
    await event.reply(file)
    #callback = event.progress(upload=True)
    #uploadfile = await client.fast_upload(file, progress_callback=callback)
    #await client.send_file(event.chat_id, uploadfile)        
    #os.remove(file)