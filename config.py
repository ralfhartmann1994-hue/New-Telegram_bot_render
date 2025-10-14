# config.py — إعدادات البوت (قابل للتعديل / التحميل من env)
import os

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")              # مُلزَم في env
USE_WEBHOOK = os.getenv("USE_WEBHOOK", "1") in ("1","true","True")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")         # e.g. https://your-app.onrender.com
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "webhook")
PORT = int(os.getenv("PORT", "10000"))

# Admin
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
SUPPORT_HANDLE = os.getenv("SUPPORT_HANDLE", "@MAA2857")

# Coins & referrals
COINS_NEW_USER = int(os.getenv("COINS_NEW_USER", "100"))
COINS_REFERRAL = int(os.getenv("COINS_REFERRAL", "50"))
COINS_SEARCH_GIRL = int(os.getenv("COINS_SEARCH_GIRL", "25"))

# Moderation thresholds
RESPECT_PENALTY_PER_BADWORD = int(os.getenv("RESPECT_PENALTY_PER_BADWORD", "5"))
PARTIAL_BAN_THRESHOLD = int(os.getenv("PARTIAL_BAN_THRESHOLD", "40"))
FULL_BAN_THRESHOLD = int(os.getenv("FULL_BAN_THRESHOLD", "25"))
PARTIAL_BAN_DAYS = int(os.getenv("PARTIAL_BAN_DAYS", "7"))

# Matchmaking
SEARCH_TIMEOUT = int(os.getenv("SEARCH_TIMEOUT", "1800"))   # 30 minutes
SEARCH_CHECK_INTERVAL = int(os.getenv("SEARCH_CHECK_INTERVAL", "10"))

# Mongo
MONGO_URL = os.getenv("MONGO_URL", None)

# Others
GENDERS = ["ذكر", "أنثى"]
