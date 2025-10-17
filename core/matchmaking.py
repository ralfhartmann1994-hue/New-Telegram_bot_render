import threading
import time
from typing import List, Optional
from mongo_storage import ensure_user, update_user, storage

_wait_lock = threading.RLock()
_waiting: List[dict] = []  # entries: {"topic", "uid", "target", "ts"}

def add_to_wait(topic: Optional[str], uid: int, target: str = "any"):
    with _wait_lock:
        # remove existing entry for uid
        _waiting[:] = [e for e in _waiting if e["uid"] != uid]
        _waiting.append({"topic": topic, "uid": int(uid), "target": target, "ts": int(time.time())})

def remove_from_wait(uid: int):
    with _wait_lock:
        before = len(_waiting)
        _waiting[:] = [e for e in _waiting if e["uid"] != uid]
        return len(_waiting) < before

def try_match(uid: int, topic: Optional[str]):
    with _wait_lock:
        me = next((e for e in _waiting if e["uid"] == uid), None)
        if not me:
            return None
        # try to find a partner with same topic and compatible target
        for e in _waiting:
            if e is me:
                continue
            # topic match (if either is None or 'any' accept)
            if me["topic"] and e["topic"] and me["topic"] != e["topic"]:
                continue
            # simple gender/target acceptance — for now ignore gender compatibility unless needed
            # remove both from waitlist and return partner uid
            _waiting[:] = [x for x in _waiting if x not in (me, e)]
            return e["uid"]
    return None

# watcher to cleanup stale waiting entries (30 minutes)
_watcher_thread = None
_stop_event = None

def _watcher(bot=None, interval=60, timeout_minutes=30):
    print("[matchmaking] watcher started")
    timeout_seconds = timeout_minutes * 60
    while True:
        now = int(time.time())
        to_notify = []
        with _wait_lock:
            for e in list(_waiting):
                if now - e["ts"] > timeout_seconds:
                    _waiting.remove(e)
                    to_notify.append(e)
        for e in to_notify:
            try:
                update_user(e["uid"], {"state": None})
                if bot:
                    bot.send_message(e["uid"], "⏰ لم يتم العثور على شريك خلال 30 دقيقة. جرّب مرة أخرى لاحقًا.",)
            except Exception as ex:
                print(f"[matchmaking watcher notify ERROR] {ex}")
        time.sleep(interval)

def start_timeout_watcher(bot=None):
    global _watcher_thread
    if _watcher_thread and _watcher_thread.is_alive():
        return
    _watcher_thread = threading.Thread(target=_watcher, args=(bot,), daemon=True)
    _watcher_thread.start()
