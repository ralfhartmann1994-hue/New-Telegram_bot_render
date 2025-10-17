from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("🔍 البحث عن دردشة"))
    kb.row(KeyboardButton("🧾 ملفي"), KeyboardButton("💰 رصيدي"))
    kb.row(KeyboardButton("📝 تعديل الاسم"), KeyboardButton("🎂 تعديل العمر"))
    kb.row(KeyboardButton("🔗 دعوة الأصدقاء"), KeyboardButton("📞 تواصل مع الدعم"))
    return kb

def profile_menu():
    # داخل "ملفي" - يظهر معلومات وأزرار تعديل / عودة
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row(KeyboardButton("✏️ تعديل الاسم"), KeyboardButton("🔙 العودة"))
    return kb

def balance_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row(KeyboardButton("💰 احصل على كوينز مجانا"), KeyboardButton("🔙 العودة"))
    return kb

def gender_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row(KeyboardButton("👦 شاب"), KeyboardButton("👧 بنت (25🪙)"))
    kb.row(KeyboardButton("🔙 العودة"))
    return kb

def topics_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row(KeyboardButton("⚽ رياضة"), KeyboardButton("🗳️ سياسة"), KeyboardButton("🎬 أفلام"))
    kb.row(KeyboardButton("💬 تعارف"), KeyboardButton("🎭 عشوائي"), KeyboardButton("🎮 ألعاب"))
    kb.row(KeyboardButton("🔙 العودة"))
    return kb

def yes_no_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row(KeyboardButton("نعم ✅"), KeyboardButton("لا ❌"))
    return kb
