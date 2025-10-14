# core/admin_handler.py
from telebot import types
from config import ADMIN_ID
from mongo_storage import storage

def register(bot):
    @bot.message_handler(commands=['cleardb'])
    def clear_database(message):
        if message.from_user.id != ADMIN_ID:
            bot.send_message(message.chat.id, "🚫 ليس لديك صلاحية استخدام هذا الأمر.")
            return
        storage.clear_all_users()
        bot.send_message(message.chat.id, "✅ تم مسح جميع المستخدمين من قاعدة البيانات بنجاح.")

    @bot.message_handler(commands=['addcoins'])
    def add_coins_cmd(message):
        if message.from_user.id != ADMIN_ID:
            return
        try:
            _, uid, amount = message.text.split()
            uid = int(uid)
            amount = int(amount)
            storage.add_coins(uid, amount)
            bot.send_message(ADMIN_ID, f"✅ تمت إضافة {amount}💰 إلى المستخدم {uid}")
        except Exception as e:
            bot.send_message(ADMIN_ID, f"⚠️ تنسيق خاطئ. استخدم: /addcoins <id> <amount>\n{e}")

    @bot.message_handler(commands=['setrespect'])
    def set_respect_cmd(message):
        if message.from_user.id != ADMIN_ID:
            return
        try:
            _, uid, value = message.text.split()
            uid = int(uid)
            value = int(value)
            storage.update_user(uid, {"respect": value})
            bot.send_message(ADMIN_ID, f"✅ تم تعيين احترام المستخدم {uid} إلى {value}")
        except Exception as e:
            bot.send_message(ADMIN_ID, f"⚠️ تنسيق خاطئ. استخدم: /setrespect <id> <value>\n{e}")

    @bot.message_handler(commands=['users'])
    def show_users_count(message):
        if message.from_user.id != ADMIN_ID:
            return
        count = storage.get_total_users()
        bot.send_message(ADMIN_ID, f"👥 عدد المستخدمين المسجلين حاليًا: <b>{count}</b>", parse_mode="HTML")
