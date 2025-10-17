# core/chat_handler.py
import time
import traceback
from mongo_storage import ensure_user, get_user, append_history
from Moderation import check_message_for_badwords, censor_text

def register(bot):
    # هذا المعالج يستقبل الرسائل النصية فقط عندما يكون المستخدم في محادثة (partner موجود)
    @bot.message_handler(func=lambda m: True, content_types=["text"])
    def chat_router(message):
        uid = message.from_user.id
        try:
            user = ensure_user(uid)
        except Exception as e:
            print(f"[chat_router ensure_user ERROR] {e}")
            return

        # إذا المستخدم في وضع تسجيل (state != None و != "REGISTERED") فلا نتعامل هنا
        state = user.get("state")
        if state and state != "REGISTERED":
            # لا نعالج هنا — هناك معالجات خاصة بالحالة في start_handler أو غيره
            return

        # التحقق إن المستخدم داخل محادثة حالية مع شريك
        partner_id = user.get("partner") or user.get("chat_partner")  # مرونة في أسماء الحقول
        if not partner_id:
            # لا نرد برسالة عامة "لست في محادثة حالياً" هنا لأن ذلك يضرب تجربة التسجيل/الأوامر
            return

        txt = (message.text or "").strip()
        # تحقق الحظر/الكتامة
        if user.get("banned_full") or user.get("banned"):
            bot.send_message(uid, "🚫 لا يمكنك التحدث حالياً لأن حسابك مقيد.")
            return

        # فحص كلمات مسيئة وتعديل النص إن لزم
        bad_count = 0
        try:
            bad_count = check_message_for_badwords(uid, txt)
        except Exception:
            pass
        if bad_count > 0:
            txt = censor_text(txt)
            bot.send_message(uid, "⚠️ تم تعديل رسالتك لاحتوائها على كلمات غير لائقة.")

        # حفظ السجل
        try:
            append_history(uid, {"ts": int(time.time()), "text": txt, "from": uid})
            append_history(partner_id, {"ts": int(time.time()), "text": txt, "from": uid})
        except Exception as e:
            print(f"[chat_router append_history ERROR] {e}")

        # إرسال الرسالة للشريك
        try:
            bot.send_message(partner_id, f"💬 {txt}")
        except Exception as e:
            print(f"[chat_router SEND ERROR] {e}")
            bot.send_message(uid, "⚠️ حدث خطأ أثناء إرسال الرسالة إلى الشريك.") 
