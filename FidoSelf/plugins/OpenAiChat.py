from FidoSelf import client
import openai
from FidoSelf.functions.AiCreator import AiCreate

STRINGS = {
    "setapi": "**The OpenAi ApiKey** ( `{}` ) **Has Been Saved!**",
    "get": "**Geeting OpenAi Result For Question** ( `{}` ) **...**",
    "result": "**Question** ( `{}` ):\n\n**ChatGPT:** ( `{}` )",
}

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
    return result, CONVERSATIONS[chat_id]

@client.Command(command="SetAiKey (.*)")
async def saveaiapi(event):
    await event.edit(client.STRINGS["wait"])
    api = event.pattern_match.group(1)
    client.DB.set_key("OPENAI_APIKEY", api)
    await event.edit(STRINGS["setapi"].format(api))
    
@client.Command(command="GOText (.*)")
async def aichat(event):
    await event.edit(client.STRINGS["wait"])
    query = event.pattern_match.group(1)
    await event.edit(STRINGS["get"].format(query))
    result, con = await gpt_response(query, event.chat_id)
    file = AiCreate(con, "ChatGPT.html")
    text = STRINGS["result"].format(query, result)
    await event.respond(text, file=file)
    await event.delete()