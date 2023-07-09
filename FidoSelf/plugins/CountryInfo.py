from FidoSelf import client
from countryinfo import CountryInfo

__INFO__ = {
    "Category": "Tools",
    "Name": "Country Info",
    "Info": {
        "Help": "To Get Information About Country!",
        "Commands": {
            "{CMD}SCountry <Name>": {
                "Help": "To Get Info",
                "Input": {
                    "<Name>": "Name Of Country",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notcon": "**{STR} The Country Name** ( `{}` ) **Is Not Finded!**",
    "country": "**{STR} Country Info:** ( `{}` )\n\n**{STR} Spellings:** ( `{}` )\n**{STR} Capital:** ( `{}` )\n**{STR} Population:** ( `{}` )\n**{STR} Area:** ( `{}` )\n**{STR} Region:** ( `{}` )\n**{STR} Currencies:** ( `{}` )\n**{STR} Calling Codes:** ( `{}` )\n**{STR} Time Zones:** ( `{}` )\n**{STR} Borders:** ( `{}` )\n\n**{STR} Provinces:** ( `{}` )"
}

@client.Command(command="SCountry (.*)")
async def countryinfo(event):
    await event.edit(client.STRINGS["wait"])
    coname = event.pattern_match.group(1).title()
    try:
        country = CountryInfo(coname)
        info = country.info()
    except:
        return await event.edit(client.getstrings(STRINGS)["notcon"].format(coname))
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
    text = client.getstrings(STRINGS)["country"].format(name, spellings, info["capital"], info["population"], info["area"], region, currencies, ccodes, tzones, borders, provinces)
    await event.edit(text)