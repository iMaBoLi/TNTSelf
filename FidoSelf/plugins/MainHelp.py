from FidoSelf import client
from telethon import Button

PAGES = {
    "s1": "Settings 1",
    "s2": "Settings 2",
    "s3": "Settings 3",
    "m1": "Manager 1",
    "m2": "Manager 2",
    "a": "Account",
    "g": "Groups",
    "o1": "Others 1",
    "o2": "Others 2",
    "t": "Times",
    "v": "Variables",
}

@client.Cmd(pattern=f"(?i)^\{client.cmd}Help$")
async def helpself(event):
    text = f"**{client.str} The Help Self Pages:**\n\n"
    for page in PAGES:
        text += f"**{client.str} Help Page {PAGES[page]}:**\n• `{client.cmd}Help {page.title()}`\n\n"
    await event.edit(text)

@client.Cmd(pattern=f"(?i)^\{client.cmd}Help (s1|s2|s3|m1|m2|o1|o2|a|g|t|v)$")
async def helpselfpages(event):
    page = event.pattern_match.group(1).lower()
    newemoji = "➖"*14
    emoji = "◆"*9
    oemoji = "𖡼"*12
    text = f"**{client.str} The Self Help Page {PAGES[page]}:**\n"
    if page == "s1":
        text += f"""
{newemoji}
⚡ `{client.cmd}SelfAll On-Off`
🔅 روشن-خاموش کردن سلف
{emoji}
⚡ `{client.cmd}Self On-Off`
🔅 روشن-خاموش کردن سلف در یک چت
{newemoji}
⚡ `{client.cmd}SetStr TEXT`
🔅 تنظیم سمبل ابتدای پیام ها
{emoji}
⚡ `{client.cmd}SetCmd TEXT`
🔅 تنظیم سمبل برای ابتدای دستورات
{emoji}
⚡ `.DelCmd`
🔅 پاک کردن سمبل ابتدای دستورات و برگشت به حالت اول
{emoji}
⚡ `{client.cmd}SetRealm`
🔅 تنظیم ریلم چت ( چت پشتیبان )
{emoji}
⚡ `{client.cmd}SetBackCh`
🔅 تنظیم چنل بکاپ ( چنل پشتیبان )
{newemoji}
⚡ `{client.cmd}SmartMonshi On-Off`
🔅 روشن-خاموش کردن حالت منشی خودکار
{emoji}
⚡ `{client.cmd}SetSmartMonshi`
🔅 تنظیم کردن متن منشی خودکار
**↪️ MESSAGE**
{emoji}
⚡ `{client.cmd}SetSmartMonshiSleep TIME`
🔅 تنظیم زمان اسلیپ برای منشی خودکار
{oemoji}
**⭐ Use From Variables!**
{newemoji}
⚡ `{client.cmd}OfflineMonshi On-Off`
🔅 روشن-خاموش کردن حالت منشی آفلاینی
{emoji}
⚡ `{client.cmd}SetOfflineMonshi`
🔅 تنظیم کردن متن منشی آفلاینی
**↪️ MESSAGE-MEDIA**
{emoji}
⚡ `{client.cmd}SetOfflineMonshiSleep TIME`
🔅 تنظیم زمان اسلیپ برای منشی آفلاینی
{oemoji}
**⭐ Use From Variables!**
{newemoji}
"""
    elif page == "s2":
        text += f"**{client.str} Empty ....**"
    elif page == "s3":
        text += f"**{client.str} Empty ....**"
    elif page == "m1":
        text += f"""
{newemoji}
⚡ `{client.cmd}Panel`
🔅 دریافت پنل مدیریت
{newemoji}
⚡ `{client.cmd}Quicks On-Off`
🔅 روشن-خاموش کردن حالت پاسخ سریع
{emoji}
⚡ `{client.cmd}AddQuick 'CMD' ANSWERS`
🔅 اضافه کردن یک پاسخ سریع جدید
**↪️ MEDIA**
{emoji}
⚡ `{client.cmd}DelQuick CMD`
🔅 پاک کردن یک پاسخ سریع
{emoji}
⚡ `{client.cmd}QuickList`
🔅 نمایش لیست پاسخ های سریع
{emoji}
⚡ `{client.cmd}CleanQuickList`
🔅 پاکسازی لیست پاسخ های سریع
{oemoji}
**⭐ Use From Variables!**
{oemoji}
**⭐ Notes:**
💎 برای تنظیم چند پاسخ بین هر کدام از , استفاده کنید
💎 برای تنظیم یک مدیا دستور را وارد کنید و روی آن مدیا ریپلی کنید.
💎 دستور و پاسخ شما نباید یکی باشد.
{newemoji}
⚡ `{client.cmd}AutoDelete On-Off`
🔅 روشن-خاموش کردن حالت پاک کردن خودکار پیام های شما
{emoji}
⚡ `{client.cmd}SetAutoDeleteSleep TIME`
🔅 تنظیم زمان اسلیپ برای پاک کردن پیام های شما
{newemoji}
⚡ `{client.cmd}TSave On-Off`
🔅 روشن-خاموش کردن حالت دانلود عکس و ویدیو های زماندار
{newemoji}
⚡ `{client.cmd}Cinfo CHAT`
🔅 دریافت اطلاعات گروه یا چنل
**🔥 CHAT: CHATID-CHATUSERNAME-INCHAT**
{emoji}
⚡ `{client.cmd}Uinfo USER`
🔅 دریافت اطلاعات کاربر
**🔥 USER: REPLY-USERID-USERNAME-INPV**
{emoji}
⚡ `{client.cmd}Gid`
🔅 دریافت آیدی چت و کاربر
{newemoji}
"""
    elif page == "m2":
        text += f"**{client.str} Empty ....**"
    elif page == "a":
        text += f"""
{newemoji}
⚡ `{client.cmd}DelProfile`
🔅 پاک کردن آخرین پروفایل
{emoji}
⚡ `{client.cmd}DelProfile COUNT`
🔅 پاک کردن پروفایل ها به تعداد دلخواه
💎 اگر قبل از عدد - قرار دهید به تعداد آن عدد از پروفایلهایتان پاک می شود.
{newemoji}
"""
    elif page == "t":
        text += f"""
{newemoji}
⚡ `{client.cmd}Name On-Off`
🔅 روشن-خاموش کردن حالت اسم
{emoji}
⚡ `{client.cmd}AddName TEXT`
🔅 افزودن یک اسم جدید
{emoji}
⚡ `{client.cmd}DelName TEXT`
🔅 پاک کردن یک اسم
{emoji}
⚡ `{client.cmd}NameList`
🔅 نمایش لیست اسم ها
{emoji}
⚡ `{client.cmd}CleanNameList`
🔅 پاکسازی لیست اسم ها
{oemoji}
**⭐ Use From Variables!**
{newemoji}
⚡ `{client.cmd}Bio On-Off`
🔅 روشن-خاموش کردن حالت بیوگرافی
{emoji}
⚡ `{client.cmd}AddBio TEXT`
🔅 افزودن یک بیوگرافی جدید
{emoji}
⚡ `{client.cmd}DelBio TEXT`
🔅 پاک کردن یک بیوگرافی
{emoji}
⚡ `{client.cmd}BioList`
🔅 نمایش لیست بیوگرافی ها
{emoji}
⚡ `{client.cmd}CleanBioList`
🔅 پاکسازی لیست بیوگرافی ها
{oemoji}
**⭐ Use From Variables!**
{newemoji}
⚡ `{client.cmd}Photo On-Off`
🔅 روشن-خاموش کردن حالت عکس
{emoji}
⚡ `{client.cmd}AddPhoto NAME`
🔅 افزودن یک عکس جدید
**↪️ PHOTO**
{emoji}
⚡ `{client.cmd}DelPhoto NAME`
🔅 پاک کردن یک عکس
{emoji}
⚡ `{client.cmd}PhotoList`
🔅 نمایش لیست عکس ها
{emoji}
⚡ `{client.cmd}CleanPhotoList`
🔅 پاکسازی لیست عکس ها
{oemoji}
**⭐ Use From Variables!**
{newemoji}
⚡ `{client.cmd}AddFont NAME`
🔅 افزودن یک فونت جدید
**↪️ FILE**
{emoji}
⚡ `{client.cmd}DelFont NAME`
🔅 پاک کردن یک فونت
{emoji}
⚡ `{client.cmd}FontList`
🔅 نمایش لیست فونت ها
{emoji}
⚡ `{client.cmd}CleanFontList`
🔅 پاکسازی لیست فونت ها
{newemoji}
⚡ `{client.cmd}AddTextTime TEXT`
🔅 افزودن یک متن روی عکس جدید
{emoji}
⚡ `{client.cmd}DelTextTime TEXT`
🔅 پاک کردن یکی از متن های روی عکس
{emoji}
⚡ `{client.cmd}TextTimeList`
🔅 نمایش لیست متن های روی عکس
{emoji}
⚡ `{client.cmd}CleanTextTimeList`
🔅 پاکسازی لیست متن های روی عکس
{newemoji}
"""
    elif page == "g":
        text += f"**{client.str} Empty ....**"
    elif page == "o1":
        text += f"""
{newemoji}
⚡ `{client.cmd}Ping`
🔅 تست آنلاینی سلف
{newemoji}
⚡ `{client.cmd}Str LANG`
🔅 ترجمه یک متن
**↪️ TEXT**
{newemoji}
⚡ `{client.cmd}Ocr`
🔅 استخراج متن از عکس
**↪️ PHOTO**
{emoji}
⚡ `{client.cmd}OcrApi APIKEY`
🔅 ذخیره کردن کلید دسترسی OcrApi
{emoji}
⚡ `{client.cmd}OcrLangs`
🔅 دریافت لیست زبان های OcrApi
{newemoji}
⚡ `{client.cmd}Scopy`
🔅 کپی کردن یک پیام
**↪️ MESSAGE**
{emoji}
⚡ `{client.cmd}Spaste`
🔅 جایگذاری کردن پیام کپی شده
{newemoji}
⚡ `{client.cmd}Sphoto`
🔅 تبدیل استیکر به عکس
**↪️ STICKER**
{emoji}
⚡ `{client.cmd}Ssticker`
🔅 تبدیل عکس به استیکر
**↪️ PHOTO**
{newemoji}
"""
    elif page == "o2":
        text += f"**{client.str} Empty ....**"
    elif page == "v":
        text += f"""
{newemoji}
⚡ `FTIME` - ساعت با فونت
⚡ `FDATE` - تاریخ با فونت
⚡ `FDAY` - عدد روز با فونت
⚡ `FMONTH` - عدد ماه با فونت
⚡ `FYEAR` - عدد سال با فونت
⚡ `FHOUR` - عدد ساعت با فونت
⚡ `FMIN` - عدد دقیقه با فونت
⚡ `FSEC` - عدد ثانیه با فونت
⚡ `TIME` - ساعت ساده
⚡ `DATE` - تاریخ ساده
⚡ `DAY` - عدد روز ساده
⚡ `MONTH` - عدد ماه ساده
⚡ `YEAR` - عدد سال ساده
⚡ `HOUR` - عدد ساعت ساده
⚡ `MIN` - عدد دقیقه ساده
⚡ `SEC` - عدد ثانیه ساده
⚡ `STRDAY` - اسم روز به صورت متن
⚡ `STRMONTH` - اسم ماه به صورت متن
⚡ `HEART` - قلب به صورت رندوم
⚡ `EMOJI` - ایموجی به صورت رندوم
{newemoji}
⚡ `FIRSTNAME` - نام کاربر ارسال کننده
⚡ `LASTNAME` - نام خانوادگی کاربر ارسال کننده
⚡ `USERNAME` - یوزرنیم کاربر ارسال کننده
⚡ `MYFIRSTNAME` - نام شما
⚡ `MYLASTNAME` - نام خانوادگی شما
⚡ `MYUSERNAME` - یوزرنیم شما
⚡ `CHATTITLE` - اسم چت
⚡ `CHATUSERNAME` - یوزرنیم چت
{newemoji}
"""
    await event.edit(text)
