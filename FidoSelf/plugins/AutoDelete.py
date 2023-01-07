from FidoSelf import client
import asyncio

@client.Cmd(pattern=f"(?i)^\{client.cmd}AutoDelete (On|Off)$")
async def autodelete(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("AUTO_DELETE_MODE", mode)
    change = client.get_string("Change_1") if mode == "on" else client.get_string("Change_2")
    await event.edit(client.get_string("AutoDelete_1").format(change))

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetAutoDeleteSleep (\d*)$")
async def setautodeletesleep(event):
    await event.edit(client.get_string("Wait"))
    sleep = event.pattern_match.group(1)
    sleep = int(sleep) * 60
    client.DB.set_key("AUTO_DELETE_SLEEP", sleep)
    await event.edit(client.get_string("AutoDelete_2").format(client.utils.convert_time(sleep)))

@client.Cmd(edits=False)
async def autodeletes(event):
    if event.is_cmd: return
    mode = client.DB.get_key("AUTO_DELETE_MODE")
    if mode == "on":
        sleep = client.DB.get_key("AUTO_DELETE_SLEEP") or 300
        client.loop.create_task(delete(event, sleep))

async def delete(event, sleep):
    await asyncio.sleep(int(sleep))
    try:
        await event.delete()
    except:
        pass
