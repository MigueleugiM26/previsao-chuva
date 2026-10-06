import os
import sys
import threading
import webbrowser
from pathlib import Path

import joblib
import numpy as np
from flask import Flask, request, jsonify, send_from_directory

try:
    from flask_cors import CORS
    HAS_CORS = True
except ImportError:
    HAS_CORS = False


BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "model" / "rain_model.pkl"
INDEX_PATH = BASE_DIR / "index.html"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
if not INDEX_PATH.exists():
    raise FileNotFoundError(f"index.html not found at {INDEX_PATH}")


model = joblib.load(MODEL_PATH)

FEATURE_ORDER = [
    "temp_mean", "temp_max", "temp_min", "radiation",
    "wind_speed", "wind_gusts", "humidity_mean", "dewpoint",
    "cloud_cover_mean", "pressure_msl", "cloud_cover_max",
    "cloud_cover_min", "humidity_max", "humidity_min",
    "pressure_surface",
    "humidity_yesterday", "cloud_cover_yesterday", "radiation_yesterday",
    "pressure_yesterday", "dewpoint_yesterday",
]


app = Flask(__name__, static_folder=None)
if HAS_CORS:
    CORS(app)

@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(force=True)
        row = payload.get("data", payload)

        fallbacks = {
            "humidity_yesterday": row.get("humidity_mean"),
            "cloud_cover_yesterday": row.get("cloud_cover_mean"),
            "radiation_yesterday": row.get("radiation"),
            "pressure_yesterday": row.get("pressure_msl"),
            "dewpoint_yesterday": row.get("dewpoint"),
        }

        features = []
        for key in FEATURE_ORDER:
            value = row.get(key)
            if value is None:
                value = fallbacks.get(key)
            if value is None:
                return jsonify({"error": f"missing feature: {key}"}), 400
            features.append(float(value))

        X = np.array(features).reshape(1, -1)
        probability = round(float(model.predict_proba(X)[0][1]) * 100)
        prediction = int(model.predict(X)[0])

        return jsonify({"probability": probability, "prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def open_browser(port: int) -> None:
    try:
        webbrowser.open(f"http://localhost:{port}")
    except Exception:
        pass

def main() -> None:
    port = int(os.environ.get("PORT", 8000))
    threading.Timer(1.2, open_browser, args=(port,)).start()
    print("Previsão de Chuva — Recife")
    print(f"Servidor rodando em http://localhost:{port}")
    print("Pressione Ctrl+C para encerrar.")
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    main()
