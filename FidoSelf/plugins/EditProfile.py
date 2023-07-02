from FidoSelf import client
from telethon import functions
from telethon.errors import UsernameInvalidError, UsernameOccupiedError

__INFO__ = {
    "Category": "Account",
    "Plugname": "Edit Profile",
    "Pluginfo": {
        "Help": "To Setting Your Profile Info!",
        "Commands": {
            "{CMD}SetName <Text>": "Set First Name!",
            "{CMD}SetLName <Text>": "Set Last Name!",
            "{CMD}SetBio <Text>": None,
            "{CMD}SetUsername <Text>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)
__INFO__ = {
    "Category": "Account",
    "Plugname": "Set Profile",
    "Pluginfo": {
        "Help": "To Set Your Profile Photo!",
        "Commands": {
            "{CMD}SetProfile <Reply(Photo)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "lenname": "**The Number Of Characters Entered For Name Exceeds The Limit!**",
    "setname": "**The Profile Name Was Set To** ( `{}` )",
    "lenlname": "**The Number Of Characters Entered For Last Name Exceeds The Limit!**",
    "setlname": "**The Profile Last Name Was Set To** ( `{}` )",
    "lenbio": "**The Number Of Characters Entered For Bio Exceeds The Limit!**",
    "setbio": "**The Profile Bio Was Set To** ( `{}` )",
    "lenuname": "**The Number Of Characters Entered For UserName Exceeds The Limit!**",
    "unameinvalid": "**The Entered UserName Is Invalid!**",
    "unameall": "**The Entered UserName Is Already Used!**",
    "setuname": "**The Profile UserName Was Set To** ( `{}` )",
    "setprof": "**The Photo iS Added To Profile Photos!**",
}

@client.Command(command="Set(Name|LName|Bio|Username) (.*)")
async def setinfos(event):
    await event.edit(client.STRINGS["wait"])
    type = event.pattern_match.group(1).lower()
    data = str(event.pattern_match.group(2))
    if type == "name":
        if len(data) > 50:
            return await event.edit(STRINGS["lenname"])
        await client(functions.account.UpdateProfileRequest(first_name=str(data)))
        await event.edit(STRINGS["setname"].format(data))
    elif type == "lname":
        if len(data) > 50:
            return await event.edit(STRINGS["lenlname"])
        await client(functions.account.UpdateProfileRequest(last_name=str(data)))
        await event.edit(STRINGS["setlname"].format(data))
    elif type == "bio":
        if len(data) > 70:
            return await event.edit(STRINGS["lenbio"])
        await client(functions.account.UpdateProfileRequest(about=str(data)))
        await event.edit(STRINGS["setbio"].format(data))
    elif type == "username":
        data = data.replace(" ", "")
        if 5 > len(data) > 32:
            return await event.edit(STRINGS["lenuname"])
        try:
            await client(functions.account.UpdateUsernameRequest(username=data))
        except UsernameInvalidError:
            return await event.edit(STRINGS["unameinvalid"])
        except UsernameOccupiedError:
            return await event.edit(STRINGS["unameall"])
        await event.edit(STRINGS["setuname"].format("@" + data))

@client.Command(command="SetProfile")
async def setprofile(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    profile = await client.upload_file(photo)
    await client(functions.photos.UploadProfilePhotoRequest(file=profile))
    await event.edit(STRINGS["setprof"])
    os.remove(photo)