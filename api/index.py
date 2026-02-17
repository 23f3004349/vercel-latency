from http.server import BaseHTTPRequestHandler
import json
import numpy as np

class handler(BaseHTTPRequestHandler):

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # CORS preflight
    def do_OPTIONS(self):
        self._set_headers(200)

    # POST endpoint
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        data = json.loads(body or "{}")

        regions = data.get("regions", [])
        threshold = data.get("threshold_ms", 0)

        records = [
            {"region": "emea", "latency": 150, "uptime": 99.9},
            {"region": "emea", "latency": 200, "uptime": 99.5},
            {"region": "apac", "latency": 120, "uptime": 99.7},
            {"region": "apac", "latency": 180, "uptime": 99.6},
        ]

        result = {}

        for r in regions:
            vals = [x for x in records if x["region"] == r]
            if not vals:
                continue
