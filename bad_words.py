# bad_words.py
# قائمة كلمات بذيئة (عربية/إنجليزية). عدّلها كما تشاء.
# ملاحظة: الكشف بسيط بالبحث الجزئي داخل النص بعد تحويله لحروف صغيرة.
BAD_WORDS = {
    # عربي (أمثلة شائعة — عدّل حسب حاجتك)
    "قحبة", "قواد", "عرص", "شرموط", "منيك", "كس", "طيز", "زب",
    "يا حيوان", "يا كلب", "يا حمار", "قرف", "وسخ", "نجس",

    # إنجليزي
    "fuck", "shit", "bitch", "asshole", "bastard", "dick", "pussy", "cunt",
    "slut", "whore", "motherfucker", "dumbass", "prick", "jerk", "moron",
    "retard", "faggot", "nigger"
}

def count_bad_words(text: str) -> int:
    if not text:
        return 0
    t = text.lower()
    total = 0
    for w in BAD_WORDS:
        if w in t:
            total += t.count(w)
    return total
