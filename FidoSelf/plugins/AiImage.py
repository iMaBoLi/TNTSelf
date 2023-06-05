from FidoSelf import client
import os
os.system("pip install somnium")
from somnium import Somnium

@client.Command(command="Gen (.*)")
async def gen_img(event):
    query = event.pattern_match.group(1)
    await event.edit(client.STRINGS["wait"])
    styleid = 84
    file = Somnium.Generate(query, styleid)
    await client.send_file(
        event.chat_id,
        file,
        force_document=True,
    )
    await event.delete()