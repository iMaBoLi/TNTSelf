from FidoSelf import client
from datetime import datetime
import datetime as date

def get_vars():
    entime = datetime.now(date.timezone.utc)
    fatime = datetime.now()
    VARS = {
        "ENSTRDAY": entime.strftime("%A"),
        "ENSTRMONTH": entime.strftime("B"),
        "ENDAY": entime.strftime("%d"),
        "ENYEAR": entime.strftime("%Y"),
        "ENDATE": entime.strftime("%F").replace("-", "/"),
        "ENTIMES": entime.strftime("%H:%M"),
        "ENSEC": entime.strftime("%S"),
        "ENMIN": entime.strftime("%M"),
        "ENHOUR": entime.strftime("%H"),
     }
    return VARS
