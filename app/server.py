"""
stash.mgr — Umbrel app server
Serves the static frontend and provides /api/data for persistence.
"""
import json
import os
import logging
from datetime import datetime, timezone
from flask import Flask, jsonify, request, abort, send_from_directory

PORT      = int(os.environ.get("PORT", 6005))
DATA_FILE = os.environ.get("DATA_FILE", "/app/data/stash-data.json")
APP_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=None)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


# ── Data helpers ────────────────────────────────────────

def read_data():
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_data(payload):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    os.replace(tmp, DATA_FILE)


# ── API routes ───────────────────────────────────────────

@app.route("/api/data", methods=["GET"])
def get_data():
    data = read_data()
    if data is None:
        return jsonify({"exists": False}), 200
    return jsonify({"exists": True, "data": data}), 200

@app.route("/api/data", methods=["POST"])
def save_data():
    payload = request.get_json(force=True, silent=True)
    if payload is None:
        abort(400, description="Invalid JSON")
    payload["savedAt"] = datetime.now(timezone.utc).isoformat()
    write_data(payload)
    app.logger.info("Saved at %s", payload["savedAt"])
    return jsonify({"ok": True, "savedAt": payload["savedAt"]}), 200

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"ok": True}), 200


# ── Static frontend ──────────────────────────────────────

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_static(path):
    # Serve files from /app; fall back to index.html for SPA routing
    target = os.path.join(APP_DIR, path) if path else ""
    if path and os.path.isfile(target):
        return send_from_directory(APP_DIR, path)
    return send_from_directory(APP_DIR, "index.html")


if __name__ == "__main__":
    app.logger.info("stash.mgr starting on port %d", PORT)
    app.logger.info("Data file: %s", DATA_FILE)
    app.run(host="0.0.0.0", port=PORT)
