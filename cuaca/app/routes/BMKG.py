# from flask import Blueprint, jsonify, render_template
# import requests

# bmkg_bp = Blueprint("bmkg", __name__)

# # Kode wilayah BMKG (ADM4)
# ADM4 = "35.78.14.1007"

# @bmkg_bp.route("/bmkg/cuaca")
# def cuaca():
#     url = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={ADM4}"
#     response = requests.get(url).json()

#     lokasi = response.get("lokasi", {})
#     prakiraan = []

#     # Flatten data cuaca
#     if "data" in response:
#         for kelompok in response["data"][0]["cuaca"]:
#             for item in kelompok:
#                 prakiraan.append({
#                     "waktu": item.get("local_datetime"),
#                     "suhu": item.get("t"),
#                     "kelembapan": item.get("hu"),
#                     "cuaca": item.get("weather_desc"),
#                     "ikon": item.get("image"),
#                 })

#     return jsonify({
#         "lokasi": {
#             "desa": lokasi.get("desa"),
#             "kecamatan": lokasi.get("kecamatan"),
#             "kotkab": lokasi.get("kotkab"),
#             "provinsi": lokasi.get("provinsi"),
#         },
#         "prakiraan": prakiraan
#     })


# @bmkg_bp.route("/cuaca")
# def cuaca_prakiraan():
#     url = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={ADM4}"
#     response = requests.get(url).json()

#     prakiraan = []
#     if "data" in response:
#         cuaca = response["data"][0]["cuaca"]
#         for hari in cuaca:  # setiap hari
#             for item in hari:  # setiap jam
#                 prakiraan.append({
#                     "local_datetime": item.get("local_datetime"),
#                     "suhu": item.get("t"),
#                     "kelembapan": item.get("hu"),
#                     "cuaca": item.get("weather_desc"),
#                     "ikon": item.get("image"),
#                     "angin": f"{item.get('wd')} {item.get('ws')} km/jam",
#                     "awan": f"{item.get('tcc')}%",
#                     "jarak_pandang": item.get("vs_text"),
#                 })

#     lokasi = response.get("lokasi", {})
    
#     return render_template("content/prakiraan_cuaca.html", prakiraan=prakiraan, lokasi=lokasi)

import os
from flask import Flask, jsonify, Blueprint
import requests
from dotenv import load_dotenv

load_dotenv()

bmkg_bp = Blueprint ("bmkg",__name__)
# ADM4 = "35.78.14.1007"
BMKG_URL = os.getenv("BMKG_URL")
ADM4 = os.getenv("ADM4")

@bmkg_bp.route("/prakiraan")
def prakiraan():
    url = f"{BMKG_URL}?adm4={ADM4}"
    # url = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={ADM4}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Referer": "https://www.bmkg.go.id/"
    }
    res = requests.get(url, headers=headers, timeout=10)

    if res.status_code != 200:
        return jsonify({
            "error": f"Gagal ambil data BMKG ({res.status_code})",
            "preview": res.text[:200]
        }), res.status_code

    try:
        data = res.json()
    except Exception:
        return jsonify({
            "error": "Respon BMKG tidak dalam format JSON",
            "preview": res.text[:200]
        }), 500

    lokasi = data.get("lokasi", {})
    prakiraan_list = []
    for hari in data.get("data", [{}])[0].get("cuaca", []):
        for item in hari:
            prakiraan_list.append({
                "waktu": item.get("local_datetime"),
                "suhu": item.get("t"),
                "kelembapan": item.get("hu"),
                "cuaca": item.get("weather_desc"),
                "arah dan kecepatan angin": f"{item.get('wd')} {item.get('ws')} km/jam",
                "awan": f"{item.get('tcc')}%",
                "jarak_pandang": item.get("vs_text"),
                "ikon": item.get("image"),
            })

    return jsonify({
        "lokasi": lokasi,
        "prakiraan": prakiraan_list,
        "sumber": "BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)"
    })