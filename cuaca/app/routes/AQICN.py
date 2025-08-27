from flask import Blueprint, jsonify
import requests

aqicn_bp = Blueprint("aqicn", __name__)

TOKEN = "8e6fff766a818b4aeba7e9b74e1a293da3f7c4dd"  # ganti dengan token asli

# Contoh endpoint AQICN → lokasi Tandes
@aqicn_bp.route("/aqicn/tandes")
def tandes():
    url = f"https://api.waqi.info/feed/A420154/?token={TOKEN}"
    response = requests.get(url).json()

    if response["status"] == "ok":
        data = {
            "aqi": response["data"]["aqi"],
            "pm25": response["data"]["iaqi"].get("pm25", {}).get("v", None),
            
            # "kota": response["data"]["city"]["name"],
            # "pm10": response["data"]["iaqi"].get("pm10", {}).get("v", None),
            # "co": response["data"]["iaqi"].get("co", {}).get("v", None),
            # "suhu": response["data"]["iaqi"].get("t", {}).get("v", None),
            # "kelembapan": response["data"]["iaqi"].get("h", {}).get("v", None),
            # "waktu": response["data"]["time"]["s"]
        }
        return jsonify(data)
    else:
        return jsonify({"error": "Data tidak ditemukan"})
