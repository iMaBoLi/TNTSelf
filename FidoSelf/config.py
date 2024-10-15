import os

#Infos
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", None)
SESSION = os.environ.get("SESSION", None)
BOT_SESSION = os.environ.get("BOT_SESSION", None)

#Database
REDIS_URL = os.environ.get("REDIS_URL", None)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)

#Other
MAX_SIZE = int(os.environ.get("MAX_SIZE", (104857600 * 5)))