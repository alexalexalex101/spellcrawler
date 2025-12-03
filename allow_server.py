from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path

ALLOWED_FILE = Path("custom_words.txt")

class AllowHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        """Helper to set CORS headers."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        """Handle browser preflight requests."""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_POST(self):
        if self.path == "/allow":
            content_length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(content_length))
            word = data.get("word", "").strip().lower()

            if word:
                ALLOWED_FILE.touch(exist_ok=True)
                with open(ALLOWED_FILE, "a", encoding="utf-8") as f:
                    f.write(word + "\n")

                self.send_response(200)
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(b"OK")
            else:
                self.send_response(400)
                self._set_cors_headers()
                self.end_headers()
        else:
            self.send_error(404)

server = HTTPServer(("localhost", 5000), AllowHandler)
print("== Allow-list server running on http://localhost:5000 ... (Ctrl+C to stop) ==")

server.serve_forever()
