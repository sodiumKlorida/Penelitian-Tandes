# from flask import Flask, jsonify, render_template
# import requests

# # Membuat instance aplikasi Flask
# app = Flask(__name__)

# @app.route("/tandes")
# def tandes():
#     url = "https://api.waqi.info/feed/A420154/?token=8e6fff766a818b4aeba7e9b74e1a293da3f7c4dd"
#     response = requests.get(url).json()
    
#     if response["status"] == "ok":
#         data = {
#             "kota": response["data"]["city"]["name"],
#             "aqi": response["data"]["aqi"],
#             "pm25": response["data"]["iaqi"].get("pm25", {}).get("v", None),
#             "pm10": response["data"]["iaqi"].get("pm10", {}).get("v", None),
#             "co": response["data"]["iaqi"].get("co", {}).get("v", None),
#             "suhu": response["data"]["iaqi"].get("t", {}).get("v", None),
#             "kelembapan": response["data"]["iaqi"].get("h", {}).get("v", None),
#             "waktu": response["data"]["time"]["s"]
#         }
#         return jsonify(data)
#     else:
#         return jsonify({"error": "Data tidak ditemukan"})

# # Menjalankan aplikasi Flask di mode debug
# if __name__ == "__main__":
#     app.run(debug=True)

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
            "kota": response["data"]["city"]["name"],
            "aqi": response["data"]["aqi"],
            "pm25": response["data"]["iaqi"].get("pm25", {}).get("v", None),
            "pm10": response["data"]["iaqi"].get("pm10", {}).get("v", None),
            "co": response["data"]["iaqi"].get("co", {}).get("v", None),
            "suhu": response["data"]["iaqi"].get("t", {}).get("v", None),
            "kelembapan": response["data"]["iaqi"].get("h", {}).get("v", None),
            "waktu": response["data"]["time"]["s"]
        }
        return jsonify(data)
    else:
        return jsonify({"error": "Data tidak ditemukan"})
