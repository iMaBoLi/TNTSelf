from FidoSelf import client
from countryinfo import CountryInfo

__INFO__ = {
    "Category": "Practical",
    "Plugname": "Country Info",
    "Pluginfo": {
        "Help": "To Get Information About Country!",
        "Commands": {
            "{CMD}SCountry <Name>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notcon": "**The Country Name** ( `{}` ) **Is Not Finded!**",
    "country": "**Country Info:** ( `{}` )\n\n**Spellings:** ( `{}` )\n**Capital:** ( `{}` )\n**Population:** ( `{}` )\n**Area:** ( `{}` )\n**Region:** ( `{}` )\n**Currencies:** ( `{}` )\n**Calling Codes:** ( `{}` )\n**Time Zones:** ( `{}` )\n**Borders:** ( `{}` )\n\n**Provinces:** ( `{}` )",
}

@client.Command(command="SCountry (.*)")
async def countryinfo(event):
    await event.edit(client.STRINGS["wait"])
    coname = event.pattern_match.group(1).title()
    try:
        country = CountryInfo(coname)
        info = country.info()
    except:
        return await event.edit(STRINGS["notcon"].format(coname))
    name = info["name"] + " - " + info["nativeName"]
    region = info["region"] + " - " + info["subregion"]
    spellings = ""
    for spelling in info["altSpellings"]:
        spellings += spelling + " - "
    spellings = spellings[:-3]
    currencies = ""
    for currency in info["currencies"]:
        currencies += currency + " - "
    currencies = currencies[:-3]
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
    provinces = ""
    for province in info["provinces"]:
        provinces += province + " - "
    provinces = provinces[:-3]
    text = STRINGS["country"].format(name, spellings, info["capital"], info["population"], info["area"], region, currencies, ccodes, tzones, borders, provinces)
    await event.edit(text)