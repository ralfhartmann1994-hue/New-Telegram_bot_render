# ============================================================
# utils.py — أدوات مساعدة عامة
# ============================================================

from mongo_storage import ensure_user, update_user


def ensure_user_extended(uid, telegram_user=None):
    user = ensure_user(uid)
    updates = {}
    if telegram_user:
        updates["username"] = telegram_user.username
        updates["first_name"] = telegram_user.first_name
    if updates:
        update_user(uid, updates)
    return user


def is_user_fully_registered(user: dict) -> bool:
    if not user:
        return False
    return all(user.get(k) for k in ["name", "gender", "age"])


def safe_get(value, default=None):
    return value if value is not None else default 
