from FidoSelf import client
from telethon.types import Message
from aiohttp import ClientSession
import time

async def file_download(event, downloadurl, filename=None):
    if not filename:
        filename = downloadurl.split("/")[-1]
    async with ClientSession() as session:
        async with session.get(downloadurl, timeout=None) as response:
            total_size = int(response.headers.get("content-length", 0)) or 0
            downloaded_size = 0
            start_time = time.time()
            with open(filename, "wb") as ffile:
                async for chunk in response.content.iter_chunked(1024):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        if total_size and downloaded_size:
                            event.progress(current=downloaded_size, total=total_size, download=True)
            return filename
            
setattr(Message, "file_download", file_download)
setattr(client, "file_download", file_download)