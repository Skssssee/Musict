# utils/peer_fix.py

import logging
from pyrogram.errors import PeerIdInvalid

log = logging.getLogger("PeerFix")

async def safe_resolve(client, peer_id):
    try:
        return await client.get_chat(peer_id)
    except PeerIdInvalid:
        log.warning(f"Ignored invalid peer: {peer_id}")
        return None
    except Exception as e:
        log.warning(f"Resolve error {peer_id}: {e}")
        return None
