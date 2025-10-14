# profile_manager.py
import re
from mongo_storage import MongoStorage

storage = MongoStorage()
NAME_RE = re.compile(r"^[\w\s\-]{2,30}$")

def ensure_user_status(user_id):
    u = storage.get_user(user_id)
    if not u:
        storage.create_user_if_not_exists(user_id)
        return "new"
    if not (u.get("name") and u.get("age") and u.get("gender")):
        return "incomplete"
    return "existing"

def set_name(user_id, name):
    storage.update_user(user_id, {"name": name})

def get_name(user_id):
    u = storage.get_user(user_id)
    return u.get("name") if u else None

def set_gender(user_id, gender):
    storage.update_user(user_id, {"gender": gender})

def get_gender(user_id):
    u = storage.get_user(user_id)
    return u.get("gender") if u else None

def set_age(user_id, age):
    storage.update_user(user_id, {"age": age})

def get_age(user_id):
    u = storage.get_user(user_id)
    return u.get("age") if u else None

def profile_text(u: dict):
    name = u.get("name", "غير محدد")
    age = u.get("age", "غير محدد")
    gender = u.get("gender", "غير محدد")
    respect = u.get("respect", "--")
    coins = u.get("coins", 0)
    return f"👤 <b>ملفي الشخصي</b>\n• الاسم: {name}\n• العمر: {age}\n• الجنس: {gender}\n• الاحترام: ⭐ {respect}\n• الكوينز: 🪙 {coins}"

def start_history(u: dict):
    u.setdefault("history", [])

def append_history(user_id, entry: dict):
    storage.append_history(user_id, entry)

def end_session(u1: dict, u2: dict = None):
    try:
        if u1:
            storage.update_user(u1["user_id"], {"partner": None, "chat_started_at": None})
        if u2:
            storage.update_user(u2["user_id"], {"partner": None, "chat_started_at": None})
    except Exception as e:
        print(f"[end_session ERROR] {e}")
