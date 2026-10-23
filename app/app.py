#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
import os
import signal
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DATABASE = Path(
    os.environ.get("DATABASE_PATH", str(BASE_DIR / "app.db"))
)
FRONTEND = BASE_DIR / "index.html"
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8004"))

def initialize_database():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS counter "
            "(id INTEGER PRIMARY KEY, visits INTEGER NOT NULL)"
        )
        connection.execute(
            "INSERT OR IGNORE INTO counter (id, visits) VALUES (1, 0)"
        )

def record_visit():
    with sqlite3.connect(DATABASE) as connection:
        connection.execute(
            "UPDATE counter SET visits = visits + 1 WHERE id = 1"
        )
        return connection.execute(
            "SELECT visits FROM counter WHERE id = 1"
        ).fetchone()[0]

class ApplicationHandler(BaseHTTPRequestHandler):
    def send_content(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self.send_content(
                200,
                "text/html; charset=utf-8",
                FRONTEND.read_bytes(),
            )
        elif self.path == "/health":
            body = json.dumps({"status": "ok"}).encode()
            self.send_content(200, "application/json", body)
        elif self.path == "/api/visits":
            body = json.dumps({"visits": record_visit()}).encode()
            self.send_content(200, "application/json", body)
        else:
            self.send_content(404, "text/plain", b"Not found\n")

initialize_database()
server = HTTPServer((HOST, PORT), ApplicationHandler)

def handle_shutdown(_signum, _frame):
    print("Shutdown signal received", flush=True)
    raise KeyboardInterrupt

signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

print(f"Application running at http://{HOST}:{PORT}", flush=True)

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    server.server_close()
    print("Application stopped gracefully", flush=True)
