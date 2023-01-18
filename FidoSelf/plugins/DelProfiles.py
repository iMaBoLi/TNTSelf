from FidoSelf import client
from telethon import functions, types

@client.Command(pattern=f"(?i)^\{client.cmd}DelProfile ?((\-)?\d*)?$")
async def delprofiles(event):
    await event.edit(client.get_string("Wait"))
    pphoto = await client.get_profile_photos("me")
    if not pphoto:
        return await event.edit(client.get_string("DelProfiles_1"))
    prof = event.pattern_match.group(1)
    if not prof:
        pphoto = pphoto[0]
        await client(functions.photos.DeletePhotosRequest(id=[types.InputPhoto(id=pphoto.id, access_hash=pphoto.access_hash, file_reference=pphoto.file_reference)]))
        await event.edit(client.get_string("DelProfiles_2"))
    elif str(prof).startswith("-"):
        prof = prof.replace("-", "")
        if int(prof) > len(pphoto):
            prof = len(pphoto)
        for con in range(0, int(prof)):
            profs = pphoto[con]
            await client(functions.photos.DeletePhotosRequest(id=[types.InputPhoto(id=profs.id, access_hash=profs.access_hash, file_reference=profs.file_reference)]))
        await event.edit(client.get_string("DelProfiles_3").format(prof))
    else:        
        if int(prof) > len(pphoto):
            return await event.edit(f"**{client.str} This Profile Photo Is Not Available!**")
        pphoto = pphoto[int(prof)-1]
        await client(functions.photos.DeletePhotosRequest(id=[types.InputPhoto(id=pphoto.id, access_hash=pphoto.access_hash, file_reference=pphoto.file_reference)]))
        await event.edit(client.get_string("DelProfiles_4").format(prof))
