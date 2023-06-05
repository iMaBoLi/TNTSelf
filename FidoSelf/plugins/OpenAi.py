from FidoSelf import client
import openai
import requests

STRINGS = {
    "setapi": "**The OpenAi ApiKey** ( `{}` ) **Has Been Saved!**",
    "noapi": "**The OpenAi ApiKey Is Not Saved!**",
    "getch": "**Geeting OpenAi Result For Question** ( `{}` ) **...**",
    "erch": "**The Ai Result Not Received!**\n\n`{}`",
    "result": "**Question** ( `{}` ):\n\n**ChatGPT:** ( `{}` )",
    "getim": "**Geeting Ai Photo For Query** ( `{}` ) **...**",
    "erim": "**The Ai Photo Not Created!**\n\n`{}`",
    "caption": "**The AiImages For Query** ( `{}` ) **Created!**",
}

@client.Command(command="SetAiKey (.*)")
async def saveaiapi(event):
    await event.edit(client.STRINGS["wait"])
    api = event.pattern_match.group(1)
    client.DB.set_key("OPENAI_APIKEY", api)
    await event.edit(STRINGS["setapi"].format(api))

CONVERSATIONS = {}

async def gpt_response(query, chat_id):
    if not openai.api_key:
        openai.api_key = client.DB.get_key("OPENAI_APIKEY")
    global CONVERSATIONS
    messages = CONVERSATIONS.get(chat_id, [])
    messages.append({"role": "user", "content": query})
    response = await openai.ChatCompletion.acreate(
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
    if not openai.api_key and not client.DB.get_key("OPENAI_APIKEY"):
        return await event.edit(STRINGS["noapi"])
    await event.edit(STRINGS["getch"].format(query))
    try:
        result = await gpt_response(query, event.chat_id)
    except Exception as error:
        return await event.edit(STRINGS["erch"].format(error))
    text = STRINGS["result"].format(query, result)
    await event.respond(text)
    await event.delete()
    
@client.Command(command="GPhoto (.*)")
async def aiphoto(event):
    await event.edit(client.STRINGS["wait"])
    query = event.pattern_match.group(1)
    if not openai.api_key and not client.DB.get_key("OPENAI_APIKEY"):
        return await event.edit(STRINGS["noapi"])
    if not openai.api_key:
        openai.api_key = client.DB.get_key("OPENAI_APIKEY")
    await event.edit(STRINGS["getim"].format(query))
    try:
        result = await openai.Image.acreate(prompt=query, n=3, size="1024x1024")
    except Exception as error:
        return await event.edit(STRINGS["erim"].format(error))
    files = []
    for i, media in enumerate(result["data"], 1):
        filename = query + "-" + str(i) + ".jpg"
        with open(filename, "wb") as f:
            f.write(requests.get(media["url"]).content)
        files.append(filename)
    caption = STRINGS["caption"].format(query)
    await client.send_file(event.chat_id, files, caption=caption)
    await event.delete()