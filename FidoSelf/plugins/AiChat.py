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

class ThabAi:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            "authority": "chatbot.theb.ai",
            "content-type": "application/json",
            "origin": "https://chatbot.theb.ai",
            "user-agent": UserAgent().random,
        }

    def get_response(self, prompt: str) -> str:
        response = self.session.post(
            "https://chatbot.theb.ai/api/chat-process",
            json={"prompt": prompt, "options": {}},
            stream=True,
        )
        response.raise_for_status()
        response_lines = response.iter_lines()
        response_data = ""
        for line in response_lines:
            if line:
                data = json.loads(line)
                if "utterances" in data:
                    response_data += " ".join(
                        utterance["text"] for utterance in data["utterances"]
                    )
                elif "delta" in data:
                    response_data += data["delta"]
        return response_data
        
AiClient = ThabAi()

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
    caption = STRINGS["result"].format(query, result)
    await client.send_file(event.chat_id, file, caption=caption)
    await event.delete()