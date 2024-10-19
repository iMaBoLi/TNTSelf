from TNTSelf import client
from telethon import functions, types

__INFO__ = {
    "Category": "Users",
    "Name": "Copy Profile",
    "Info": {
        "Help": "To Copy Profile Info Of Users!",
        "Commands": {
            "{CMD}CopyProfile": {
                "Help": "To Copy Profile",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "copying": "**{STR} The Profile Info For** ( {} ) **Is Copying ...**",
    "copy": "**{STR} The Profile Info For** ( {} ) **Is Copied!**"
}

@client.Command(command="CopyProfile", userid=True)
async def copyprofile(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    info = await client(functions.users.GetFullUserRequest(event.userid))
    uinfo = info.users[0]
    fullinfo = info.full_user
    mention = client.functions.mention(uinfo)
    await event.edit(client.getstrings(STRINGS)["copying"].format(mention))
    fname = uinfo.first_name
    lname = uinfo.last_name or ""
    bio = fullinfo.about or ""
    await client(functions.account.UpdateProfileRequest(first_name=fname, last_name=lname, about=bio))
    if fullinfo.profile_photo:
        photo = await client.download_media(fullinfo.profile_photo)
        profile = await client.upload_file(photo)
        if not fullinfo.profile_photo.video_sizes:
            await client(functions.photos.UploadProfilePhotoRequest(file=profile))
        else:
            await client(functions.photos.UploadProfilePhotoRequest(video=profile))
    await event.edit(client.getstrings(STRINGS)["copy"].format(mention))