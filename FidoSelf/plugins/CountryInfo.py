from FidoSelf import client
from countryinfo import CountryInfo

STRINGS = {
    "notcon": "**The Country Name** ( `{}` ) **Is Not Finded!**",
    "country": "**Country Info:** ( `{}` )\n\n**Capital:** ( `{}` )\n**Population:** ( `{}` )\n**Area:** ( `{}` )\n**Region:** ( `{}` )\n**Calling Codes:** ( `{}` )\n**TimeZones:** ( `{}` )",
}

@client.Command(command="SCountry (.*)")
async def chatcounts(event):
    await event.edit(client.STRINGS["wait"])
    country = event.pattern_match.group(1).title()
    try:
        country = CountryInfo(country)
        info = country.info()
    except:
        return await event.edit(STRINGS["notcon"].format(country))
    name = info["name"] + " - " + info["nativeName"]
    region = info["region"] + " - " + info["subregion"]
    ccodes = ("".join((tzone + " - " for tzone in info["callingCodes"]))[:-2]
    tzones = ("".join((tzone + " - " for tzone in info["timezones"]))[:-2]
    text = STRINGS["country"].format(name, info["capital"], info["population"], info["area"], region, ccodes, tzones)
    await event.edit(text)