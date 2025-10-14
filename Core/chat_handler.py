# core/chat_handler.py
import time
from telebot import types
from mongo_storage import ensure_user, get_user, append_history
from Moderation import check_message_for_badwords, censor_text

def register(bot):
    # فقط استقبل الرسائل النصية عندما المستخدم في دردشة فعلية مع شريك
    @bot.message_handler(func=lambda m: (ensure_user(m.from_user.id).get("partner") is not None and ensure_user(m.from_user.id).get("state") in (None, "REGISTERED")), content_types=["text"])
    def chat_router(message):
        uid = message.from_user.id
        txt = (message.text or "").strip()
        user = ensure_user(uid)
        pid = user.get("partner")
        if not pid:
            # هذه الحالة نادرًا ستصل هنا لأن الفلتر أعلاه يتحقق، لكن امانًا:
            bot.send_message(uid, "⚠️ لست في محادثة حالياً.")
            return

        # تحقق من حظر أو كتم
        if user.get("banned_full"):
            bot.send_message(uid, "🚫 لا يمكنك التحدث حالياً لأن حسابك محظور.")
            return
        if user.get("muted_until") and int(user.get("muted_until")) > int(time.time()):
            remaining = int(int(user.get("muted_until")) - time.time())
            bot.send_message(uid, f"🔇 أنت مكتوم لوقت {remaining} ثانية.")
            return

        # فلترة الإساءة
        bad_count = check_message_for_badwords(uid, txt)
        if bad_count > 0:
            txt_to_send = censor_text(txt)
            bot.send_message(uid, "⚠️ تم تعديل رسالتك لاحتوائها على كلمات غير لائقة.")
        else:
            txt_to_send = txt

        # حفظ السجل للطرفين
        try:
            append_history(uid, {"ts": int(time.time()), "text": txt_to_send, "from": uid})
            append_history(pid, {"ts": int(time.time()), "text": txt_to_send, "from": uid})
        except Exception:
            pass

        # إرسال الطرف الآخر
        try:
            bot.send_message(pid, f"💬 {txt_to_send}")
        except Exception as e:
            print(f"[SEND ERROR] {e}")
            bot.send_message(uid, "⚠️ حدث خطأ أثناء إرسال الرسالة.")
