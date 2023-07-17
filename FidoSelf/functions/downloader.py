from FidoSelf import client
from telethon.types import Message
from aiohttp import ClientSession
import time

async def file_download(event, downloadurl, filename=None):
    if not filename:
        filename = downloadurl.split("/")[-1]
    filename = client.PATH + filename
    async with ClientSession() as session:
        async with session.get(downloadurl, timeout=None) as response:
            total = int(response.headers.get("content-length", 0)) or 0
            current = 0
            newtime = time.time()
            with open(filename, "wb") as file:
                async for chunk in response.content.iter_chunked(1024):
                    if chunk:
                        file.write(chunk)
                        current += len(chunk)
                        if total and current:
                            event.progress(current=current, total=total, newtime=newtime, download=True)
            return filename
            
setattr(Message, "file_download", file_download)
setattr(client, "file_download", file_download)