from TNTSelf import client
from telethon import functions
from telethon.errors import UsernameInvalidError, UsernameOccupiedError

__INFO__ = {
    "Category": "Account",
    "Name": "Edit Profile",
    "Info": {
        "Help": "To Setting Your Profile Info!",
        "Commands": {
            "{CMD}SetName <Text>": {
                "Help": "To Set First Name",
                "Input": {
                    "<Text>": "Text Name",
                },
            },
            "{CMD}SetLName <Text>": {
                "Help": "To Set Last Name",
                "Input": {
                    "<Text>": "Text Last Name",
                },
            },
            "{CMD}SetBio <Text>": {
                "Help": "To Set Bio",
                "Input": {
                    "<Text>": "Text Bio",
                },
            },
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
            "{CMD}SetProfile": {
                "Help": "To Set Profile Photo",
                "Reply": ["Photo"],
            },
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
    "notprof": "**{STR} The Media Is Unavailable For Your Profile Medias!**", 
    "setprof": "**{STR} The Media Is Added To Profile Medias!**", 
}

@client.Command(command="Set(Name|LName|Bio) (.*)")
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
    if reply:= event.checkReply(["Photo", "Video"]):
        return await event.edit(reply)
    callback = event.progress(download=True)
    downfile = await client.fast_download(event.reply_message, progress_callback=callback)
    profile = await client.upload_file(downfile)
    if client.functions.mediatype(event.reply_message) == "Video":
        try:
            await client(functions.photos.UploadProfilePhotoRequest(video=profile))
        except:
            return await event.edit(client.getstrings(STRINGS)["notprof"])
    else:
        await client(functions.photos.UploadProfilePhotoRequest(file=profile))
    await event.edit(client.getstrings(STRINGS)["setprof"])
    os.remove(downfile)