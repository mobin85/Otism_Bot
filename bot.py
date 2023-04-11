import asyncio
import re
from pathlib import Path
from typing import Coroutine

from pyromod.listen.listen import ListenerTypes

from util import *
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyromod.listen import Client as C
from setting import *
from db import Admin, Video, IsAdmin, Question


class Bot(Client):
    def __init__(self):
        super().__init__("bot1", API_ID, API_HASH, bot_token=TOKEN)
        self.otism_sound_answers = {
            0: {
                "photo": "util/start_3.jpg",
                "caption": """**می‌دونی اتیسم چیه؟**
اتیسم یک اختلال عصبی-رشدیه، یعنی بخش‌های مختلف مغز نمی‌تونن به‌درستی باهم ارتباط برقرار کنن و نتیجه این اتفاق می‌تونه در هر فرد دارای اتیسم متفاوت باشه، به‌خاطر همین اتیسم رو با طیف‌های مختلفش معرفی می‌کنن.
**افراد دارای اتیسم دنیا رو به‌شکل دیگه‌ای می‌بینن، می‌شنون و حس می‌کنن و نمی‌تونن با ما که از نگاه **اونها، در دنیای دیگه‌ای هستیم ارتباط برقرار کنن، به همین دلیل دچار درخودماندگی می‌شن.
""",
                "reply_markup": InlineKeyboardMarkup([
                    [InlineKeyboardButton("فهمیدیم، ادامه...", callback_data="otism_sound:1")]
                ])
            },
            1: {
                "photo": "util/start_4.jpg",
                "caption": """**صحبت از یه اختلال نادر نیست**
طبق آخرین آمار آمریکا از هر ۳۶ تولد یه کودک دارای اتیسم متولد میشه، خیلی زیاده!

**در دوران بارداری و لحظه تولد هم قابل تشخیص نیست**
متاسفانه با آزمایش‌های زمان بارداری و غربالگری و ... اتیسم رو نمیشه تشخیص داد، پس قبل از تولد نمیشه کاری کرد. بلافاصله بعد از تولد هم نمیشه تشخیص داد و لازمه پدر و مادر رشد بچه‌شون رو خیلی دقیق رصد کنن. اگر دیدن کاری با تاخیر داره انجام میشه یا بچه‌شون یه مقدار با بقیه تفاوت داره، لازمه حساس بشن و از متخصص سوال کنن.

**تا پایان عمر...**
اتیسم کامل درمان نمیشه و تا آخر عمر همراه شخص هست. اما اگر تشخیص به‌موقع اتفاق بیفته و خانواده تو سه سالگی یا نهایتا قبل از شش سالگی تشخیص بده با کلاس‌های توانبخشی کودک دارای اتیسم می‌تونه به استقلال بیشتری برسه و در بزرگ‌سالی لحظه‌های آروم‌تری رو تجربه کنه. 
کلاس‌های توانبخشی: گفتار درمانی، کار درمانی، رفتار درمانی""",
                "reply_markup": InlineKeyboardMarkup([
                    [InlineKeyboardButton("فهمیدیم، ادامه...", callback_data="otism_sound:2")]
                ])
            },
            2: {
                "photo": "util/start_5.jpg",
                "caption": """**همه افراد دارای اتیسم شبیه هم نیستند**
اتیسم طیف‌های مختلفی داره، ممکنه شما شخص دارای اتیسم رو ببینید که صحبت می‌کنه و دیگری رو ببینید که نمی‌تونه حتی کلمه‌ای صحبت کنه. شخصی رو ببینید که آروم نشسته و دیگری رو ببینید که بال بال می‌زنه و بی‌قراری زیادی داره. شخصی رو ببینید که صداها و نورها رو چند برابر بیشتر حس می‌کنه (بیش‌حسی) و دیگری رو ببینید که حتی زخم شدن دستش رو متوجه نمیشه (کم‌حسی)
**پس اگه یه فرد دارای اتیسم رو می‌شناسیم به این معنی نیست که اتیسم رو می‌شناسیم، رفتارها و نشانه‌ها **در افراد دارای اتیسم متفاوته""",
                "reply_markup": InlineKeyboardMarkup([
                    [InlineKeyboardButton("فهمیدیم، ادامه...", callback_data="otism_sound_video:1")]
                ])
            }
        }

        @self.on_message(filters=filters.private)
        async def echo(_, msg: Message):
            text = msg.text
            chat = msg.chat.id
            if text == "/start":
                await self.start_command(msg)
            elif text == "می‌خواهم صدای اتیسم باشم":
                await self.otism_sound(msg)
            elif text == "محتواهای آگاهی‌بخشی اتیسم":
                await self.send_message(chat, "test", reply_markup=keyboard_agahi_bakhsh)
            elif text == "admin":
                if IsAdmin.get_or_none(IsAdmin.user_id == msg.from_user.id):
                    await self.send_message(chat, "Welcome to Admin Panel", reply_markup=admin_keyboard)
                else:
                    await self.send_message(chat, "Enter Admin Password")
                    password: Message = await msg.chat.listen()
                    if password.text == Admin.get().password:
                        await self.send_message(chat, "Welcome to Admin Panel", reply_markup=admin_keyboard)
                        if not IsAdmin.get_or_none(IsAdmin.user_id == msg.from_user.id):
                            IsAdmin.create(user_id=msg.from_user.id)
                    else:
                        await self.send_message(chat, "Wrong password!", reply_markup=main_keyboard)

            elif text == "بازگشت":
                await self.is_admin_checker(self.send_with_reply(chat, "بازگشت انجام شد", main_keyboard),
                                            msg.from_user.id)
            elif text == "بازگشت!":
                await self.is_admin_checker(self.send_with_reply(chat, "بازگشت انجام شد", admin_keyboard),
                                            msg.from_user.id)
            elif text == "مراحل آموزش":
                await self.is_admin_checker(self.send_with_reply(chat, "قسمت آموزش", amoozesh_keyboard),
                                            msg.from_user.id)
            elif text == "ساخت آزمون":
                await self.make_exam(msg)
            elif text == "اضافه کردن مرحله":
                await self.is_admin_checker(self.add_level(msg), msg.from_user.id)

            elif text == "پیش نمایش مراحل":
                for video in Video.select():
                    await self.send_video(chat, video.text, "مرحله {}".format(video.id))
                    await asyncio.sleep(.5)

        @self.on_callback_query()
        async def callback(_, call: CallbackQuery):
            if res := re.search(r'otism_sound:(\d+)', call.data):
                await self.send_photo(call.message.chat.id, **self.otism_sound_answers[int(res.groups()[0])])
            elif res := re.search(r'otism_sound_video:(\d+)', call.data):
                index = int(res.groups()[0])
                obj: Video = Video.get_or_none(id=index)
                if not obj:
                    return
                video_path, text = obj.video_path, obj.text
                if Video.get_or_none(id=index + 1):
                    continue_keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("فهمیدیم، ادامه...", callback_data=f"otism_sound_video:{index + 1}")]
                    ])
                    if Path(video_path).suffix[1:] in ("mp4", "mkv", "avi", "m4v"):
                        await self.send_video(call.message.chat.id, video_path, caption=text,
                                              reply_markup=continue_keyboard)
                    elif Path(video_path).suffix[1:] in ("png", "jpg", "jpeg"):
                        await self.send_photo(call.message.chat.id, video_path, caption=text,
                                              reply_markup=continue_keyboard)
                else:
                    start_question_keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("شروع آزمون", callback_data="start_question")]
                    ])
                    if Path(video_path).suffix[1:] in ("mp4", "mkv", "avi", "m4v"):
                        await self.send_video(call.message.chat.id, video_path, caption=text,
                                              reply_markup=start_question_keyboard)
                    elif Path(video_path).suffix[1:] in ("png", "jpg", "jpeg"):
                        await self.send_photo(call.message.chat.id, video_path, caption=text,
                                              reply_markup=start_question_keyboard)
            elif call.data == "start_question":
                questions = Question.select()
                len_questions = len(questions)
                answers = 0
                for question in questions:
                    question_keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton(f"{question.answer_1} (1", callback_data="1"),
                         InlineKeyboardButton(f"{question.answer_2} (2", callback_data="2")],
                        [InlineKeyboardButton(f"{question.answer_3} (3", callback_data="3"),
                         InlineKeyboardButton(f"{question.answer_4} (4", callback_data="4")]
                    ])
                    await self.send_message(call.message.chat.id, f"({question.id}/{len_questions})\n{question.question}",
                                            reply_markup=question_keyboard)
                    c: CallbackQuery = await call.message.chat.listen(listener_type=ListenerTypes.CALLBACK_QUERY)
                    if int(c.data) == question.answer:
                        answers += 1

                percent = (answers / len_questions) * 100
                await self.send_message(call.message.chat.id, "ریدم تو این مهدی فیر {} درصد زدی بینیم بینیم".format(percent))
                await self.send_message(call.message.chat.id, "کشید یا نکشیددددددددددددددددددددددددددددددددددد")

        self.run()

    async def make_exam(self, msg: Message):
        questions_num = await msg.chat.ask("تعداد سوالات خود را وارد کنید")
        Question.raw("DELETE FROM question").execute()
        for i in range(1, int(questions_num.text) + 1):
            question: str = (await msg.chat.ask("لطفا سوال {} را وارد کنید".format(i))).text
            answer_1: str = (await msg.chat.ask("گزینه اول را وارد کنید")).text
            answer_2: str = (await msg.chat.ask("گزینه دوم را وارد کنید")).text
            answer_3: str = (await msg.chat.ask("گزینه سوم را وارد کنید")).text
            answer_4: str = (await msg.chat.ask("گزینه چهارم را وارد کنید")).text
            answer: str = (await msg.chat.ask("جواب صحیح را به عدد وارد کنید (1 تا 4)")).text

            Question.create(
                question=question,
                answer_1=answer_1,
                answer_2=answer_2,
                answer_3=answer_3,
                answer_4=answer_4,
                answer=answer
            )
        ok: Message = await self.send_message(msg.chat.id, "آیا میخواهید ذخیره کنید؟", reply_markup=add_level_keyboard)
        if ok.text == "ذخیره":
            await self.send_message(msg.chat.id, "ذخیره شد!", reply_markup=admin_keyboard)
        elif ok.text == "لغو":
            await self.send_message(msg.chat.id, "لغو شد!", reply_markup=admin_keyboard)
            Question.raw("DELETE FROM question").execute()

    async def is_admin_checker(self, coroutine: Coroutine, user_id: int, check: bool = True):
        if check:
            if IsAdmin.get_or_none(IsAdmin.user_id == user_id):
                return await coroutine
        else:
            return await coroutine

    async def start_command(self, msg: Message):
        first_caption = """کاش همه اتیسم رو می‌شناختن...
این آرزوی خیلی از پدران و مادران کودکان دارای اتیسم است"""
        await self.send_photo(msg.chat.id, "util/start_1.jpg", caption=first_caption)
        first_msg = """سلام
امیدواریم خوب باشید

خیلی خوشحالیم که اینجایید و می‌خواید صدای اتیسم باشید، صدای ما در «انجمن اتیسم ایران» به تنهایی به جایی نمی‌رسه، اما ایمان داریم با کمک شما صدامون به خیلی جاها می‌رسه و می‌تونیم اتیسم رو خیلی بهتر و دقیق‌تر به جامعه معرفی کنیم.

به امید روزی که همه اتیسم رو بشناسن و کودکان دارای اتیسم و خانواده‌شون خیلی راحت بتونن زندگی کنن.
به امید روزهای روشن‌تر برای جامعه اتیسم ایران"""
        await asyncio.sleep(1)
        await self.send_message(msg.chat.id, first_msg)
        second_msg = """این بات توسط «انجمن اتیسم ایران» راه‌اندازی شده و کمک می‌کنه شما یه مقداری اتیسم رو بشناسید و بعدش با محتوایی که در اختیارتون قرار می‌گیره کمک کنید افراد بیشتری اتیسم رو بشناسن. 
ممنون از اینکه همراه جامعه اتیسم هستید.
اینستاگرام‌مون رو داری؟    https://www.instagram.com/iran.autism.association/
اینم وب‌سایت: irautism.org  

آماده‌ای «صدای اتیسم باشی؟»"""
        await asyncio.sleep(1)
        await self.send_photo(msg.chat.id, "util/start_2.jpg", second_msg, reply_markup=main_keyboard)

    async def send_with_reply(self, chat: int, text: str, keyboard: ReplyKeyboardMarkup):
        await self.send_message(chat, text, reply_markup=keyboard)

    async def add_level(self, msg: Message):
        video: Message = await msg.chat.ask("لطفا ویدیو مورد نظر خود را وارد کنید")
        text: Message = await msg.chat.ask("لطفا متن مورد نظر خود را وارد کنید")
        ok: Message = await msg.chat.ask("آیا میخواهید ذخیره کنید؟", reply_markup=add_level_keyboard)
        if ok.text == "ذخیره":
            await msg.reply("ذخیره شد!", reply_markup=admin_keyboard)
            video_path = await self.download_media(video)
            Video.create(text=text.text, video_path=video_path)
            print("دخیره شد!")
        elif ok.text == "لغو":
            await msg.reply("لغو شد!", reply_markup=admin_keyboard)

    async def otism_sound(self, msg: Message):
        await self.send_photo(msg.chat.id, **self.otism_sound_answers[0])


if __name__ == "__main__":
    bot = Bot()
