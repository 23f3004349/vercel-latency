from http.server import BaseHTTPRequestHandler
import json
import numpy as np

with open("q-vercel-latency.json") as f:
    DATA = json.load(f)


class handler(BaseHTTPRequestHandler):

    # ---------- CORS headers ----------
    def _set_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    # ---------- OPTIONS (preflight) ----------
    def do_OPTIONS(self):
        self.send_response(204)          # IMPORTANT: 204 No Content
        self._set_cors()
        self.end_headers()               # NO BODY

    # ---------- POST handler ----------
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        req = json.loads(body)

        regions = req.get("regions", [])
        threshold = req.get("threshold_ms", 0)

        result = {}

        for region in regions:
            records = [r for r in DATA if r["region"] == region]
            if not records:
                continue

            latencies = [r["latency_ms"] for r in records]
            uptimes = [r["uptime_pct"] for r in records]

            result[region] = {
                "avg_latency": float(np.mean(latencies)),
                "p95_latency": float(np.percentile(latencies, 95)),
                "avg_uptime": float(np.mean(uptimes)),
                "breaches": sum(1 for l in latencies if l > threshold),
            }

        # ---------- send response ----------
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self._set_cors()
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
