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
        "/health",
    ],
}


class MockHandler(BaseHTTPRequestHandler):
    def _add_cors_headers(self):
        origin = self.headers.get("Origin", "*")
        self.send_header("Access-Control-Allow-Origin", origin if origin else "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
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
