import os

#Infos
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")
BOT_SESSION = os.environ.get("BOT_SESSION")

#Database
REDIS_URL = os.environ.get("REDIS_URL")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

#Other
MAX_SIZE = int(os.environ.get("MAX_SIZE"))