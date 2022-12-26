from telethon import TelegramClient
from telethon.errors import (
    AccessTokenExpiredError,
    AccessTokenInvalidError,
    ApiIdInvalidError,
    AuthKeyDuplicatedError,
)
import sys

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
        self._cache = {}
        self._dialogs = []
        kwargs["api_id"] = api_id
        kwargs["api_hash"] = api_hash
        super().__init__(session, **kwargs)
        self.run_in_loop(self.start_client(bot_token=bot_token))
        self.dc_id = self.session.dc_id

    async def start_client(self, **kwargs):
        try:
            await self.start(**kwargs)
        except ApiIdInvalidError:
            print("• Sorry, API_ID And API_HASH Combination Does Not Match!")
            sys.exit()
        except (AuthKeyDuplicatedError, EOFError) as er:
            print("• Sorry, String Session Is Expired, Create Again!")
            sys.exit()
        except (AccessTokenExpiredError, AccessTokenInvalidError):
            print("• Sorry, Bot Token Is Expired, Create Again!")
            sys.exit()

    def run_in_loop(self, function):
        return self.loop.run_until_complete(function)

    def run(self):
        self.run_until_disconnected()

    def add_handler(self, func, *args, **kwargs):
        if func in [hand[0] for hand in self.list_event_handlers()]:
            return
        self.add_event_handler(func, *args, **kwargs)
