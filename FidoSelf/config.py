import os

#Infos
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")
BOT_SESSION = os.environ.get("BOT_SESSION")

#UserInfos
USERID = os.environ.get("USERID")

#Database
REDIS_URL = os.environ.get("REDIS_URL", "redis-12319.c59.eu-west-1-2.ec2.cloud.redislabs.com:12319")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "HvKZ7FppsNWScMFwdV07Q24EeNZHezPT")

#Other
MAX_SIZE = 104857600 * 2
