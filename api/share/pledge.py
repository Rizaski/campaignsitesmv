# Vercel serverless: POST /api/share/pledge
from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

from api.lib.firestore import _get_firestore, get_session


def _cors_headers(handler):
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "*")


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        _cors_headers(self)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8", errors="ignore") if content_length else "{}"
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            data = {}
        session_token = (data.get("session") or "").strip()
        voter_id = (data.get("voterId") or data.get("voterDocumentId") or "").strip()
        pledge = (data.get("pledge") or "").strip().lower()
        if pledge not in ("yes", "no", "undecided"):
            pledge = "undecided"
        if not session_token or not voter_id:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            _cors_headers(self)
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": "Missing session or voterId"}).encode())
            return
        sess = get_session(session_token)
        if not sess:
            self.send_response(401)
            self.send_header("Content-type", "application/json")
            _cors_headers(self)
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": "Session expired or invalid"}).encode())
            return
        db = _get_firestore()
        if not db:
            self.send_response(503)
            self.send_header("Content-type", "application/json")
            _cors_headers(self)
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": "Share backend not configured"}).encode())
            return
        created_by = sess.get("createdBy") or sess.get("created_by")
        try:
            pledges_ref = db.collection("pledges")
            existing = list(pledges_ref.where("email", "==", created_by).where("voterDocumentId", "==", voter_id).limit(1).stream())
            voter_ref = db.collection("voters").document(voter_id)
            voter_snap = voter_ref.get()
            voter_data = voter_snap.to_dict() if voter_snap.exists else {}
            island = voter_data.get("island") or ""
            if existing:
                existing[0].reference.update({"pledge": pledge, "recordedAt": datetime.utcnow()})
            else:
                pledges_ref.add({
                    "email": created_by,
                    "voterDocumentId": voter_id,
                    "pledge": pledge,
                    "island": island,
                    "recordedAt": datetime.utcnow(),
                })
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            _cors_headers(self)
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            _cors_headers(self)
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode())
