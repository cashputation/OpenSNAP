#!/usr/bin/env python3
# client.py

import json
import hmac
import hashlib
import base64
import requests

# ─── Configuration ─────────────────────────────────────────────────────────────
SECRET_KEY = b"supersecretkey"       # must match server’s SECRET_KEY
API_BASE   = "http://localhost:8000"
# ────────────────────────────────────────────────────────────────────────────────

def fetch_spec():
    return requests.get(f"{API_BASE}/openapi.json").json()

def create_offer(endpoint: str):
    spec = fetch_spec()
    meta = spec["paths"][endpoint]["post"]
    base = meta["x-price-base"]
    mn, mx = meta["x-min-price"], meta["x-max-price"]
    bid = base  # static pricing example
    if not (mn <= bid <= mx):
        raise ValueError("Bid out of range")
    offer = {"endpoint": endpoint, "bid": bid}
    offer_json = json.dumps(offer)
    voucher = base64.b64encode(
        hmac.new(SECRET_KEY, offer_json.encode(), hashlib.sha256).digest()
    ).decode()
    return offer_json, voucher

def call_generate(prompt: str):
    endpoint = "/video/generate"
    offer, voucher = create_offer(endpoint)
    headers = {
        "X-OpenSNAP-Offer": offer,
        "X-OpenSNAP-Voucher": voucher
    }
    resp = requests.post(
        API_BASE + endpoint,
        headers=headers,
        json={"prompt": prompt},
        stream=True
    )
    if resp.status_code == 200:
        with open("out.mp4", "wb") as f:
            for chunk in resp.iter_content(1024):
                f.write(chunk)
        print("✔ Video saved as out.mp4")
    else:
        print("✘ Error", resp.status_code, resp.json())

if __name__ == "__main__":
    call_generate("Photorealistic Tyrannosaurus rex in jungle")
