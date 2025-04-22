#!/usr/bin/env python3
# server.py

import os
import json
import hmac
import hashlib
import base64
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import FileResponse
import uvicorn

# ─── Configuration ─────────────────────────────────────────────────────────────
SECRET_KEY = b"supersecretkey"          # play‑money HMAC secret
VIDEO_DIR  = "./videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

# Extended OpenAPI spec with price metadata
OPENAPI = {
    "openapi": "3.0.0",
    "info": {"title": "OpenSNAP Example API", "version": "1.0"},
    "paths": {
        "/video/generate": {
            "post": {
                "summary": "Generate a video from a prompt",
                "x-price-base": 0.001,
                "x-pricing-algo": "static",
                "x-min-price": 0.0005,
                "x-max-price": 0.01,
                "requestBody": {"content": {"application/json": {"schema": {"type": "object", "properties": {"prompt": {"type": "string"}}}}}}},
                "responses": {"200": {"description": "binary mp4"}}
            }
        }
    }
}
# ────────────────────────────────────────────────────────────────────────────────

app = FastAPI()

@app.get("/openapi.json")
def get_spec():
    """Return the extended OpenAPI spec."""
    return OPENAPI

@app.post("/video/generate")
async def generate_video(
    request: Request,
    offer: str = Header(None, alias="X-OpenSNAP-Offer"),
    voucher: str = Header(None, alias="X-OpenSNAP-Voucher")
):
    # 1. Validate headers
    if not offer or not voucher:
        raise HTTPException(400, "Missing X-OpenSNAP-Offer or X-OpenSNAP-Voucher")

    # 2. Parse and validate the offer JSON
    try:
        od = json.loads(offer)
        endpoint = od["endpoint"]
        bid = float(od["bid"])
    except:
        raise HTTPException(400, "Invalid offer format")

    meta = OPENAPI["paths"].get(endpoint, {}).get("post")
    if not meta:
        raise HTTPException(404, "Unknown endpoint")

    base = meta["x-price-base"]
    mn, mx = meta["x-min-price"], meta["x-max-price"]
    if not (mn <= bid <= mx):
        return HTTPException(402, {"detail": "Bid out of acceptable range"})

    # 3. Verify voucher (HMAC of offer)
    expected = base64.b64encode(
        hmac.new(SECRET_KEY, offer.encode(), hashlib.sha256).digest()
    ).decode()
    if not hmac.compare_digest(expected, voucher):
        raise HTTPException(402, "Invalid voucher")

    # 4. Read prompt and simulate video generation
    body = await request.json()
    prompt = body.get("prompt", "").strip()
    if not prompt:
        raise HTTPException(400, "Empty prompt")

    # (Here you’d call into your real WanT2V pipeline)
    # We’ll write a dummy file
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"video_{ts}.mp4"
    path = os.path.join(VIDEO_DIR, filename)
    with open(path, "wb") as f:
        f.write(b"FAKE_VIDEO_BYTES")

    return FileResponse(path, media_type="video/mp4", filename=filename)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
