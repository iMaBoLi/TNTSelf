from FidoSelf import client
from datetime import datetime
import datetime as date
from FidoSelf.functions.helper import convert_date

def get_vars():
    fatime = datetime.now()
    entime = datetime.now(date.timezone.utc)
    cdate = convert_date(entime.strftime("%Y"), entime.strftime("%m"), entime.strftime("%d"))
    VARS = {
        "ENSTRDAY": entime.strftime("%A"),
        "ENSTRMONTH": entime.strftime("B"),
        "FADAY": cdate[2],
        "FAMONTH": cdate[1],
        "FAYEAR": cdate[0],
        "FADATE": cdate[0] + "/" cdate[1] + "/" cdate[2],
        "FATIME": fatime.strftime("%H:%M"),
        "FASEC": fatime.strftime("%S"),
        "FAMIN": fatime.strftime("%M"),
        "FAHOUR": fatime.strftime("%H"),
        "ENSTRDAY": entime.strftime("%A"),
        "ENSTRMONTH": entime.strftime("%B"),
        "ENDAY": entime.strftime("%d"),
        "ENMONTH": entime.strftime("%m"),
        "ENYEAR": entime.strftime("%Y"),
        "ENDATE": entime.strftime("%F").replace("-", "/"),
        "ENTIME": entime.strftime("%H:%M"),
        "ENSEC": entime.strftime("%S"),
        "ENMIN": entime.strftime("%M"),
        "ENHOUR": entime.strftime("%H"),
     }
    return VARS
