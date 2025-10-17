# Main.py — نقطة الدخول: يحمّل bot ثم يسجل handlers عبر register(bot)
import os, traceback
import telebot
from flask import Flask, request
from mongo_storage import MongoStorage
import importlib

from config import BOT_TOKEN, WEBHOOK_URL, PORT, USE_WEBHOOK, WEBHOOK_PATH

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN غير معرف في environment")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
app = Flask(__name__)
db = MongoStorage()
print("[DB] ✅ MongoStorage جاهز.")

# نحمّل كل handlers هنا
try:
    import core.start_handler as start_handler
    import core.profile_handler as profile_handler
    import core.chat_handler as chat_handler
    import core.admin_handler as admin_handler
    import core.search_handler as search_handler      # ✅ تمت الإضافة الجديدة
    import core.matchmaking as matchmaking
    import core.keyboards as keyboards
except Exception as e:
    print(f"[IMPORT core ERROR] {e}")

# تسجيل كل handler
try:
    start_handler.register(bot)
    profile_handler.register(bot)
    chat_handler.register(bot)
    admin_handler.register(bot)
    search_handler.register(bot)                      # ✅ تسجيل البحث عن دردشة
    print("[REGISTER] ✅ تم تسجيل Handlers بنجاح.")
except Exception as e:
    print(f"[REGISTER ERROR] {e}")

# بدء مراقب المطابقة (30 دقيقة)
try:
    matchmaking.start_timeout_watcher(bot)
except Exception as e:
    print(f"[MATCHMAKING WATCHER ERROR] {e}")

# webhook endpoint
@app.route("/", methods=["GET"])
def home():
    return "Bot is running"

@app.route(f"/{WEBHOOK_PATH}", methods=["POST"])
def webhook():
    try:
        payload = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(payload)
        bot.process_new_updates([update])
    except Exception as e:
        print(f"[WEBHOOK PROCESS ERROR] {e}\n{traceback.format_exc()}")
    return "", 200

if __name__ == "__main__":
    if USE_WEBHOOK and WEBHOOK_URL:
        try:
            bot.remove_webhook()
        except Exception:
            pass
        try:
            bot.set_webhook(f"{WEBHOOK_URL}/{WEBHOOK_PATH}")
            print(f"[WEBHOOK] ✅ تم تعيين Webhook إلى: {WEBHOOK_URL}/{WEBHOOK_PATH}")
        except Exception as e:
            print(f"[WEBHOOK SET ERROR] {e}")
    else:
        raise RuntimeError("WEBHOOK_URL غير معرف أو USE_WEBHOOK False — البوت مضبوط للعمل على webhook فقط.")

    app.run(host="0.0.0.0", port=PORT)
