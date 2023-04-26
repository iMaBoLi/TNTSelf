from FidoSelf import client

STRINGS = {
    "EN": {
        "Main": "**{STR} The {} Has Been {}!**",
        "Name": "Name Mode",
        "Bio": "Bio Mode",
        "Photo": "Photo Mode",
        "Dtimer": "Download Timer Medias",
        "Quicks": "Quicks Mode",
        "Monshi": "Monshi Self",
        "Autodelete": "Auto Delete Messages",
        "Autoreplace": "Auto Replace Mode",
        "Autosay": "Auto Say Mode",
        "Mutepv": "Mute Pv",
        "Lockpv": "Lock Pv",
        "Antispampv": "Anti Spam Pv",
        "Readall": "MarkRead All",
        "Readpv": "MarkRead Pvs",
        "Readgp": "MarkRead Groups",
        "Readch": "MarkRead Channels",
    },
    "FA": {
        "Main": "**{STR} حالت {} باموفقیت {}!**",
        "Name": "اسم",
        "Bio": "بیو",
        "Photo": "عکس",
        "Dtimer": "دانلود مدیا های زماندار",
        "Quicks": "پاسخ سریع",
        "Monshi": "منشی سلف",
        "Autodelete": "پاک کردن خودکار پیام ها",
        "Autoreplace": "جایگزین کردن خودکار پیام ها",
        "Autosay": "ادیت کردن خودکار پیام ها",
        "Mutepv": "سکوت پیوی",
        "Lockpv": "قفل پیوی",
        "Antispampv": "آنتی اسپم پیوی",
        "Readall": "خواندن همه پیام ها",
        "Readpv": "خواندن پیام های پیوی",
        "Readgp": "خواندن پیام های گروه",
        "Readch": "خواندن پیام های چنل",
    },
}

Modes = {
    "EN": {
        "Name": "NAME_MODE",
        "Bio": "BIO_MODE",
        "Photo": "PHOTO_MODE",
        "Dtimer": "TIMER_MODE",
        "Quicks": "QUICKS_MODE",
        "Monshi": "MONSHI_MODE",
        "Autodelete": "AUTO_DELETE_MODE",
        "Autoreplace": "AUTO_REPLACE_MODE",
        "Autosay": "AUTO_SAY_MODE",
        "Mutepv": "MUTE_PV",
        "Lockpv": "LOCK_PV",
        "Antispampv": "ANTISPAM_PV",
        "Readall": "READALL_MODE",
        "Readpv": "READPV_MODE",
        "Readgp": "READGP_MODE",
        "Readch": "READCH_MODE",
    },
    "FA": {
        "اسم": "NAME_MODE",
        "بیو": "BIO_MODE",
        "عکس": "PHOTO_MODE",
        "دانلود تایمردار": "TIMER_MODE",
        "پاسخ ها": "QUICKS_MODE",
        "منشی": "MONSHI_MODE",
        "حذف خودکار": "AUTO_DELETE_MODE",
        "جایگزین خودکار": "AUTO_REPLACE_MODE",
        "تایپ خودکار": "AUTO_SAY_MODE",
        "سکوت پیوی": "MUTE_PV",
        "قفل پیوی": "LOCK_PV",
        "آنتی اسپم پیوی": "ANTISPAM_PV",
        "خواندن همه": "READALL_MODE",
        "خواندن پیوی": "READPV_MODE",
        "خواندن گروه": "READGP_MODE",
        "خواندن چنل": "READCH_MODE",
    },
}

ENPAT = ""
for mode in Modes["EN"]:
    ENPAT += mode + "|"
ENPAT = ENPAT[:-1]

FAPAT = ""
for mode in Modes["FA"]:
    FAPAT += mode + "|"
FAPAT = FAPAT[:-1]

@client.Command(
    commands={
        "EN": f"({ENPAT}) (On|Off)",
        "FA": f"({FAPAT}) (روشن|خاموش)",
     }
)
async def changer(event):
    await event.edit(client.get_string("wait"))
    Mode = event.pattern_match.group(1).title()
    Change = event.pattern_match.group(2).lower()   
    client.DB.set_key(Modes[client.LANG][Mode], Change)
    Mode = client.get_string(Mode, STRINGS)
    Change = client.get_string("On") if Change == "on" else client.get_string("Off")
    Main = client.get_string("Main", STRINGS)
    await event.edit(Main.format(Mode, Change))
