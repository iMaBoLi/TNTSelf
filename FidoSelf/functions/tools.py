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
    with open(filename, "wb") as file:
        file.write(response)
    return filename