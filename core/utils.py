# ============================================================
# utils.py — أدوات مساعدة عامة للبوت
# ============================================================

from mongo_storage import MongoStorage

# تهيئة الاتصال بقاعدة البيانات
db = MongoStorage()


def ensure_user_extended(uid, telegram_user=None):
    """
    يتأكد من أن المستخدم موجود في قاعدة البيانات، 
    ويحدث معلومات الاسم واسم المستخدم من Telegram إن وجدت.
    """
    user = db.ensure_user(uid)
    updates = {}

    if telegram_user:
        updates["username"] = telegram_user.username
        updates["first_name"] = telegram_user.first_name

    if updates:
        db.update_user(uid, updates)

    return user


def get_user(user_id):
    """
    جلب بيانات المستخدم من قاعدة البيانات.
    إذا لم يكن موجودًا، يتم إنشاؤه تلقائيًا.
    """
    user = db.get_user(user_id)
    if not user:
        db.ensure_user(user_id)
        user = db.get_user(user_id)
    return user


def is_user_fully_registered(user: dict) -> bool:
    """
    التحقق مما إذا كان المستخدم قد أكمل جميع خطوات التسجيل.
    """
    if not user:
        return False
    return all(user.get(k) for k in ["name", "gender", "age"])


def safe_get(value, default=None):
    """
    دالة آمنة لإرجاع قيمة أو قيمة افتراضية في حال كانت None.
    """
    return value if value is not None else default
