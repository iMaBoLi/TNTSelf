from aiohttp import ClientSession
import requests
import json
import random
import re

async def request(url, post=False, head=False, headers=None, evaluate=None, object=False, re_json=False, re_content=False, *args, **kwargs,):
    async with ClientSession(headers=headers) as CSession:
        method = CSession.head if head else (CSession.post if post else CSession.get)
        data = await method(url, *args, **kwargs)
        if evaluate:
            return await evaluate(data)
        if re_json:
            return await data.json()
        if re_content:
            return await data.read()
        if head or object:
            return data
        return await data.text()

class FakeEmail:
	def __init__(self, session=None):
		self.session = session			
		self.request = requests.session()		
		
	def Mail(self):
		self.Buildsession = str("".join(random.choice("qwertyuiopasdfghjklzxcvbnm0987654321")for i in range(26)))		
		email = self.request.get(f"https://10minutemail.net/address.api.php?new=1&sessionid={self.Buildsession}&_=1661770438359").json()
		datajson = {"mail":email["permalink"]["mail"], "session":email["session_id"]}		
		return datajson

	def inbox(self, loop=False):
		if self.session : 
			sessinbox = self.session	
		elif self.session == None:
			sessinbox = self.Buildsession
		data = self.request.get(f"https://10minutemail.net/address.api.php?sessionid={sessinbox}&_=1661770438359").json()
		if len(data["mail_list"]) != 1:				 
			address = data["mail_list"][0]["subject"]
			id = data["mail_list"][0]["mail_id"]
			box = self.request.get(f"https://10minutemail.net//mail.api.php?mailid={id}&sessionid={sessinbox}").json()
			plain = box["plain_link"]
			datetime = ["datetime"]
			to = box["to"]
			name = box["header_decode"]["replylist"][0]["name"]
			amli = box["header_decode"]["replylist"][0]["address"]
			datainbox = {"topic":address, "name":name, "from":amli, "to":to, "message":plain[0], "datetime":datetime}	
			return datainbox