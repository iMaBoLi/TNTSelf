###
MAINCONFIG = "../tmp/config.txt"
OLDDATA = open(MAINCONFIG, "r").readlines()
DATA = []
for ODATA in OLDDATA:
    DATA.append(str(ODATA).replace("\n", ""))

#Infos
API_ID = int(DATA[0])
API_HASH = DATA[1]
SESSION = DATA[2]
BOT_SESSION = DATA[3]

#Database
REDIS_URL = DATA[4]
REDIS_PASSWORD = DATA[5]

#Other
MAX_SIZE = 104857600 * 5