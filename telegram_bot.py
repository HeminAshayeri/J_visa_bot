import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, ChatJoinRequestHandler, filters
from flask import Flask, request
import os

import asyncio

TOKEN = os.getenv("TG_BOT_TOKEN")
OWNER_ID = int(os.environ["OWNER_ID"])
OWNER_USER = os.environ.get("OWNER_USER")
group_link = os.environ.get("group_link")

app = ApplicationBuilder().token(TOKEN).build()
bot = telegram.Bot(token=TOKEN)
flask_app = Flask(__name__)


async def join_req_msg(update: Update, context = ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    req_welcome_text = f"{user.first_name} عزیز"
    req_send_proof = """سلام وقت بخیرسلام و وقت بخیر 🌿

    به گروه ویزای J ویژه پزشکان خوش آمدید 🙏🏻
    برای تأیید عضویت شما و حفظ فضای تخصصی و امن گروه، لطفاً موارد زیر را با دقت بررسی و در اسرع وقت ارسال بفرمایید:

    🔹 با توجه به اینکه این گروه صرفاً مخصوص پزشکان، دندانپزشکان و داروسازان می‌باشد، لطفاً برای احراز هویت حرفه‌ای خود، یکی از مدارک زیر را به‌صورت تصویر واضح ارسال نمایید:
    1️⃣ کارت دانشجویی
    یا
    2️⃣ کارت نظام پزشکی
    🔹 در صورتی که پروفایل تلگرام شما برای ادمین‌ها قابل مشاهده نیست، لطفاً آن را فعال نمایید.

    ❗️بدیهی است در صورت عدم ارسال مدارک فوق، امکان تأیید عضویت و یا ادامه فعالیت در گروه برای شما فراهم نخواهد بود.
    🙏🏻 سپاس از همکاری شما در حفظ کیفیت و اعتبار این جمع تخصصی

    لطفاً مدارک را به آیدی زیر ارسال بفرمایید:
    {OWNER_USER}

    {group_link} """

    await update.effective_user.send_message(f"{req_welcome_text}\n {req_send_proof}")

    owner_msg = f"""New request 

        user: {user.first_name}
        User_id:  {user.id}

        Group: {update.chat_join_request.chat.title}"""

    await context.bot.send_message(chat_id=OWNER_ID, text=owner_msg)

async def reply_message(update: Update, context=ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = f"""عزیز {user.first_name}
لطفاً برای هرگونه سوال درباره ویزای آمریکا یا شرایط عضویت در گروه،
مستقیماً با ادمین گروه تماس بگیرید:

💬 {OWNER_USER}

از توجه و همکاری شما سپاسگزاریم!"""

    await update.effective_user.send_message(msg)


app.add_handler(handler=ChatJoinRequestHandler(callback=join_req_msg))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, callback=reply_message))






# ---------- Flask webhook route ----------
@flask_app.route(f"/{TOKEN }", methods = ['POST'])
def webhook():
    json_data = request.get_json(force = True)
    update = Update.de_json(data = json_data, bot = app.bot)
    
    asyncio.run(main = app.update_queue.put(update))

    return 'ok'


webhook_url = f'https://J-visa-bot-tv1e.onrender.com/{TOKEN}'
bot.set_webhook(webhook_url)


async def start_bot():
    await app.initialize()
    await app.start()


# برای تست لوکال می‌تونی اینو اجرا کنی
if __name__ == "__main__":
    asyncio.run(start_bot())
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))




