from FidoSelf import client
from telethon import functions, types

__INFO__ = {
    "Category": "Account",
    "Plugname": "Del Profiles",
    "Pluginfo": {
        "Help": "To Delete Profile Phots!",
        "Commands": {
            "{CMD}DelProfile": "Delete First Profile!",
            "{CMD}DelProfile <Num>": "Delete Inputed Number Profile!",
            "{CMD}DelProfile -<Count>": "Delete Profiles As Required!",
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "not": "**The Profile Photos Is Not Found!**",
    "last": "**The Last Profile Photo Has Been Deleted!**",
    "count": "**The** ( `{}` ) **Of Your Profile Photos Has Been Deleted!**",
    "nota": "**This Profile Photo Is Not Available!**",
    "one": "**The Profile Photo** ( `{}` ) **Has Been Deleted!**",
}

@client.Command(command="DelProfile ?((\-)?\d*)?")
async def delprofiles(event):
    await event.edit(client.STRINGS["wait"])
    pphoto = await client.get_profile_photos("me")
    if not pphoto:
        return await event.edit(STRINGS["not"])
    prof = event.pattern_match.group(1)
    if not prof:
        pphoto = pphoto[0]
        await client(functions.photos.DeletePhotosRequest(id=[types.InputPhoto(id=pphoto.id, access_hash=pphoto.access_hash, file_reference=pphoto.file_reference)]))
        await event.edit(STRINGS["last"])
    elif str(prof).startswith("-"):
        prof = prof.replace("-", "")
        if int(prof) > len(pphoto):
            prof = len(pphoto)
        for con in range(0, int(prof)):
            profs = pphoto[con]
            await client(functions.photos.DeletePhotosRequest(id=[types.InputPhoto(id=profs.id, access_hash=profs.access_hash, file_reference=profs.file_reference)]))
        await event.edit(STRINGS["count"].format(prof))
    else:        
        if int(prof) > len(pphoto):
            return await event.edit(STRINGS["nota"])
        pphoto = pphoto[int(prof)-1]
        await client(functions.photos.DeletePhotosRequest(id=[types.InputPhoto(id=pphoto.id, access_hash=pphoto.access_hash, file_reference=pphoto.file_reference)]))
        await event.edit(STRINGS["one"].format(prof))
