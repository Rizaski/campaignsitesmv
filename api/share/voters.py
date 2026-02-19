# Vercel serverless: GET /api/share/voters?session=...
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

from api.lib.firestore import _get_firestore, get_session


def _cors_headers(handler):
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "*")


def _serialize(obj):
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    if hasattr(obj, "seconds"):
        return {"_seconds": obj.seconds, "_nanoseconds": getattr(obj, "nanoseconds", 0)}
    raise TypeError(type(obj).__name__)


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        _cors_headers(self)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        session_token = (qs.get("session") or [None])[0]
        if not session_token:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            _cors_headers(self)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing session"}).encode())
            return
        sess = get_session(session_token)
        if not sess:
            self.send_response(401)
            self.send_header("Content-type", "application/json")
            _cors_headers(self)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Session expired or invalid"}).encode())
            return
        db = _get_firestore()
        if not db:
            self.send_response(503)
            self.send_header("Content-type", "application/json")
            _cors_headers(self)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Share backend not configured"}).encode())
            return
        try:
            created_by = sess.get("createdBy") or sess.get("created_by")
            voters_ref = db.collection("voters")
            recipient_agent_id = sess.get("recipientAgentId") or None
            recipient_island = sess.get("recipientIsland") or None
            if recipient_agent_id:
                q = voters_ref.where("email", "==", created_by).where("assignedAgentId", "==", recipient_agent_id).limit(5000)
            elif recipient_island:
                q = voters_ref.where("email", "==", created_by).where("island", "==", recipient_island).limit(5000)
            else:
                q = voters_ref.where("email", "==", created_by).limit(5000)
            docs = list(q.stream())
            voters = []
            voter_ids = []
            for d in docs:
                data = d.to_dict()
                data["id"] = d.id
                voter_ids.append(d.id)
                voters.append(data)
            pledge_by_voter = {}
            if voter_ids:
                pledges_ref = db.collection("pledges")
                for i in range(0, len(voter_ids), 30):
                    batch = voter_ids[i : i + 30]
                    pq = pledges_ref.where("email", "==", created_by).where("voterDocumentId", "in", batch)
                    for pd in pq.stream():
                        pdata = pd.to_dict()
                        vid = pdata.get("voterDocumentId")
                        if vid:
                            pledge_by_voter[vid] = (pdata.get("pledge") or "undecided").lower()
                            if pledge_by_voter[vid] == "negative":
                                pledge_by_voter[vid] = "no"
            for v in voters:
                v["pledge"] = pledge_by_voter.get(v["id"], "undecided")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            _cors_headers(self)
            self.end_headers()
            self.wfile.write(json.dumps({"voters": voters}, default=_serialize).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            _cors_headers(self)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
