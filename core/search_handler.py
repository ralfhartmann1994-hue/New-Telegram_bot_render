from telebot.types import Message, ReplyKeyboardRemove
from core.utils import ensure_user_extended, get_user, update_user
from core.keyboards import topics_menu, gender_menu, main_menu
from core.matchmaking import add_to_wait, try_match, start_timeout_watcher
from messages import get_category_welcome
import time, traceback

COINS_SEARCH_GIRL = int(__import__("os").environ.get("COINS_SEARCH_GIRL", "25"))

def register(bot):
    @bot.message_handler(func=lambda m: m.text == "🔍 البحث عن دردشة")
    def cmd_search(m: Message):
        uid = m.from_user.id
        u = ensure_user_extended(uid, telegram_user=m.from_user)
        if u.get("partner"):
            bot.send_message(uid, "⚠️ أنت بالفعل في دردشة!", reply_markup=main_menu())
            return
        update_user(uid, {"state": "CHOOSE_TOPIC"})
        bot.send_message(uid, "اختر موضوع النقاش:", reply_markup=topics_menu())

    @bot.message_handler(func=lambda m: get_state_for(m.from_user.id) == "CHOOSE_TOPIC")
    def on_topic_choice(m: Message):
        uid = m.from_user.id
        txt = (m.text or "")
        if txt == "🔙 العودة":
            update_user(uid, {"state": None})
            bot.send_message(uid, "تم الإلغاء.", reply_markup=main_menu())
            return
        # map the displayed label to internal topic id
        topic_map = {
            "⚽ رياضة": "sports",
            "🗳️ سياسة": "politics",
            "🎬 أفلام": "movies",
            "🎮 ألعاب": "games",
            "🎭 عشوائي": "random",
            "💬 تعارف": "social",
        }
        topic = topic_map.get(txt)
        if not topic:
            bot.send_message(uid, "اختر من الأزرار.", reply_markup=topics_menu())
            return
        update_user(uid, {"topic": topic, "state": "CHOOSE_TARGET_GENDER"})
        bot.send_message(uid, get_category_welcome(topic))
        # send category sticker if available — handled by matchmaking module or stickers file
        time.sleep(0.5)
        bot.send_message(uid, "الآن اختر جنس الطرف الذي تريد:", reply_markup=gender_menu())

    @bot.message_handler(func=lambda m: get_state_for(m.from_user.id) == "CHOOSE_TARGET_GENDER")
    def on_target_choice(m: Message):
        uid = m.from_user.id
        txt = (m.text or "")
        if txt == "🔙 العودة":
            update_user(uid, {"state": None, "topic": None})
            bot.send_message(uid, "تم الإلغاء.", reply_markup=main_menu())
            return
        target = "female" if "بنت" in txt or "👧" in txt else "male"
        # if female and costs coins
        if "بنت" in txt:
            ok = __import__("mongo_storage").deduct_coins(uid, COINS_SEARCH_GIRL)
            if not ok:
                bot.send_message(uid, "رصيدك غير كافٍ.", reply_markup=main_menu())
                update_user(uid, {"state": None})
                return
        # set searching state and search_start timestamp
        now = int(time.time())
        update_user(uid, {"state": "SEARCHING", "target_gender": target, "search_start": now})
        # add to matchmaking queue
        try:
            add_to_wait(topic= (get_user(uid) or {}).get("topic"), uid=uid, target=target)
            # try immediate match
            partner = try_match(uid, (get_user(uid) or {}).get("topic"))
            if partner:
                pid = int(partner)
                now = int(time.time())
                update_user(uid, {"partner": pid, "state": None, "chat_started_at": now})
                update_user(pid, {"partner": uid, "state": None, "chat_started_at": now})
                bot.send_message(uid, "✅ تم العثور على شريك! ابدأ المحادثة.", reply_markup=ReplyKeyboardRemove())
                bot.send_message(pid, "✅ تم العثور على شريك! ابدأ المحادثة.", reply_markup=ReplyKeyboardRemove())
            else:
                bot.send_message(uid, "🔍 جاري البحث... سنخبرك عند العثور على شريك.", reply_markup=main_menu())
        except Exception as e:
            print(f"[search_handler ERROR] {e}")
            bot.send_message(uid, "⚠️ حدث خطأ أثناء بدء البحث.", reply_markup=main_menu())

# helper to get state
def get_state_for(uid):
    try:
        from mongo_storage import get_user
        u = get_user(uid)
        return u.get("state")
    except Exception:
        return None
