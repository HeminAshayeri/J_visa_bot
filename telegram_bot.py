from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, ChatJoinRequestHandler, filters
from flask import Flask, request
import os

import asyncio

TOKEN = os.getenv("TG_BOT_TOKEN")
OWNER_ID = int(os.environ["OWNER_ID"])

app = ApplicationBuilder().token(TOKEN).build()
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
    @DrHemin

    https://t.me/+4-las6zkqDZkNWNk """

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

💬 @DrHemin

از توجه و همکاری شما سپاسگزاریم!"""

    await update.effective_user.send_message(msg)


app.add_handler(handler=ChatJoinRequestHandler(callback=join_req_msg))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, callback=reply_message))

# async def main():
#     await app.initialize()
#     await app.start()
#     await app.updater.start_polling()
#
#     await asyncio.Event().wait()
#
# if __name__ == "__main__":
#     asyncio.run(main())


# Flask webhook route

@flask_app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, app.bot)
    asyncio.create_task(app.update_queue.put(update))  # Add update to bot queue
    return "OK", 200

@flask_app.route("/")
def index():
    return "Bot is running!", 200

# ---------------- Start everything ---------------- #

async def start_bot():
    await app.initialize()
    await app.start()
    # Set webhook
    url = os.environ.get("RENDER_EXTERNAL_URL")
    await app.bot.set_webhook(f"{url}/{TOKEN}")



asyncio.get_event_loop().create_task(start_bot())
