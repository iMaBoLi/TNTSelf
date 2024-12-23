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

    def add_coustom_vars(self):
        from TNTSelf.functions import add_vars
        add_vars()
        for client in self.clients:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._add_coustom_vars(client))

    async def _add_coustom_vars(self, client):
        from TNTSelf.functions import DATABASE
        info = await client.get_me()
        botinfo = await client.bot.get_me()
        setattr(client, "me", info)
        setattr(client, "id", info.id)
        setattr(client.bot, "me", botinfo)
        setattr(client.bot, "id", botinfo.id)
        setattr(client.bot, "user", info)
        setattr(client.bot, "user", info.id)
        DB = DATABASE(info.id)
        setattr(client, "DB", DB)
        setattr(client.bot, "DB", DB)
        REALM = DB.get_key("REALM_CHAT") or info.id
        setattr(client, "REALM", REALM)
        setattr(client.bot, "REALM", REALM)