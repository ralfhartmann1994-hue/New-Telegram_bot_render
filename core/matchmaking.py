# ============================================================
# core/matchmaking.py — نظام البحث والمطابقة بين المستخدمين
# ============================================================

import time
from telebot import types
from mongo_storage import ensure_user, update_user
from core.keyboards import target_gender_menu
from stickers import STICKERS
from messages import CATEGORY_WELCOME


def register(bot):
    @bot.message_handler(func=lambda m: m.text in ["💬 تعارف", "🎮 ألعاب", "🎭 عشوائي", "⚽ رياضة", "🎬 أفلام", "🗳️ سياسة"])
    def handle_category(message):
        uid = message.from_user.id
        user = ensure_user(uid)

        category_map = {
            "🎬 أفلام": ("movies", STICKERS["movies"]),
            "🗳️ سياسة": ("politics", STICKERS["putin_politics"]),
            "⚽ رياضة": ("sports", STICKERS["barca_celebration"]),
            "🎮 ألعاب": ("games", None),
            "🎭 عشوائي": ("random", None),
            "💬 تعارف": ("random", None),
        }

        category_key, sticker = category_map.get(message.text, ("random", None))
        update_user(uid, {"topic": category_key})

        welcome_msg = CATEGORY_WELCOME.get(category_key, "💬 دردشة ممتعة!")
        bot.send_message(uid, welcome_msg)

        if sticker:
            try:
                bot.send_sticker(uid, sticker)
            except Exception:
                pass

        time.sleep(1)
        bot.send_message(uid, "من ترغب أن تتحدث معه؟", reply_markup=target_gender_menu())
