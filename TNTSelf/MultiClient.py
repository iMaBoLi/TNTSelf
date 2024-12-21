from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
import logging

class MultiClient:
    def __init__(self, sessions, *args, **kwargs):
        self.sessions = sessions
        self.clients = list()
        for session in self.sessions:
            api_id = self.sessions[session]["api_id"]
            api_hash = self.sessions[session]["api_hash"]
            sessionstring = self.sessions[session]["session"]
            _cli = TelegramClient(
                session=StringSession(sessionstring),
                api_id=api_id,
                api_hash=api_hash,
                *args,
                **kwargs
            ).start()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._add_coustom_vars(_cli))
            self.clients.append(_cli)

    def on(self, event):
        def decorator(f):
            for cli in self.clients:
                cli.add_event_handler(f, event)
        return decorator

    def run_all_clients(self, loop=None):
        loop = loop if loop is not None else asyncio.get_event_loop()
        loop.run_until_complete(self._run_all_clients())

    async def _run_all_clients(self):
        tasks: list = list()
        for cli in self.clients:
            await cli.start()
            tasks.append(cli.run_until_disconnected())
        done, tasks = await asyncio.gather(*tasks)
        
    async def _add_coustom_vars(self, client):
        setattr(client, "me", (await client.get_me()))