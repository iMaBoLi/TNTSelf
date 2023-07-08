from FidoSelf import client
from telethon import functions
from telethon.errors import UsernameInvalidError, UsernameOccupiedError

__INFO__ = {
    "Category": "Account",
    "Name": "Edit Profile",
    "Info": {
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
    "Name": "Set Profile",
    "Info": {
        "Help": "To Set Your Profile Photo!",
        "Commands": {
            "{CMD}SetProfile <Reply(Photo)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "lenname": "**{STR} The Number Of Characters Entered For Name Exceeds The Limit!**",
    "setname": "**{STR} The Profile Name Was Set To** ( `{}` )",
    "lenlname": "**{STR} The Number Of Characters Entered For Last Name Exceeds The Limit!**",
    "setlname": "**{STR} The Profile Last Name Was Set To** ( `{}` )",
    "lenbio": "**{STR} The Number Of Characters Entered For Bio Exceeds The Limit!**",
    "setbio": "**{STR} The Profile Bio Was Set To** ( `{}` )",
    "lenuname": "**{STR} The Number Of Characters Entered For UserName Exceeds The Limit!**",
    "unameinvalid": "**{STR} The Entered UserName Is Invalid!**",
    "unameall": "**{STR} The Entered UserName Is Already Used!**",
    "setuname": "**{STR} The Profile UserName Was Set To** ( `{}` )",
    "setprof": "**{STR} The Photo iS Added To Profile Photos!**"
}

@client.Command(command="Set(Name|LName|Bio|Username) (.*)")
async def setinfos(event):
    await event.edit(client.STRINGS["wait"])
    type = event.pattern_match.group(1).lower()
    data = str(event.pattern_match.group(2))
    if type == "name":
        if len(data) > 50:
            return await event.edit(client.getstrings(STRINGS)["lenname"])
        await client(functions.account.UpdateProfileRequest(first_name=str(data)))
        await event.edit(client.getstrings(STRINGS)["setname"].format(data))
    elif type == "lname":
        if len(data) > 50:
            return await event.edit(client.getstrings(STRINGS)["lenlname"])
        await client(functions.account.UpdateProfileRequest(last_name=str(data)))
        await event.edit(client.getstrings(STRINGS)["setlname"].format(data))
    elif type == "bio":
        if len(data) > 70:
            return await event.edit(client.getstrings(STRINGS)["lenbio"])
        await client(functions.account.UpdateProfileRequest(about=str(data)))
        await event.edit(client.getstrings(STRINGS)["setbio"].format(data))
    elif type == "username":
        data = data.replace(" ", "")
        if 5 > len(data) > 32:
            return await event.edit(client.getstrings(STRINGS)["lenuname"])
        try:
            await client(functions.account.UpdateUsernameRequest(username=data))
        except UsernameInvalidError:
            return await event.edit(client.getstrings(STRINGS)["unameinvalid"])
        except UsernameOccupiedError:
            return await event.edit(client.getstrings(STRINGS)["unameall"])
        await event.edit(client.getstrings(STRINGS)["setuname"].format("@" + data))

@client.Command(command="SetProfile")
async def setprofile(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    profile = await client.upload_file(photo)
    await client(functions.photos.UploadProfilePhotoRequest(file=profile))
    await event.edit(client.getstrings(STRINGS)["setprof"])
    os.remove(photo)