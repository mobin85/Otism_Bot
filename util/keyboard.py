from pyrogram.types import ReplyKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup([
    ["می‌خواهم صدای اتیسم باشم"],
    ["تماس با ما", "محتواهای آگاهی‌بخشی اتیسم"],
    ["پروفایل"]
], resize_keyboard=True)

keyboard_agahi_bakhsh = ReplyKeyboardMarkup([
    list(reversed(["تشخیص به موقع اتیسم", "پذیرش شخص دارای اتیسم", "پذیرش خانواده اتیسم"])),
    ["بازگشت"]
], resize_keyboard=True)

admin_keyboard = ReplyKeyboardMarkup([
    ["مراحل آموزش", "ساخت آزمون"],
    ["بازگشت"]
], resize_keyboard=True)

amoozesh_keyboard = ReplyKeyboardMarkup([
    ["اضافه کردن مرحله", "حذف کردن مرحله", "پیش نمایش مراحل"],
    ["بازگشت!"]
], resize_keyboard=True)

add_level_keyboard = ReplyKeyboardMarkup([
    ["لغو", "ذخیره"]
], resize_keyboard=True)
