from FidoSelf import client
from telethon import Button

@client.Cmd(pattern=f"(?i)^\{client.cmd}help$")
async def helpselfpanel(event):
    await event.edit(f"**{client.str} Processing . . .**")
    res = await client.inline_query(client.bot.me.username, "helpselfpanel")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

BUTTONS = [
    [Button.inline("• Settings •", data=f"helpselfpage:settings"), Button.inline("• Manager •", data=f"helpselfpage:manager")],
    [Button.inline("• Account •", data=f"helpselfpage:account"), Button.inline("• Groups •", data=f"helpselfpage:groups")],
    [Button.inline("• Times •", data=f"helpselfpage:times"), Button.inline("• Others •", data=f"helpselfpage:others")],
    [Button.inline("🚫 Close 🚫", data=f"closehelpself")],
]

@client.Inline(pattern="helpselfpanel")
async def helpselfinline(event):
    text = f"**{client.str} Please Choose Help Panel Page To Get Help Information:**\n\n"
    await event.answer([event.builder.article(f"{client.str} Smart Self - Help", text=text, buttons=BUTTONS)])

@client.Callback(data="helpselfpage\:(.*)")
async def helpselfpages(event):
    page = str(event.data_match.group(1).decode('utf-8'))
    newemoji = "➖"*14
    emoji = "◆"*8
    oemoji = "𖡼"*12
    text = f"**{client.str} The Self Help {page.title()}:**\n"
    if page == "settings":
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
**⭐ Variables:**
💠 `MNAME` = اسم فرد
💠 `UNAME` = اسن خودتان
💠 `TITLE` = اسم چت
💠 `HEART` = قلب رندوم
💠 `TIME` = ساعت
💠 `DATE` = تاریخ
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
**⭐ Variables:**
💠 `MNAME` = اسم فرد
💠 `UNAME` = اسن خودتان
💠 `TITLE` = اسم چت
💠 `HEART` = قلب رندوم
💠 `TIME` = ساعت
💠 `DATE` = تاریخدقیقه
{newemoji}
"""
    elif page == "manager":
        text += f"""
{newemoji}
⚡ `{client.cmd}Panel`
🔅 دریافت پنل مدیریت
{newemoji}
⚡ `{client.cmd}Quicks On-Off`
🔅 روشن-خاموش کردن حالت پاسخ سریع
{emoji}
⚡ `{client.cmd}AddQuick CMD|ANSWERS`
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
**⭐ Notes:**
💎 برای تنظیم چند پاسخ بین هر کدام از , استفاده کنید
💎 برای تنظیم یک مدیا دستور را وارد کنید و روی آن مدیا ریپلی کنید.
💎 دستور و پاسخ شما نباید یکی باشد.
{newemoji}
⚡ `{client.cmd}TSave On-Off`
🔅 روشن-خاموش کردن حالت دانلود عکس و ویدیو های زماندار
{newemoji}
⚡ `{client.cmd}Cinfo CHAT`
🔅 دریافت اطلاعات گروه یا چنل
**🔥 CHAT: REPLY-CHATID-CHATUSERNAME-INCHAT**
{emoji}
⚡ `{client.cmd}Uinfo USER`
🔅 دریافت اطلاعات کاربر
**🔥 USER: REPLY-USERID-USERNAME-INPV**
{newemoji}
"""
    elif page == "account":
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
    elif page == "times":
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
**⭐ Variables:**
💠 `TIME` = ساعت کامل
💠 `DATEEN` = تاریخ میلادی
💠 `DATEFA` = تاریخ شمسی
💠 `HEART` = قلب رندوم
💠 `TIMER` = ساعت آنالوگ
💠 `HOURS` = ساعت
💠 `MINS` = دقیقه
💠 `WEEK` = روز هفته
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
**⭐ Variables:**
💠 `TIME` = ساعت کامل
💠 `DATEEN` = تاریخ میلادی
💠 `DATEFA` = تاریخ شمسی
💠 `HEART` = قلب رندوم
💠 `TIMER` = ساعت آنالوگ
💠 `HOURS` = ساعت
💠 `MINS` = دقیقه
💠 `WEEK` = روز هفته
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
**⭐ Variables:**
💠 `TIME` = ساعت کامل
💠 `DATEEN` = تاریخ میلادی
💠 `DATEFA` = تاریخ شمسی
💠 `HOURS` = ساعت
💠 `MINS` = دقیقه
💠 `WEEK` = روز هفته
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
    elif page == "groups":
        text += f"**{client.str} Empty!**"
    elif page == "others":
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
    await event.edit(text=text, buttons=BUTTONS)

@client.Callback(data="closehelpself")
async def closehelpselfpanel(event):
    await event.edit(text=f"**{client.str} The Help Panel Successfuly Closed!**")
