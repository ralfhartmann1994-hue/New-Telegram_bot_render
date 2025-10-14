# ============================================================
# matchmaking.py — نظام البحث والمطابقة بين المستخدمين
# ============================================================

import random
import time
from telebot import types
from mongo_storage import ensure_user, update_user, get_coins, deduct_coins
from core.keyboards import target_gender_menu, main_menu
from messages import CATEGORY_WELCOME
from stickers import movies, putin_politics, barca_celebration

# ✅ أسماء الستيكرات الأخرى التي ستضيفها لاحقًا في ملف stickers.py
STICKER_BY_CATEGORY = {
    "تعارف": "taarof_welcome",     # أضف لاحقاً في stickers.py
    "ألعاب": "games_fun",          # أضف لاحقاً
    "أفلام": movies,               # موجود
    "سياسة": putin_politics,       # موجود
    "عشوائي": "random_chat",       # أضف لاحقاً
    "رياضة": barca_celebration     # موجود
}

# المستخدمون المنتظرون للمطابقة
waiting_users = {}


def register(bot):
    # 1️⃣ عند الضغط على فئة دردشة
    @bot.message_handler(func=lambda m: m.text in CATEGORY_WELCOME.keys())
    def handle_category_selection(message):
        uid = message.from_user.id
        category = message.text.strip()

        user = ensure_user(uid)
        update_user(uid, {"topic": category})

        # رسالة ترحيب عشوائية للفئة
        welcome_text = random.choice(CATEGORY_WELCOME.get(category, ["👋 مرحباً بك!"]))
        bot.send_message(uid, welcome_text)

        # إرسال ستيكر الفئة
        sticker = STICKER_BY_CATEGORY.get(category)
        if sticker:
            try:
                bot.send_sticker(uid, sticker)
            except Exception:
                bot.send_message(uid, "🎭 (الستيكر لهذه الفئة غير متاح حالياً)")

        # عرض كيبورد اختيار الجنس
        time.sleep(0.8)
        bot.send_message(uid, "👥 اختر من تريد الدردشة معه:", reply_markup=target_gender_menu())

    # 2️⃣ اختيار الجنس
    @bot.message_handler(func=lambda m: m.text in ["👦 شاب", "👧 بنت (25🪙)"])
    def handle_gender_target(message):
        uid = message.from_user.id
        user = ensure_user(uid)

        if message.text.startswith("👧"):
            cost = 25
            if get_coins(uid) < cost:
                bot.send_message(uid, "❌ لا تمتلك ما يكفي من الكوينز لاختيار فتاة. تحتاج 25💰.")
                bot.send_message(uid, "🔙 عد إلى القائمة.", reply_markup=main_menu())
                return
            deduct_coins(uid, cost)
            target = "female"
        else:
            target = "male"

        update_user(uid, {"target_gender": target})
        bot.send_message(uid, "🔎 جاري البحث عن شريك مناسب لك...",
                         reply_markup=cancel_search_button())

        start_search(bot, uid)

    # 3️⃣ زر إلغاء البحث
    @bot.message_handler(func=lambda m: m.text == "❌ إلغاء البحث")
    def cancel_search(message):
        uid = message.from_user.id
        if uid in waiting_users:
            del waiting_users[uid]
        update_user(uid, {"state": "REGISTERED", "topic": None})
        bot.send_message(uid, "❌ تم إلغاء البحث والعودة للقائمة.", reply_markup=main_menu())

    # 4️⃣ العودة من أي مكان
    @bot.message_handler(func=lambda m: m.text == "🔙 العودة للقائمة")
    def handle_back(message):
        uid = message.from_user.id
        update_user(uid, {"state": "REGISTERED", "topic": None})
        bot.send_message(uid, "🔙 تم الرجوع إلى القائمة الرئيسية.", reply_markup=main_menu())


# ============================================================
# نظام البحث والمطابقة
# ============================================================

def start_search(bot, uid):
    """بدء البحث عن شريك"""
    user = ensure_user(uid)
    gender = user.get("gender")
    target = user.get("target_gender")
    topic = user.get("topic")

    if not gender or not target:
        bot.send_message(uid, "⚠️ بياناتك غير مكتملة.")
        return

    # ابحث عن شريك مناسب
    for partner, data in list(waiting_users.items()):
        if data["gender"] == target and data["target_gender"] == gender and data["topic"] == topic:
            # تم إيجاد شريك
            del waiting_users[partner]
            update_user(uid, {"partner": partner})
            update_user(partner, {"partner": uid})

            bot.send_message(uid, f"🎉 تم العثور على شريك للدردشة في فئة {topic}! 🧍‍♂️↔️🧍‍♀️")
            bot.send_message(partner, f"🎉 تم العثور على شريك للدردشة في فئة {topic}! 🧍‍♂️↔️🧍‍♀️")

            return

    # لا يوجد شريك، أضف إلى الانتظار
    waiting_users[uid] = {"gender": gender, "target_gender": target, "topic": topic}
    bot.send_message(uid, "⌛ لم يتم العثور على شريك بعد، سيتم إعلامك عند توفر شخص مناسب.")


def cancel_search_button():
    """زر إلغاء البحث"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❌ إلغاء البحث"))
    return markup
