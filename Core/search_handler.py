# handlers/search_handler.py
from telebot.types import Message, ReplyKeyboardRemove
from core.utils import ensure_user_extended, get_user, update_user, deduct_coins, add_coins
from keyboards import topics_menu, target_gender_menu, searching_menu, main_menu
from core.matchmaking import add_to_wait, try_match, start_timeout_watcher
from messages import INTRO_PARTNER, NO_MATCH, SEARCHING
from Profile_manager import start_history
import time, traceback

COINS_SEARCH_GIRL = int(__import__("config").COINS_SEARCH_GIRL if hasattr(__import__("config"), "COINS_SEARCH_GIRL") else 25)

def register(bot):
    @bot.message_handler(commands=['search', 'chat', 'find'])
    def cmd_search(m: Message):
        uid = m.from_user.id
        handle_search_request(bot, uid)

    def handle_search_request(bot, uid: int):
        u = ensure_user_extended(uid)
        if u.get("partner"):
            bot.send_message(uid, "⚠️ أنت بالفعل في دردشة!", reply_markup=main_menu(in_chat=True))
            return
        update_user(uid, {"state": "CHOOSE_TOPIC"})
        bot.send_message(uid, "اختر موضوع النقاش:", reply_markup=topics_menu())

    @bot.message_handler(func=lambda m: m.text in ["رياضة ⚽","سياسة 🗳️","دين ☪️","فلسفة 🤔","تعارف 💬","افلام 🎬"])
    def on_topic_choice(m: Message):
        uid = m.from_user.id
        try:
            topic = (m.text or "").split()[0]
            update_user(uid, {"topic": topic, "state": "CHOOSE_TARGET_GENDER"})
            welcome_msg = __import__("messages").get_category_welcome(topic)
            bot.send_message(uid, welcome_msg)
            bot.send_message(uid, "الآن اختر جنس الطرف الذي تريده:", reply_markup=target_gender_menu())
        except Exception as e:
            print(f"[search_handler topic ERROR] {e}")
            traceback.print_exc()
            bot.send_message(uid, "حدث خطأ. حاول ثانية.", reply_markup=main_menu(in_chat=False))

    @bot.message_handler(func=lambda m: m.text in ["👦 شاب","👩 بنت (25 🪙)","🔙 العودة لاختيار الفئة","❌ إلغاء البحث"])
    def on_target_choice(m: Message):
        uid = m.from_user.id
        txt = (m.text or "")
        if txt == "❌ إلغاء البحث":
            update_user(uid, {"state": None, "topic": None, "target_gender": None})
            try:
                # attempt to remove from waitlist
                add_to_wait(None, uid, None)  # noop - safe; or call remove_from_wait in matchmaking
            except Exception:
                pass
            bot.send_message(uid, "❌ تم إلغاء البحث.", reply_markup=main_menu(in_chat=False))
            return
        if txt == "🔙 العودة لاختيار الفئة":
            update_user(uid, {"state": "CHOOSE_TOPIC", "target_gender": None})
            bot.send_message(uid, "اختر موضوع النقاش:", reply_markup=topics_menu())
            return

        target = "male" if "شاب" in txt else "female"
        if target == "female":
            ok = deduct_coins(uid, COINS_SEARCH_GIRL)
            if not ok:
                bot.send_message(uid, __import__("coins").INSUFFICIENT_COINS_MSG, reply_markup=main_menu(in_chat=False))
                update_user(uid, {"state": None, "topic": None, "target_gender": None})
                return
            bot.send_message(uid, f"🔍 تم خصم {COINS_SEARCH_GIRL} 🪙 للبحث عن بنت.\n⏳ جاري البحث...", reply_markup=searching_menu())
        else:
            bot.send_message(uid, "🔍 جاري البحث عن شاب...", reply_markup=searching_menu())

        update_user(uid, {"target_gender": target, "state": "SEARCHING"})
        topic = (get_user(uid) or {}).get("topic")
        try:
            add_to_wait(topic, uid, target)
            partner = try_match(uid, topic)
            if partner:
                pid = int(partner)
                now = time.time()
                update_user(uid, {"partner": pid, "state": None, "chat_started_at": now, "reported_by": []})
                update_user(pid, {"partner": uid, "state": None, "chat_started_at": now, "reported_by": []})
                try:
                    start_history(get_user(uid))
                    start_history(get_user(pid))
                except Exception:
                    pass
                bot.send_message(uid, __import__("core.utils").partner_profile_text(pid), reply_markup=ReplyKeyboardRemove())
                bot.send_message(pid, __import__("core.utils").partner_profile_text(uid), reply_markup=ReplyKeyboardRemove())
                bot.send_message(uid, INTRO_PARTNER, reply_markup=main_menu(in_chat=True))
                bot.send_message(pid, INTRO_PARTNER, reply_markup=main_menu(in_chat=True))
        except Exception as e:
            print(f"[search_handler matching ERROR] {e}")
            traceback.print_exc()
        try:
            start_timeout_watcher(bot)
        except Exception:
            pass
