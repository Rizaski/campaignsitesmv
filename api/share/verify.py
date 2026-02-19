# Vercel serverless: POST /api/share/verify
from http.server import BaseHTTPRequestHandler
import json
import uuid
from datetime import datetime

from api.lib.firestore import _get_firestore, set_session


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
        token = (data.get("token") or "")
        if not isinstance(token, str):
            token = str(token)
        token = token.strip()
        password = (data.get("password") or "")
        if not isinstance(password, str):
            password = str(password)
        password = password.strip()
        if not token:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            _cors_headers(self)
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": "Missing token"}).encode())
            return
        db = _get_firestore()
        if not db:
            self.send_response(503)
            self.send_header("Content-type", "application/json")
            _cors_headers(self)
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": "Share backend not configured"}).encode())
            return
        try:
            links_ref = db.collection("sharedVoterLinks")
            query = links_ref.where("token", "==", token).limit(1)
            docs = list(query.stream())
            if not docs:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                _cors_headers(self)
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": "Invalid link or password"}).encode())
                return
            doc = docs[0]
            link_data = doc.to_dict()
            stored_pw = link_data.get("password")
            if stored_pw is not None and not isinstance(stored_pw, str):
                stored_pw = str(stored_pw)
            stored_pw = (stored_pw or "").strip()
            if stored_pw != password:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                _cors_headers(self)
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": "Invalid link or password"}).encode())
                return
            created_by = link_data.get("createdBy", "")
            recipient_island = (link_data.get("recipientIsland") or "").strip() or None
            recipient_agent_id = (link_data.get("recipientAgentId") or "").strip() or None
            access_log = list(link_data.get("accessLog") or [])
            access_log.append({
                "accessedAt": datetime.utcnow(),
                "recipientName": link_data.get("recipientName", ""),
                "recipientIsland": recipient_island or "",
            })
            doc.reference.update({"accessLog": access_log})
            session_id = str(uuid.uuid4())
            if not set_session(session_id, token, created_by, recipient_island, recipient_agent_id):
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                _cors_headers(self)
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": "Could not create session"}).encode())
                return
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            _cors_headers(self)
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "sessionToken": session_id, "session": session_id}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            _cors_headers(self)
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode())
