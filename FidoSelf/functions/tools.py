from FidoSelf import client
from aiohttp import ClientSession
from telethon.types import Message

async def request(url, post=False, head=False, headers=None, evaluate=None, object=False, re_json=False, re_content=False, *args, **kwargs,):
    async with ClientSession(headers=headers) as CSession:
        method = CSession.head if head else (CSession.post if post else CSession.get)
        data = await method(url, *args, **kwargs)
        if evaluate:
            return await evaluate(data)
        if re_json:
            return await data.json()
        if re_content:
            return await data.read()
        if head or object:
            return data
        return await data.text()

async def file_download(event, downloadurl, filename=None):
    if not filename:
        filename = downloadurl.split("/")[-1]
    filename = client.PATH + filename
    response = await request(downloadurl, re_content=True)
    total = int(response.headers.get("content-length", 0)) or 0
    current = 0
    newtime = time.time()
    with open(filename, "wb") as file:
        async for chunk in response.iter_chunked(1024):
            if chunk:
                file.write(chunk)
                current += len(chunk)
                event.progress(current=current, total=total, newtime=newtime, download=True)
    return filename

setattr(Message, "file_download", file_download)
setattr(client, "file_download", file_download)