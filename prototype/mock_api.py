"""
Lightweight mock API server for Volley Platform wireframe flows.
Run with: python prototype/mock_api.py
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from urllib.parse import urlparse

MOCK_DATA = {
    "exercises": [
        {
            "id": 1,
            "name": "Пас с движение",
            "status": "approved",
            "category": "Подаване",
            "level": "U14",
            "proposed_by": "coach.petrov",
            "approved_by": "bfv_admin.ivanova",
        },
        {
            "id": 2,
            "name": "Блок с пренасочване",
            "status": "pending",
            "category": "Блок",
            "level": "U16",
            "proposed_by": "coach.dimitrov",
            "approved_by": None,
        },
        {
            "id": 3,
            "name": "Сервис под напрежение",
            "status": "draft",
            "category": "Сервис",
            "level": "U18",
            "proposed_by": "bfv_admin.ivanova",
            "approved_by": "platform_admin",
        },
    ],
    "trainings": [
        {
            "id": 101,
            "name": "U14 Техника + прием",
            "status": "saved",
            "duration": 75,
            "owner": "club.sofia",
            "created_by": "coach.petrov",
        },
        {
            "id": 102,
            "name": "U16 Генератор (авто)",
            "status": "approved",
            "duration": 90,
            "owner": "club.plovdiv",
            "created_by": "coach.dimitrov",
        },
    ],
    "clubs": [
        {
            "id": "club-sofia",
            "name": "Клуб София",
            "status": "active",
            "bfv_admin": "bfv_admin.ivanova",
            "coaches": 3,
            "coach_limit": 4,
        },
        {
            "id": "club-plovdiv",
            "name": "Клуб Пловдив",
            "status": "pending",
            "bfv_admin": None,
            "coaches": 1,
            "coach_limit": 4,
        },
    ],
    "roles": [
        {
            "role": "platform_admin",
            "can": [
                "създава/одобрява клубове",
                "назначава bfv_admin",
                "одобрява официални упражнения",
                "управлява методика, категории и форума",
            ],
        },
        {
            "role": "bfv_admin",
            "can": [
                "управлява треньори (до 4 на клуб)",
                "одобрява предложени упражнения",
                "публикува/редактира статии",
                "модерира форум",
            ],
        },
        {
            "role": "coach",
            "can": [
                "разглежда база упражнения",
                "генерира и запазва тренировки",
                "предлага нови упражнения",
                "пише във форума",
            ],
        },
    ],
    "pending": {
        "exercises": [
            {
                "id": 2,
                "name": "Блок с пренасочване",
                "proposed_by": "coach.dimitrov",
                "needs": "proof video",
            }
        ],
        "articles": [
            {
                "id": 201,
                "title": "Примерен фитнес протокол",
                "proposed_by": "coach.petrov",
                "needs": "review by bfv_admin",
            }
        ],
        "forum_reports": [
            {
                "topic": "Тактика срещу висок блок",
                "reported_by": "coach.nikolov",
                "reason": "off-topic",
            }
        ],
    },
}

API_INTRO = {
    "message": "Volley Platform mock API",
    "endpoints": [
        "/api/exercises",
        "/api/trainings",
        "/api/clubs",
        "/api/roles",
        "/api/pending",
        "POST /api/pending/exercises",
        "POST /api/pending/exercises/<id>/approve",
        "POST /api/pending/exercises/<id>/reject",
        "/health",
    ],
}


def _next_exercise_id():
    """Return the next available exercise id across exercises and pending."""

    existing_ids = [e.get("id", 0) for e in MOCK_DATA.get("exercises", [])]
    existing_ids += [e.get("id", 0) for e in MOCK_DATA.get("pending", {}).get("exercises", [])]
    return (max(existing_ids) if existing_ids else 0) + 1


class MockHandler(BaseHTTPRequestHandler):
    def _add_cors_headers(self):
        origin = self.headers.get("Origin", "*")
        self.send_header("Access-Control-Allow-Origin", origin if origin else "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Origin, Accept")
        self.send_header("Access-Control-Max-Age", "86400")

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._add_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_bytes(self, body: bytes, status=200, content_type="text/plain; charset=utf-8"):
        self.send_response(status)
        self._add_cors_headers()
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
        except (TypeError, ValueError):
            length = 0
        if length <= 0:
            return {}
        try:
            data = self.rfile.read(length)
            return json.loads(data.decode("utf-8")) if data else {}
        except Exception:
            return {}

    def do_OPTIONS(self):
        # Handle preflight for cross-origin requests when hosting UI separately
        self.send_response(204)
        self._add_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        accept_header = self.headers.get("Accept", "") or ""
        wants_html = "text/html" in accept_header

        if parsed.path in {"/", "/index.html"} and wants_html:
            index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "index.html"))
            if os.path.isfile(index_path):
                with open(index_path, "rb") as f:
                    self._send_bytes(f.read(), content_type="text/html; charset=utf-8")
            else:
                self._send_json(API_INTRO)
        elif parsed.path in {"/", "/api"}:
            self._send_json(API_INTRO)
        elif parsed.path == "/health":
            self._send_json({"status": "ok"})
        elif parsed.path == "/api/exercises":
            self._send_json(MOCK_DATA["exercises"])
        elif parsed.path == "/api/trainings":
            self._send_json(MOCK_DATA["trainings"])
        elif parsed.path == "/api/clubs":
            self._send_json(MOCK_DATA["clubs"])
        elif parsed.path == "/api/roles":
            self._send_json(MOCK_DATA["roles"])
        elif parsed.path == "/api/pending":
            self._send_json(MOCK_DATA["pending"])
        else:
            self._send_json({"error": "not found"}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/pending/exercises":
            payload = self._read_json_body()
            name = payload.get("name") or "Ново упражнение"
            category = payload.get("category") or "Общо"
            proposed_by = payload.get("proposed_by") or "coach.demo"
            new_item = {
                "id": _next_exercise_id(),
                "name": name,
                "category": category,
                "proposed_by": proposed_by,
                "needs": payload.get("needs") or "review",
            }
            MOCK_DATA.setdefault("pending", {}).setdefault("exercises", []).append(new_item)
            self._send_json({"status": "queued", "item": new_item}, status=201)
            return

        if parsed.path.startswith("/api/pending/exercises/"):
            segments = [s for s in parsed.path.rstrip("/").split("/") if s]
            action = None
            exercise_id = None

            # Support both /api/pending/exercises/<id>/<action> and /api/pending/exercises/<action>/<id>
            if len(segments) >= 5 and segments[-1] in {"approve", "reject"}:
                action = segments[-1]
                try:
                    exercise_id = int(segments[-2])
                except (TypeError, ValueError):
                    exercise_id = None
            if action is None and len(segments) >= 5 and segments[-2] in {"approve", "reject"}:
                action = segments[-2]
                try:
                    exercise_id = int(segments[-1])
                except (TypeError, ValueError):
                    exercise_id = None

            if exercise_id is None or action not in {"approve", "reject"}:
                self._send_json({"error": "invalid path"}, status=400)
                return

            pending_list = MOCK_DATA.get("pending", {}).get("exercises", [])
            match = next((x for x in pending_list if x.get("id") == exercise_id), None)
            if not match:
                self._send_json({"error": "not found"}, status=404)
                return

            if action == "approve":
                pending_list.remove(match)
                payload = self._read_json_body()
                new_ex = {
                    "id": match.get("id"),
                    "name": match.get("name"),
                    "category": match.get("category", "Общо"),
                    "status": "approved",
                    "level": (payload or {}).get("level", ""),
                    "proposed_by": match.get("proposed_by"),
                    "approved_by": (payload or {}).get("approved_by", "bfv_admin.demo"),
                }
                MOCK_DATA.setdefault("exercises", []).append(new_ex)
                self._send_json({"status": "approved", "item": new_ex})
                return

            if action == "reject":
                pending_list.remove(match)
                self._send_json({"status": "rejected", "removed": match})
                return

        self._send_json({"error": "not found"}, status=404)

    def log_message(self, format, *args):
        # Silence default stdout logging for cleaner console output
        return


def run_server(host="0.0.0.0", port=None):
    # Render и други платформи подават порт чрез променлива PORT
    effective_port = int(port or os.environ.get("PORT", 8001))
    server = HTTPServer((host, effective_port), MockHandler)
    print(f"Mock API server running on http://{host}:{effective_port}")
    print("Endpoints: /api/exercises, /api/trainings, /api/clubs, /api/roles, /api/pending")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
