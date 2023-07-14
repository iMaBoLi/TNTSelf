from FidoSelf import client
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

STRINGS = {
    "setinfo": "**{STR} The Spotify Keys Has Been Saved!**\n\n**{STR} Client ID:** ( `{}` )\n**{STR} Client Secret:** ( `{}` )",
    "errorclient": "**{STR} The Spotify Client Is Not Worked!**\n\n**{STR} Error:** ( `{}` )",
    "searchinfo": "**{STR} Title:** ( {} )\n\n**{STR} Duration:** ( `{}` )\n**{STR} Release Date:** ( `{}` )\n\n**{STR} Artists:** ( {} )",
}

def getspotify():
    client_info = client.DB.get_key("SPOTIFY_KEYS")
    if not client_info:
        return None, "Spotify Keys Is Not Saved!"
    client_id = client_info.split(":")[0]
    client_secret = client_info.split(":")[1]
    try:
        spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id ,client_secret=client_secret))
        return spotify, None
    except Exception as error:
        return None, error

@client.Command(command="SetSpotify (.*)\:(.*)")
async def setspotify(event):
    await event.edit(client.STRINGS["wait"])
    client_id = event.pattern_match.group(1)
    client_secret = event.pattern_match.group(2)
    client_info = client_id + ":" + client_secret
    client.DB.set_key("SPOTIFY_KEYS", client_info)
    await event.edit(client.getstrings(STRINGS)["setinfo"].format(client_id, client_secret))
    
@client.Command(command="SpSearch (.*)")
async def searchspotify(event):
    await event.edit(client.STRINGS["wait"])
    query = event.pattern_match.group(1)
    spotify, error = getspotify()
    if not spotify:
        return await event.edit(client.getstrings(STRINGS)["errorclient"].format(error))
    query = "track:" + query
    results = spotify.search(q=query, limit=1)
    track = results["tracks"]["items"][0]
    thumb = client.PATH + track["name"] + ".jpg"
    thumb = await client.functions.download_photo(track["album"]["images"][0]["url"], thumb)
    title = f'[{track["name"]}]({track["external_urls"]["spotify"]})'
    artists = ""
    for artist in track["artists"]:
        arname = artist["name"]
        arlink = artist["external_urls"]["spotify"]
        artists += f"[{arname}]({arlink})" + " - "
    artists = artists[:-3]
    duration = client.functions.convert_time(track["duration_ms"] / 1000)
    caption = client.getstrings(STRINGS)["searchinfo"].format(title, duration, track["album"]["release_date"], artists)
    await client.send_file(event.chat_id, thumb, caption=caption)
    os.remove(thumb)
    await event.delete()