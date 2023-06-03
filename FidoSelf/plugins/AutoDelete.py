from FidoSelf import client
import asyncio

@client.Command(command="SetAutoDeleteSleep (\d*)")
async def setautodeletesleep(event):
    await event.edit(client.get_string("Wait"))
    sleep = event.pattern_match.group(1)
    sleep = int(sleep) * 60
    client.DB.set_key("AUTO_DELETE_SLEEP", sleep)
    await event.edit(client.get_string("AutoDelete_2").format(client.utils.convert_time(sleep)))

@client.Command(alowedits=False)
async def autodeletes(event):
    if event.is_cmd: return
    client.loop.create_task(trydelete(event))

async def trydelete(event):
    mode = client.DB.get_key("AUTO_DELETE_MODE")
    if mode == "off": return
    sleep = client.DB.get_key("AUTO_DELETE_SLEEP") or 300
    await asyncio.sleep(int(sleep))
    try:
        await event.delete()
    except:
        pass