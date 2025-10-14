# Moderation.py
from datetime import datetime, timedelta
from mongo_storage import MongoStorage
from bad_words import BAD_WORDS
from config import (
    RESPECT_PENALTY_PER_BADWORD,
    PARTIAL_BAN_THRESHOLD,
    PARTIAL_BAN_DAYS,
    FULL_BAN_THRESHOLD
)

db = MongoStorage()

def contains_bad_word(text: str):
    if not text:
        return False
    text_lower = text.lower()
    # return list of words found or boolean — بعض الأكواد تتوقع قائمة، بعضها boolean
    found = [w for w in BAD_WORDS if w in text_lower]
    return found if found else []

def censor_text(text: str):
    # بسيط: استبدال كل كلمة مسيئة بنجمات (يمكن تحسينه لاحقًا)
    if not text:
        return text
    censored = text
    for w in BAD_WORDS:
        censored = censored.replace(w, '*' * len(w))
    return censored

def apply_respect(uid: int, text: str):
    # اختياري: إخطار سجل/تخفيض نقاط بناءً على الرسائل (مكمل للمشروع)
    return 0

def check_message_for_badwords(uid: int, text: str) -> int:
    if not text:
        return 0
    text_lower = text.lower()
    bad_count = sum(1 for w in BAD_WORDS if w in text_lower)
    if bad_count > 0:
        penalty = bad_count * RESPECT_PENALTY_PER_BADWORD
        user = db.ensure_user(uid)
        new_respect = max(0, user.get("respect", 100) - penalty)
        db.update_user(uid, {"respect": new_respect})
        check_for_ban(uid, new_respect)
    return bad_count

def check_for_ban(uid: int, respect: int):
    user = db.ensure_user(uid)
    if respect <= FULL_BAN_THRESHOLD:
        db.update_user(uid, {"banned_full": True, "banned_until": None})
        print(f"[BAN] user {uid} fully banned (respect={respect})")
        return "full"
    elif respect <= PARTIAL_BAN_THRESHOLD:
        until = int((datetime.utcnow() + timedelta(days=PARTIAL_BAN_DAYS)).timestamp())
        db.update_user(uid, {"banned_full": False, "banned_until": until})
        print(f"[BAN] user {uid} partially banned until {until} (respect={respect})")
        return "partial"
    else:
        # clear ban if any
        if user.get("banned_until") or user.get("banned_full"):
            db.update_user(uid, {"banned_full": False, "banned_until": None})
        return None
