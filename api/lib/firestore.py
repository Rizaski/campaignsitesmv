"""
Firebase Admin + Firestore for Vercel serverless.
Uses env FIREBASE_SERVICE_ACCOUNT_JSON (full JSON string) or GOOGLE_APPLICATION_CREDENTIALS.
Sessions are stored in Firestore (shareSessions) since Vercel is stateless.
"""
import os
import json
import time

_db = None
_app = None
_SESSION_TTL = 24 * 3600  # 24 hours


def _get_firestore():
    global _db, _app
    if _db is not None:
        return _db
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        if not firebase_admin._apps:
            json_str = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON", "").strip()
            if json_str:
                cred_dict = json.loads(json_str)
                cred = credentials.Certificate(cred_dict)
            else:
                cred = credentials.ApplicationDefault()
            _app = firebase_admin.initialize_app(cred)
        _db = firestore.client()
        return _db
    except Exception:
        return None


def get_session(session_id):
    """Return session dict (token, createdBy, expiry) or None if invalid/expired."""
    db = _get_firestore()
    if not db:
        return None
    try:
        ref = db.collection("shareSessions").document(session_id)
        doc = ref.get()
        if not doc or not doc.exists:
            return None
        data = doc.to_dict()
        expiry = data.get("expiry") or 0
        if time.time() > expiry:
            ref.delete()
            return None
        return data
    except Exception:
        return None


def set_session(session_id, token, created_by, recipient_island=None, recipient_agent_id=None):
    """Store session in Firestore (recipientIsland/recipientAgentId used to filter voters like agent assigned list)."""
    db = _get_firestore()
    if not db:
        return False
    try:
        data = {
            "token": token,
            "createdBy": created_by,
            "expiry": time.time() + _SESSION_TTL,
        }
        if recipient_island:
            data["recipientIsland"] = recipient_island
        if recipient_agent_id:
            data["recipientAgentId"] = recipient_agent_id
        db.collection("shareSessions").document(session_id).set(data)
        return True
    except Exception:
        return False
