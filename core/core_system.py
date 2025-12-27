# ======================================================
# core/core_system.py
# ALL CORE LOGIC COMBINED & EXPLAINED
# ======================================================

from pymongo import MongoClient
from typing import List, Optional

from config import OWNER_ID, MONGO_DB_URI, LOGGER_ID

# ======================================================
# DATABASE CONNECTION
# ======================================================
# Ek hi MongoDB client poore bot ke core ke liye

mongo = MongoClient(MONGO_DB_URI)
db = mongo.musicbot

# Collections
sudo_col = db.sudo_users        # sudo users list
chats_col = db.chats            # chats where bot is used
logger_col = db.logger_state    # logger on/off + chat id


# ======================================================
# SUDO SYSTEM
# ======================================================
# OWNER hamesha sudo hota hai
# Baaki sudo users DB me store hote hain

def is_owner(user_id: int) -> bool:
    """
    Check if user is bot owner
    """
    return user_id == OWNER_ID


def is_sudo(user_id: int) -> bool:
    """
    Check if user is sudo or owner
    """
    if is_owner(user_id):
        return True
    return sudo_col.find_one({"_id": user_id}) is not None


def add_sudo(user_id: int):
    """
    Add sudo user (DB based, no restart needed)
    """
    sudo_col.update_one(
        {"_id": user_id},
        {"$set": {"_id": user_id}},
        upsert=True
    )


def remove_sudo(user_id: int):
    """
    Remove sudo user
    """
    sudo_col.delete_one({"_id": user_id})


def get_sudo_users() -> List[int]:
    """
    Return all sudo user IDs
    """
    return [u["_id"] for u in sudo_col.find()]


# ======================================================
# CHAT DATABASE (FOR BROADCAST / STATS)
# ======================================================
# Bot jahan-jahan add hota hai
# ya command use hoti hai
# un chats ko yahan store kiya jata hai

def add_chat(chat_id: int):
    """
    Save chat ID where bot is used
    """
    chats_col.update_one(
        {"_id": chat_id},
        {"$set": {"_id": chat_id}},
        upsert=True
    )


def get_all_chats() -> List[int]:
    """
    Get all saved chat IDs
    """
    return [c["_id"] for c in chats_col.find()]


# ======================================================
# PERMISSIONS HELPERS
# ======================================================
# Plugins in helpers ko use karte hain

def owner_only(user_id: int) -> bool:
    """
    True only for owner
    """
    return is_owner(user_id)


def sudo_or_owner(user_id: int) -> bool:
    """
    True for sudo or owner
    """
    return is_sudo(user_id)


# ======================================================
# LOGGER SYSTEM (LOGGER GC)
# ======================================================
# Logger ON/OFF DB me store hota hai
# Agar OFF → koi log nahi
# Agar ON → logs LOGGER_ID ya saved chat me jate hain

def enable_logger(chat_id: int):
    """
    Enable logger and save chat_id
    """
    logger_col.update_one(
        {"_id": 1},
        {"$set": {"enabled": True, "chat_id": chat_id}},
        upsert=True
    )


def disable_logger():
    """
    Disable logger
    """
    logger_col.update_one(
        {"_id": 1},
        {"$set": {"enabled": False}},
        upsert=True
    )


def is_logger_enabled() -> bool:
    """
    Check if logger is enabled
    """
    data = logger_col.find_one({"_id": 1})
    return bool(data and data.get("enabled"))


def get_logger_chat() -> Optional[int]:
    """
    Returns chat ID where logs should be sent

    Priority:
    1️⃣ Logger enabled chat from DB
    2️⃣ LOGGER_ID from ENV
    """
    data = logger_col.find_one({"_id": 1})

    if data and data.get("enabled"):
        return data.get("chat_id")

    return LOGGER_ID


# ======================================================
# CORE SYSTEM SUMMARY (MENTAL MODEL)
# ======================================================
"""
core_system.py handles:

1️⃣ SUDO SYSTEM
   - OWNER_ID → always sudo
   - DB-based sudo users
   - /sudo add / remove (no restart)

2️⃣ CHAT DB
   - All groups & private chats
   - Used for broadcast / stats

3️⃣ PERMISSIONS
   - owner_only()
   - sudo_or_owner()

4️⃣ LOGGER SYSTEM
   - /logger on / off
   - Logs go to one GC only
   - ENV LOGGER_ID as fallback
"""
