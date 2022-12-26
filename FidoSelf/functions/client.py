from telethon import TelegramClient

class FidoClient(TelegramClient):
    def __init__(
        self,
        session,
        api_id=None,
        api_hash=None,
        bot_token=None,
        *args,
        **kwargs,
    ):
        kwargs["api_id"] = api_id
        kwargs["api_hash"] = api_hash
        super().__init__(session, **kwargs)
        self.loop.run_until_complete(self.start_client(bot_token=bot_token))
        self.dc_id = self.session.dc_id

    async def start_client(self, **kwargs):
        await self.start(**kwargs)
