# core/setup.py
import telebot
from flask import Flask, request
import traceback
import config
from MongoStorage import MongoStorage
from core import handlers, matchmaking, reports, admin
from core.utils import start_timeout_watcher

bot = telebot.TeleBot(config.BOT_TOKEN)
app = Flask(__name__)
mongo_storage = MongoStorage()

# تسجيل كل ملفات الهاندلر
handlers.register_handlers(bot, mongo_storage)
matchmaking.register_handlers(bot, mongo_storage)
reports.register_handlers(bot, mongo_storage)
admin.register_handlers(bot, mongo_storage)

@app.route(f"/{getattr(config, 'WEBHOOK_PATH', 'webhook')}", methods=["POST"])
def webhook():
    try:
        update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
        bot.process_new_updates([update])
    except Exception as e:
        print(f"[WEBHOOK PROCESS ERROR] {e}\n{traceback.format_exc()}")
    return "", 200

def set_webhook():
    url = getattr(config, "WEBHOOK_URL", None)
    path = getattr(config, "WEBHOOK_PATH", "webhook")
    if not url:
        print("[WEBHOOK] WEBHOOK_URL not set; skipping webhook setup")
        return
    try:
        bot.remove_webhook()
    except Exception:
        pass
    bot.set_webhook(f"{url}/{path}")
    print(f"[WEBHOOK] Set to {url}/{path}")
