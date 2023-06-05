from FidoSelf import client
from somnium import Somnium
from fake_useragent import UserAgent
import requests
import json

STRINGS = {
    "get": "**Geeting Ai Chat Result For Query** ( `{}` ) **...**",
    "notres": "**Not Ai Chat Result For Query** ( `{}` )",
    "result": "**Query** ( `{}` ):\n\n**Result:** ( `{}` )",
}

def generate_gpt_response(input_text, chat_id):
    openai.api_key = client.DB.get_key("OPENAI_APIKEY")
    global conversations
    model = "gpt-3.5-turbo"
    messages = conversations.get(chat_id, [])
    messages.append({"role": "user", "content": input_text})
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )
        generated_text = response.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": generated_text})
        conversations[chat_id] = messages
    except Exception as e:
        generated_text = f"`Error generating GPT response: {str(e)}`"
    return generated_text

@client.Command(command="GText (.*)")
async def aichat(event):
    await event.edit(client.STRINGS["wait"])
    client.loop.create_task(generate(event))
    
async def generate(event):
    query = event.pattern_match.group(1)
    await event.edit(STRINGS["get"].format(query))
    result = AiClient.get_response(query)
    if not result:
        return await event.edit(STRINGS["notres"].format(query))
    text = STRINGS["result"].format(query, result)
    await event.edit(text)