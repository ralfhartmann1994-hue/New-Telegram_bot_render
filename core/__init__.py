# core/__init__.py — تجميع الوحدات الأساسية (لا تستورد الوحدات التي لديها آثار جانبية عند الاستيراد)
# فقط نعرّف أسماء يمكن استيرادها من الخارج عند الحاجة.

__all__ = [
    "start_handler",
    "profile_handler",
    "chat_handler",
    "admin_handler",
    "matchmaking",
    "keyboards",
    "utils"
]

# المبدأ: لا نعمل `from . import start_handler` هنا كي لا تنفّذ الديكوراتورات على الاستيراد.
# بدلاً من ذلك، Main.py سيحمل الوحدات صراحة ثم يستدعي register(bot).
