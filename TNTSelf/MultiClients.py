from .functions import add_vars
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
import logging

class MultiClients:
    def __init__(self, sessions):
        self.sessions = sessions
        self.clients = list()
        for session in self.sessions:
            api_id = self.sessions[session]["api_id"]
            api_hash = self.sessions[session]["api_hash"]
            sessionstring = self.sessions[session]["session"]
            botsession = self.sessions[session]["botsession"]
            _cli = TelegramClient(
                session=StringSession(sessionstring),
                api_id=int(api_id),
                api_hash=api_hash,
            ).start()
            _cli.bot = TelegramClient(
                session=StringSession(botsession),
                api_id=int(api_id),
                api_hash=api_hash,
            ).start()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._add_coustom_vars(_cli))
            self.clients.append(_cli)

    def run_all_clients(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run_all_clients())

    async def _run_all_clients(self):
        tasks = list()
        for cli in self.clients:
            await cli.start()
            tasks.append(cli.run_until_disconnected())
            await cli.bot.start()
            tasks.append(cli.bot.run_until_disconnected())
        done, tasks = await asyncio.gather(*tasks)
        
    async def _add_coustom_vars(self, client):
        info = await client.get_me()
        botinfo = await client.bot.get_me()
        setattr(client, "me", info)
        setattr(client, "id", info.id)
        setattr(client.bot, "me", botinfo)
        setattr(client.bot, "id", botinfo.id)