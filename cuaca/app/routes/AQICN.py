from flask import Blueprint, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

aqicn_bp = Blueprint("aqicn", __name__)

# TOKEN = "8e6fff766a818b4aeba7e9b74e1a293da3f7c4dd"  # ganti dengan token asli
AQICN_URL = os.getenv("AQICN_URL")
AQICN_TOKEN = os.getenv("AQICN_TOKEN")

# Contoh endpoint AQICN → lokasi Tandes
@aqicn_bp.route("/aqicn/tandes")
def tandes():
    # url = f"https://api.waqi.info/feed/A420154/?token={TOKEN}"
    url = f"{AQICN_URL}?token={AQICN_TOKEN}"
    response = requests.get(url).json()

    if response["status"] == "ok":
        data = {
            "aqi": response["data"]["aqi"],
            "pm25": response["data"]["iaqi"].get("pm25", {}).get("v", None),
        }
        return jsonify(data)
    else:
        return jsonify({"error": "Data tidak ditemukan"})
