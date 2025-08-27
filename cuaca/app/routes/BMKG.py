from flask import Blueprint, jsonify
import requests

bmkg_bp = Blueprint("bmkg", __name__)

#  Kode wilayah BMKG (ADM4) → ini untuk menentukan lokasi yang ingin diambil datanya
ADM4 = "35.78.14.1007"

# Contoh endpoint cuaca BMKG
@bmkg_bp.route("/bmkg/cuaca")
def cuaca():
    # URL API BMKG sesuai dengan ADM4
    url = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={ADM4}"
    
    # Ambil data JSON langsung dari API BMKG
    response = requests.get(url).json()

    # Ambil data lokasi dari JSON
    lokasi = response["lokasi"]
    
    # Siapkan list kosong untuk menampung semua prakiraan
    prakiraan = []

    # Karena data "cuaca" di dalam JSON berupa nested list (list dalam list),
    # kita perlu loop dua kali (kelompok → item) agar datanya bisa di-flatten
    for kelompok in response["data"][0]["cuaca"]:
        for item in kelompok:
            prakiraan.append({
                "waktu": item["local_datetime"],  # waktu lokal prakiraan
                "cuaca": item["weather_desc"],    # deskripsi cuaca (Cerah, Berawan, dll.)
                "ikon": item["image"]             # URL ikon cuaca dari BMKG
            })

    # Kembalikan data JSON ringkas: lokasi + daftar prakiraan
    return jsonify({
        "lokasi": {
            "desa": lokasi.get("desa"),
            "kecamatan": lokasi.get("kecamatan"),
            "kotkab": lokasi.get("kotkab"),
            "provinsi": lokasi.get("provinsi")
        },
        "prakiraan": prakiraan
    })
