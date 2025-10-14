# ============================================================
# keyboards.py — لوحات المفاتيح المختلفة للواجهة
# ============================================================

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🔍 البحث عن دردشة"))
    kb.add(KeyboardButton("🧾 الملف الشخصي"), KeyboardButton("💰 رصيدي"))
    kb.add(KeyboardButton("🤝 دعوة الأصدقاء"))
    kb.add(KeyboardButton("📞 التواصل مع الدعم"))
    return kb

def gender_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("👦 شاب"), KeyboardButton("👧 بنت"))
    return kb

def target_gender_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("👦 شاب"), KeyboardButton("👧 بنت (25💰)"))
    kb.add(KeyboardButton("🔙 العودة للقائمة"))
    return kb

def topics_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(
        KeyboardButton("💬 تعارف"),
        KeyboardButton("🎮 ألعاب"),
        KeyboardButton("🎭 عشوائي"),
        KeyboardButton("⚽ رياضة"),
        KeyboardButton("🎬 أفلام"),
        KeyboardButton("🗳️ سياسة")
    )
    kb.add(KeyboardButton("🔙 العودة للقائمة"))
    return kb
