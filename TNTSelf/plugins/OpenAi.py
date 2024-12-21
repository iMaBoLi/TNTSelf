from TNTSelf import client
from openai import OpenAI
import openai
import requests

__INFO__ = {
    "Category": "Tools",
    "Name": "Open Ai",
    "Info": {
        "Help": "To Use From OpenAi For Chat And Create Photo!",
        "Commands": {
            "{CMD}SetAiKey <Key>": "Set OpenAi Api Key!",
            "{CMD}GText <Text>": "To Get Response For Text!",
            "{CMD}GPhoto <Text>": "To Create Photo For Text!",
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "setapi": "**{STR} The OpenAi ApiKey** ( `{}` ) **Has Been Saved!**",
    "noapi": "**{STR} The OpenAi ApiKey Is Not Saved!**",
    "getch": "**{STR} Geeting OpenAi Result For Question** ( `{}` ) **...**",
    "erch": "**{STR} The Ai Result Not Received!**\n\n`{}`",
    "result": "**{STR} Question** ( `{}` ):\n\n**ChatGPT:** ( `{}` )",
    "getim": "**{STR} Geeting Ai Photo For Query** ( `{}` ) **...**",
    "erim": "**{STR} The Ai Photo Not Created!**\n\n`{}`",
    "caption": "**{STR} The AiImages For Query** ( `{}` ) **Created!**"
}

@client.Command(command="SetAiKey (.*)")
async def saveaiapi(event):
    await event.edit(client.STRINGS["wait"])
    api = event.pattern_match.group(1)
    client.DB.set_key("OPENAI_APIKEY", api)
    await event.edit(client.getstrings(STRINGS)["setapi"].format(api))

CONVERSATIONS = {}

async def gpt_response(query, chat_id):
    apikey = client.DB.get_key("OPENAI_APIKEY")
    AiClient = OpenAI(api_key=apikey)
    global CONVERSATIONS
    messages = CONVERSATIONS.get(chat_id, [])
    messages.append({"role": "user", "content": query})
    response = await AiClient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    result = response.choices[0].message.content.strip()
    messages.append({"role": "assistant", "content": result})
    CONVERSATIONS[chat_id] = messages
    return result
    
@client.Command(command="GText (.*)")
async def aichat(event):
    await event.edit(client.STRINGS["wait"])
    query = event.pattern_match.group(1)
    apikey = client.DB.get_key("OPENAI_APIKEY")
    if not apikey:
        return await event.edit(client.getstrings(STRINGS)["noapi"])
    await event.edit(client.getstrings(STRINGS)["getch"].format(query))
    try:
        result = await gpt_response(query, event.chat_id)
    except Exception as error:
        return await event.edit(client.getstrings(STRINGS)["erch"].format(error))
    text = client.getstrings(STRINGS)["result"].format(query, result)
    await event.respond(text)
    await event.delete()
    
@client.Command(command="aiPhoto (.*)")
async def aiphoto(event):
    await event.edit(client.STRINGS["wait"])
    query = event.pattern_match.group(1)
    if not client.DB.get_key("OPENAI_APIKEY"):
        return await event.edit(client.getstrings(STRINGS)["noapi"])
    if not openai.api_key:
        openai.api_key = client.DB.get_key("OPENAI_APIKEY")
    await event.edit(client.getstrings(STRINGS)["getim"].format(query))
    try:
        result = await openai.Image.acreate(prompt=query, n=3, size="1024x1024")
    except Exception as error:
        return await event.edit(client.getstrings(STRINGS)["erim"].format(error))
    files = []
    for i, media in enumerate(result["data"], 1):
        filename = query + "-" + str(i) + ".jpg"
        with open(filename, "wb") as f:
            f.write(requests.get(media["url"]).content)
        files.append(filename)
    caption = client.getstrings(STRINGS)["caption"].format(query)
    await client.send_file(event.chat_id, files, caption=caption)
    await event.delete()