# core/profile_handler.py
from telebot import types
from mongo_storage import ensure_user, update_user, get_user
from core.keyboards import main_menu, profile_menu, balance_menu
from core.utils import is_user_fully_registered

def register(bot):
    @bot.message_handler(commands=['profile'])
    def handle_profile(message):
        uid = message.from_user.id
        user = ensure_user(uid)
        if not is_user_fully_registered(user):
            bot.send_message(uid, "⚠️ ملفك الشخصي غير مكتمل. أكمل التسجيل أولاً.")
            return

        profile_text = (
            f"🧾 ملفي:\n"
            f"• الاسم: {user.get('name','غير محدد')}\n"
            f"• الجنس: {user.get('gender','غير محدد')}\n"
            f"• العمر: {user.get('age','غير محدد')}\n"
            f"• الاحترام: ⭐ {user.get('respect',80)}\n"
            f"• رصيد: 💰 {user.get('coins',0)}"
        )
        bot.send_message(uid, profile_text, reply_markup=profile_menu())

    @bot.message_handler(func=lambda m: m.text == "🧾 ملفي")
    def show_profile_btn(message):
        return handle_profile(message)

    @bot.message_handler(func=lambda m: m.text == "✏️ تعديل الاسم")
    def set_name_step(message):
        uid = message.from_user.id
        bot.send_message(uid, "أرسل اسمك الجديد:")
        bot.register_next_step_handler(message, do_set_name)

    def do_set_name(message):
        uid = message.from_user.id
        new_name = message.text.strip()
        if len(new_name) < 2:
            bot.send_message(uid, "⚠️ الاسم قصير جدًا. حاول مجددًا.")
            return
        update_user(uid, {"name": new_name})
        bot.send_message(uid, f"✅ تم تحديث اسمك إلى: {new_name}", reply_markup=main_menu())

    @bot.message_handler(func=lambda m: m.text == "💰 رصيدي")
    def show_balance(message):
        uid = message.from_user.id
        user = ensure_user(uid)
        bot.send_message(uid, f"رصيدك: 💰 {user.get('coins',0)}", reply_markup=balance_menu())
