# core/keyboards.py
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu(in_chat=False):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🔍 البحث عن دردشة"))
    kb.row(KeyboardButton("🧾 ملفي"), KeyboardButton("💰 رصيدي"))
    kb.row(KeyboardButton("🧑‍🤝‍🧑 دعوة الأصدقاء"), KeyboardButton("📞 تواصل مع الدعم"))
    # عند وجود دردشة - يمكن إضافة زر للغادر
    if in_chat:
        kb.add(KeyboardButton("🚪 مغادرة الدردشة"))
        kb.add(KeyboardButton("🚨 إبلاغ"))
    return kb

def profile_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("✏️ تعديل الاسم"), KeyboardButton("✏️ تعديل العمر"))
    kb.add(KeyboardButton("🔙 العودة"))
    return kb

def balance_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("احصل على كوينز مجانا"))
    kb.add(KeyboardButton("🔙 العودة"))
    return kb

def gender_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("👦 شاب"), KeyboardButton("👧 بنت"))
    return kb

def target_gender_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("👦 شاب"), KeyboardButton("👧 بنت (25🪙)"))
    kb.add(KeyboardButton("🔙 العودة"))
    return kb

def topics_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("رياضة ⚽"), KeyboardButton("سياسة 🗳️"))
    kb.add(KeyboardButton("دين ☪️"), KeyboardButton("فلسفة 🤔"))
    kb.add(KeyboardButton("تعارف 💬"), KeyboardButton("افلام 🎬"))
    kb.add(KeyboardButton("🔙 العودة"))
    return kb
