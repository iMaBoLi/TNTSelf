from FidoSelf import client
from countryinfo import CountryInfo

STRINGS = {
    "notcon": "**The Country Name** ( `{}` ) **Is Not Finded!**",
    "country": "**Country Info:** ( `{}` )\n\n**Capital:** ( `{}` )\n**Population:** ( `{}` )\n**Area:** ( `{}` )\n**Region:** ( `{}` )\n**Calling Codes:** ( `{}` )\n**TimeZones:** ( `{}` )\n**Borders:** ( `{}` )",
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
    ccodes = ""
    for ccode in info["callingCodes"]:
        ccodes += ccode + " - "
    ccodes = ccodes[:-3]
    tzones = ""
    for tzone in info["timezones"]:
        tzones += tzone + " - "
    tzones = tzones[:-3]
    borders = ""
    for border in info["borders"]:
        borders += border + " - "
    borders = borders[:-3]
    text = STRINGS["country"].format(name, info["capital"], info["population"], info["area"], region, ccodes, tzones, borders)
    await event.edit(text)