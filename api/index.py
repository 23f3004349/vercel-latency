from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Load telemetry CSV
df = pd.read_csv("telemetry.csv")


@app.post("/")
async def metrics(request: Request):
    body = await request.json()
    regions = body["regions"]
    threshold = body["threshold_ms"]

    filtered = df[df["region"].isin(regions)]

    result = {}

    for region in regions:
        region_df = filtered[filtered["region"] == region]

        result[region] = {
            "avg_latency": float(region_df["latency_ms"].mean()),
            "p95_latency": float(np.percentile(region_df["latency_ms"], 95)),
            "avg_uptime": float(region_df["uptime"].mean()),
            "breaches": int((region_df["latency_ms"] > threshold).sum())
        }

    return result
