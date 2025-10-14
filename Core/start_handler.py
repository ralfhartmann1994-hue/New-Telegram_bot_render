# core/start_handler.py
from telebot import types
import re
import uuid
import time
from config import COINS_REFERRAL, ADMIN_ID
from mongo_storage import ensure_user, update_user, find_by_ref_code, add_coins, get_user, create_user_if_not_exists, storage
from core.keyboards import main_menu, gender_menu
from stickers import WELCOME_STICKER, AFTER_NAME_STICKER, NABEEL_YOUNG_STICKER
from messages import WELCOME_MSG, ASK_NAME, ASK_GENDER, ASK_AGE, TOO_YOUNG_MSG
from core.utils import is_user_fully_registered


def register(bot):
    """تسجيل جميع مراحل التسجيل"""

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        uid = message.from_user.id
        # تأكد من وجود المستخدم (لننشئ doc افتراضي)
        user = ensure_user(uid)

        # فحص الإحالة (رابط الدعوة)
        parts = message.text.strip().split()
        referrer_id = None
        if len(parts) > 1:
            code = parts[1].strip()
            inviter = find_by_ref_code(code)
            if inviter and inviter.get("user_id") != uid:
                referrer_id = inviter.get("user_id")
                # بنعطي الداعي مكافأة لاحقًا عند إكمال التسجيل المدعو (أو الآن)
                # هنا نعلّم الحقل referrer
                update_user(uid, {"referrer": referrer_id})

        # مستخدم جديد — بدء التسجيل (أو اكتمال ناقص)
        if not is_user_fully_registered(user):
            update_user(uid, {"state": "ASK_NAME"})
            # ارسل ستيكر وسؤال الاسم
            try:
                bot.send_sticker(uid, WELCOME_STICKER)
            except Exception:
                pass
            bot.send_message(uid, WELCOME_MSG)
            bot.send_message(uid, ASK_NAME)
        else:
            bot.send_message(uid, "👋 مرحباً بعودتك!", reply_markup=main_menu())

    # =================================
    # مرحلة الاسم
    # =================================
    @bot.message_handler(func=lambda m: get_state(m.from_user.id) == "ASK_NAME")
    def handle_name(message):
        uid = message.from_user.id
        name = message.text.strip()
        if not (3 <= len(name) <= 30):
            bot.send_message(uid, "❌ الاسم يجب أن يكون بين 3 و 30 حرفًا. حاول مرة أخرى:")
            return
        if not re.match(r"^[A-Za-zأ-ي\s]+$", name):
            bot.send_message(uid, "❌ الاسم يجب أن يحتوي على أحرف فقط بدون أرقام أو رموز.")
            return
        update_user(uid, {"name": name, "state": "ASK_GENDER"})
        try:
            bot.send_sticker(uid, AFTER_NAME_STICKER)
        except Exception:
            pass
        bot.send_message(uid, ASK_GENDER, reply_markup=gender_menu())

    # =================================
    # مرحلة الجنس
    # =================================
    @bot.message_handler(func=lambda m: get_state(m.from_user.id) == "ASK_GENDER")
    def handle_gender(message):
        uid = message.from_user.id
        gender_text = message.text.strip()
        if "👦" in gender_text or "ذكر" in gender_text:
            gender = "male"
        elif "👧" in gender_text or "بنت" in gender_text or "أنثى" in gender_text:
            gender = "female"
        else:
            bot.send_message(uid, "❌ الرجاء اختيار الجنس من الأزرار.")
            return
        update_user(uid, {"gender": gender, "state": "ASK_AGE"})
        bot.send_message(uid, ASK_AGE)

    # =================================
    # مرحلة العمر
    # =================================
    @bot.message_handler(func=lambda m: get_state(m.from_user.id) == "ASK_AGE")
    def handle_age(message):
        uid = message.from_user.id
        try:
            age = int(message.text.strip())
        except ValueError:
            bot.send_message(uid, "❌ أدخل رقمًا صحيحًا لعُمرك.")
            return
        if not (10 <= age <= 99):
            bot.send_message(uid, "❌ أدخل عمرك الحقيقي (بين 10 و 99).")
            return

        # حدثنا الحقل "age" وحالة التسجيل
        update_user(uid, {"age": age, "state": "REGISTERED"})

        # الآن نكمل إعداد الملف الرسمي (احترام + عملات + كود دعوة إن لم يكن)
        user = get_user(uid) or {}
        # referral_code: أنشئ إن لم يكن
        referral_code = user.get("referral_code") or storage.generate_unique_ref_code()

        respect = 80
        base_coins = int(__import__("os").environ.get("COINS_NEW_USER", "100"))
        referrer = user.get("referrer")

        if referrer:
            # إذا كان لديه مدعو (انضم عبر كود)، أعطه مكافأة +50 وبنفس الوقت لكل من الداعي أيضاً:
            bonus = int(__import__("os").environ.get("COINS_REFERRAL", "50"))
            # منح المدعو
            storage.add_coins(uid, base_coins + bonus)
            # منح الداعي
            storage.add_coins(referrer, bonus)
            coins_final = storage.get_coins(uid)
        else:
            storage.add_coins(uid, base_coins)
            coins_final = storage.get_coins(uid)

        # حفظ الحقول النهائية
        update_user(uid, {
            "respect": respect,
            "referral_code": referral_code,
            "coins": coins_final,
            "registered_at": int(time.time())
        })

        if age < 20:
            bot.send_message(uid, "اهلا بالكتكوت الصغير 🤭")
            try:
                bot.send_sticker(uid, NABEEL_YOUNG_STICKER)
            except Exception:
                pass

        bot.send_message(
            uid,
            "✅ تم إنشاء ملفك الشخصي بنجاح!\nيمكنك الآن البدء باستخدام البوت.",
            reply_markup=main_menu()
        )

    # =================================
    def get_state(uid: int):
        u = ensure_user(uid)
        return u.get("state")
