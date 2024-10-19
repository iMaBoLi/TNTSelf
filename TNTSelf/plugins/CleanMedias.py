from TNTSelf import client
from telethon import functions, types

__INFO__ = {
    "Category": "Pv",
    "Name": "Clean Medias",
    "Info": {
        "Help": "To Clean Medias In Pvs!",
        "Commands": {
            "{CMD}CleanPhotos": {
                "Help": "Clean Photo Messages!",
            },
            "{CMD}CleanVideos": {
                "Help": "Clean Video Messages!",
            },
            "{CMD}CleanGifs": {
                "Help": "Clean Gif Messages!",
            },
            "{CMD}CleanMusics": {
                "Help": "Clean Music Messages!",
            },
            "{CMD}CleanVoices": {
                "Help": "Clean Voice Messages!",
            },
            "{CMD}CleanFiles": {
                "Help": "Clean File Messages!",
            },
            "{CMD}CleanContacts": {
                "Help": "Clean Contact Messages!",
            },
            "{CMD}CleanUrls": {
                "Help": "Clean Url Messages!",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "deleting": "**{STR} Deleting Messages Of** ( `{}` ) **Medias In This Chat ...**",
    "del": "**{STR} The** ( `{}` ) **Messages Of** ( `{}` ) **Medias Was Deleted!**",
}

@client.Command(command="Clean(Photo|Video|Gif|Voice|Music|File|Contact|Url)s")
async def cleanmedias(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_private:
        return await event.edit(client.STRINGS["only"]["Pv"])
    filter = event.pattern_match.group(1).title()
    filters = {
        "Photo": types.InputMessagesFilterPhotos,
        "Video": types.InputMessagesFilterVideo,
        "Gif": types.InputMessagesFilterGif,
        "Voice": types.InputMessagesFilterVoice,
        "Music": types.InputMessagesFilterMusic,
        "File": types.InputMessagesFilterDocument,
        "Contact": types.InputMessagesFilterContacts,
        "Url": types.InputMessagesFilterUrl,
    }
    addfilter = filters[filter]
    await event.edit(client.getstrings(STRINGS)["deleting"].format(filter))
    count = 0
    async for message in client.iter_messages(event.chat_id, filter=addfilter, limit=50):
        await message.delete()
        count += 1
    await event.edit(client.getstrings(STRINGS)["del"].format(count, filter))