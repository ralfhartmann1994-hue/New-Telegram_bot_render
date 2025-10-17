from telebot.types import Message
from core.utils import ensure_user_extended, get_user, update_user
from core.keyboards import main_menu, profile_menu, balance_menu
import re

def register(bot):
    # عرض الملف عند الضغط على زر "🧾 ملفي" أو أوامر /profile
    @bot.message_handler(commands=['profile'])
    def cmd_profile(m: Message):
        uid = m.from_user.id
        u = ensure_user_extended(uid, telegram_user=m.from_user)
        if not u or not u.get("user_id"):
            bot.send_message(uid, "⚠️ حدث خطأ؛ أعد /start.")
            return
        # بناء نص الملف
        name = u.get("name") or "غير محدد"
        age = u.get("age") or "غير محدد"
        gender = u.get("gender") or "غير محدد"
        respect = u.get("respect", "--")
        coins = u.get("coins", 0)
        txt = (f"👤 ملفك الشخصي\n• الاسم: {name}\n• العمر: {age}\n• الجنس: {gender}\n"
               f"• الاحترام: ⭐ {respect}\n• الرصيد: 🪙 {coins}")
        bot.send_message(uid, txt, reply_markup=profile_menu())

    # زر ملفي من لوحة رئيسية
    @bot.message_handler(func=lambda m: m.text == "🧾 ملفي")
    def on_profile_btn(m: Message):
        return cmd_profile(m)

    # تعديل الاسم — ندخل في حالة خاصة
    @bot.message_handler(func=lambda m: m.text == "✏️ تعديل الاسم")
    def ask_new_name(m: Message):
        uid = m.from_user.id
        u = ensure_user_extended(uid, telegram_user=m.from_user)
        if not u or not u.get("user_id"):
            bot.send_message(uid, "⚠️ أعد /start.")
            return
        update_user(uid, {"state": "EDIT_NAME"})
        bot.send_message(uid, "✏️ أرسل اسمك الجديد (أو اضغط 🔙 العودة لإلغاء):")

    @bot.message_handler(func=lambda m: get_state_for(m.from_user.id) == "EDIT_NAME")
    def receive_new_name(m: Message):
        uid = m.from_user.id
        text = (m.text or "").strip()
        if text == "🔙 العودة":
            update_user(uid, {"state": None})
            bot.send_message(uid, "❌ تم إلغاء تعديل الاسم.", reply_markup=main_menu())
            return
        # validate name
        if not (2 <= len(text) <= 30) or not re.match(r"^[A-Za-zأ-ي\s]+$", text):
            bot.send_message(uid, "❌ الاسم غير صالح. استخدم فقط أحرف (2-30). حاول مرة أخرى:")
            return
        update_user(uid, {"name": text, "state": None})
        bot.send_message(uid, f"✅ تم تحديث اسمك إلى: {text}", reply_markup=main_menu())

    # تعديل العمر
    @bot.message_handler(func=lambda m: m.text == "🎂 تعديل العمر")
    def ask_new_age(m: Message):
        uid = m.from_user.id
        update_user(uid, {"state": "EDIT_AGE"})
        bot.send_message(uid, "🎂 أرسل عمرك الجديد (أو اضغط 🔙 العودة لإلغاء):")

    @bot.message_handler(func=lambda m: get_state_for(m.from_user.id) == "EDIT_AGE")
    def receive_new_age(m: Message):
        uid = m.from_user.id
        text = (m.text or "").strip()
        if text == "🔙 العودة":
            update_user(uid, {"state": None})
            bot.send_message(uid, "❌ تم إلغاء تعديل العمر.", reply_markup=main_menu())
            return
        try:
            age = int(text)
        except ValueError:
            bot.send_message(uid, "❌ ادخل رقماً صالحاً للعمر:")
            return
        if not (10 <= age <= 99):
            bot.send_message(uid, "❌ العمر يجب أن يكون بين 10 و 99.")
            return
        update_user(uid, {"age": age, "state": None})
        bot.send_message(uid, f"✅ تم تحديث عمرك إلى: {age}", reply_markup=main_menu())

    # عرض الرصيد و زر احصل على كوينز
    @bot.message_handler(func=lambda m: m.text == "💰 رصيدي")
    def on_balance(m: Message):
        uid = m.from_user.id
        u = ensure_user_extended(uid, telegram_user=m.from_user)
        coins = u.get("coins", 0)
        txt = f"💰 رصيدك الحالي: {coins} 🪙\nاضغط 'احصل على كوينز مجانا' لرابط الدعوة."
        bot.send_message(uid, txt, reply_markup=balance_menu())

    @bot.message_handler(func=lambda m: m.text == "💰 احصل على كوينز مجانا" or m.text == "💰 احصل على كوينز مجانا")
    def give_ref_msg(m: Message):
        uid = m.from_user.id
        u = ensure_user_extended(uid, telegram_user=m.from_user)
        code = u.get("referral_code") or u.get("referral", "")
        bot.send_message(uid, f"احصل على 50 كوينز على كل صديق تدعوه.\nرابط دعوتك: https://t.me/YourBot?start={code}", reply_markup=balance_menu())

# مساعدة صغيرة: دالة لجلب الحالة الحالية من storage
def get_state_for(uid):
    try:
        u = ensure_user_extended(uid)
        return u.get("state")
    except Exception:
        # fallback to direct storage call if utils expose ensure_user differently
        try:
            from mongo_storage import get_user
            return get_user(uid).get("state")
        except Exception:
            return None
