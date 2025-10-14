# mongo_storage.py
import os
import random
from pymongo import MongoClient

MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise RuntimeError("MONGO_URL environment variable not set")

client = MongoClient(MONGO_URL)
db = client["chatbot_db"]
users_col = db["users"]

class MongoStorage:
    def __init__(self):
        self.users = users_col

    # === user fetch/create/update ===
    def get_user(self, user_id):
        return self.users.find_one({"user_id": int(user_id)})

    def create_user_if_not_exists(self, user_id, default_data=None):
        user_id = int(user_id)
        existing = self.users.find_one({"user_id": user_id})
        if existing:
            return existing
        data = default_data or {
            "user_id": user_id,
            "name": None,
            "gender": None,
            "age": None,
            "respect": 80,
            "referrer": None,
            "referral_code": self.generate_unique_ref_code(),
            "state": None,
            "partner": None,
            "history": [],
            "banned_until": None,
            "banned_full": False,
            "reported_by": [],
            "chat_started_at": None,
            "coins": int(os.getenv("COINS_NEW_USER", "100")),
            "topic": None,
            "target_gender": None
        }
        self.users.insert_one(data)
        return self.users.find_one({"user_id": user_id})

    def ensure_user(self, user_id, default_data=None):
        return self.create_user_if_not_exists(user_id, default_data)

    def update_user(self, user_id, updates: dict):
        self.users.update_one({"user_id": int(user_id)}, {"$set": updates}, upsert=True)

    # === coins ===
    def add_coins(self, user_id, amount):
        self.users.update_one({"user_id": int(user_id)}, {"$inc": {"coins": int(amount)}}, upsert=True)

    def deduct_coins(self, user_id, amount):
        user = self.get_user(user_id)
        if not user:
            return False
        if user.get("coins", 0) < amount:
            return False
        self.users.update_one({"user_id": int(user_id)}, {"$inc": {"coins": -int(amount)}})
        return True

    def get_coins(self, user_id):
        u = self.get_user(user_id)
        return int(u.get("coins", 0)) if u else 0

    # === referral ===
    def find_by_ref_code(self, ref_code):
        return self.users.find_one({"referral_code": ref_code})

    def generate_unique_ref_code(self, length=7):
        alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        for _ in range(50):
            code = ''.join(random.choices(alphabet, k=length))
            if not self.users.find_one({"referral_code": code}):
                return code
        return ''.join(random.choices(alphabet, k=length+3))

    # === history ===
    def append_history(self, user_id, entry: dict):
        self.users.update_one({"user_id": int(user_id)}, {"$push": {"history": entry}}, upsert=True)

    def clear_history(self, user_id):
        self.users.update_one({"user_id": int(user_id)}, {"$set": {"history": []}}, upsert=True)

    # === admin ops ===
    def delete_user(self, user_id):
        self.users.delete_one({"user_id": int(user_id)})

    def clear_all_users(self):
        self.users.delete_many({})

    def get_total_users(self):
        return int(self.users.count_documents({}))

    # === helper ===
    def is_new_user(self, user_id):
        u = self.get_user(user_id)
        if not u:
            return True
        return not (u.get("name") and u.get("gender") and u.get("age"))

# module-level convenience
_storage = MongoStorage()

def get_user(uid): return _storage.get_user(uid)
def create_user_if_not_exists(uid, default_data=None): return _storage.create_user_if_not_exists(uid, default_data)
def ensure_user(uid, default_data=None): return _storage.ensure_user(uid, default_data)
def update_user(uid, d): return _storage.update_user(uid, d)
def add_coins(uid,a): return _storage.add_coins(uid,a)
def deduct_coins(uid,a): return _storage.deduct_coins(uid,a)
def get_coins(uid): return _storage.get_coins(uid)
def find_by_ref_code(code): return _storage.find_by_ref_code(code)
def generate_unique_ref_code(l=7): return _storage.generate_unique_ref_code(l)
def append_history(uid,e): return _storage.append_history(uid,e)
def clear_history(uid): return _storage.clear_history(uid)
def delete_user(uid): return _storage.delete_user(uid)
def clear_all_users(): return _storage.clear_all_users()
def is_new_user(uid): return _storage.is_new_user(uid)
def get_total_users(): return _storage.get_total_users()

# expose instance
storage = _storage
