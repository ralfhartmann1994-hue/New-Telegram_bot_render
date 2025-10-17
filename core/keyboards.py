# core/keyboards.py
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("🔍 البحث عن دردشة"))
    kb.row(KeyboardButton("🧾 ملفي"), KeyboardButton("💰 رصيدي"))
    kb.row(KeyboardButton("🎯 دعوة الأصدقاء"), KeyboardButton("✉️ تواصل مع الدعم"))
    return kb

def profile_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("👤 عرض ملفي"), KeyboardButton("✏️ تعديل الاسم"))
    kb.row(KeyboardButton("🎂 تعديل العمر"), KeyboardButton("🔙 العودة"))
    return kb

def balance_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("💰 رصيدي: عرض"), KeyboardButton("🎁 احصل على كوينز مجانا"))
    kb.row(KeyboardButton("🔙 العودة"))
    return kb

def gender_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row(KeyboardButton("👦 شاب"), KeyboardButton("👧 بنت"))
    return kb

def target_gender_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # تظهر الفتاة مع سعر البحث (كما طلبت)
    kb.row(KeyboardButton("👦 شاب"), KeyboardButton("👩 بنت (25 🪙)"))
    kb.row(KeyboardButton("🔙 العودة"))
    return kb

def topics_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # الفئات التي طلبت: رياضة سياسة دين فلسفة تعارف افلام
    kb.row(KeyboardButton("رياضة ⚽"), KeyboardButton("سياسة 🗳️"))
    kb.row(KeyboardButton("دين ☪️"), KeyboardButton("فلسفة 🤔"))
    kb.row(KeyboardButton("تعارف 💬"), KeyboardButton("افلام 🎬"))
    kb.row(KeyboardButton("🔙 العودة"))
    return kb

def searching_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("❌ إلغاء البحث"))
    return kb

def yes_no_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row(KeyboardButton("نعم ✅"), KeyboardButton("لا ❌"))
    return kb 
