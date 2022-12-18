from FidoSelf import client
from telethon import functions

@client.Cmd(pattern=f"(?i)^\{client.cmd}DelProfile ?(\-\d*)?$")
async def delprofiles(event):
    await event.edit(f"**{client.str} Processing . . .**")
    pphoto = await client.get_profile_photos("me")
    if not pphoto:
        return await event.edit(f"**{client.str} The Profile Photos Is Empty!**")
    prof = event.pattern_match.group(1)
    if not prof:
        pphoto = pphoto[0]
        await client(functions.photos.DeletePhotosRequest(id=[types.InputPhoto(id=pphoto.id, access_hash=pphoto.access_hash, file_reference=pphoto.file_reference)]))
        await event.edit(f"**{client.str} The Last Profile Photo Has Been Deleted!**")
    elif str(prof).startswith("-"):
        prof = prof.replace("-", "")
        if int(prof) > len(pphoto):
            prof = len(pphoto)
        for con in range(0, int(prof)):
            profs = pphoto[con]
            await client(functions.photos.DeletePhotosRequest(id=[types.InputPhoto(id=profs.id, access_hash=profs.access_hash, file_reference=profs.file_reference)]))
        await event.edit(f"**{client.str} The** ( `{str(prof)}` ) **Of Your Profile Photos Has Been Deleted!**")
    else:        
        if int(prof) > len(pphoto):
            return await event.edit(f"**{client.str} This Profile Photo Is Not Available!**")
        pphoto = pphoto[int(prof)-1]
        await client(functions.photos.DeletePhotosRequest(id=[types.InputPhoto(id=pphoto.id, access_hash=pphoto.access_hash, file_reference=pphoto.file_reference)]))
        await event.edit(f"**{client.str} The Profile Photo** ( `{str(prof)}` ) **Has Been Deleted!**")
