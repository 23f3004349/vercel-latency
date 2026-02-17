from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.post("")
async def latency(request: Request):
    data = await request.json()

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

        latencies = [v["latency"] for v in vals]
        uptimes = [v["uptime"] for v in vals]

        result[r] = {
            "avg_latency": float(np.mean(latencies)),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": float(np.mean(uptimes)),
            "breaches": int(sum(1 for l in latencies if l > threshold)),
        }

    return result
