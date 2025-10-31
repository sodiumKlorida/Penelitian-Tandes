from flask import Blueprint, jsonify
import requests, json
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

api_bp_web = Blueprint("api_bp_web", __name__)

class WaqiController:

    @staticmethod
    def get_breakpoints():
        return {
            "pm25": [(0.0, 12.0, 0, 50),
                     (12.0, 35.4, 51, 100),
                     (35.4, 55.4, 101, 150),
                     (55.4, 150.4, 151, 200),
                     (150.4, 250.4, 201, 300),
                     (250.4, 350.4, 301, 400),
                     (350.4, 500.4, 401, 500)],
            "pm10": [(0, 54, 0, 50),
                     (54, 154, 51, 100),
                     (154, 254, 101, 150),
                     (254, 354, 151, 200),
                     (354, 424, 201, 300),
                     (424, 504, 301, 400),
                     (504, 604, 401, 500)],
            "co": [(0.0, 4.4, 0, 50),
                   (4.4, 9.4, 51, 100),
                   (9.4, 12.4, 101, 150),
                   (12.4, 15.4, 151, 200),
                   (15.4, 30.4, 201, 300),
                   (30.4, 40.4, 301, 400),
                   (40.4, 50.4, 401, 500)],
            "so2": [(0, 35, 0, 50),
                    (35, 75, 51, 100),
                    (75, 185, 101, 150),
                    (185, 304, 151, 200),
                    (304, 604, 201, 300),
                    (604, 804, 301, 400),
                    (804, 1004, 401, 500)],
            "no2": [(0, 53, 0, 50),
                    (53, 100, 51, 100),
                    (100, 360, 101, 150),
                    (360, 649, 151, 200),
                    (649, 1249, 201, 300),
                    (1249, 1649, 301, 400),
                    (1649, 2049, 401, 500)],
            "o3": [(0.0, 0.054, 0, 50),
                   (0.054, 0.070, 51, 100),
                   (0.070, 0.085, 101, 150),
                   (0.085, 0.105, 151, 200),
                   (0.105, 0.200, 201, 300)]
        }

    @staticmethod
    def hitung_aqi(pollutant, concentration):
        bp = WaqiController.get_breakpoints().get(pollutant)
        if not bp or concentration is None:
            return 0
        for c_low, c_high, i_low, i_high in bp:
            if c_low <= concentration <= c_high:
                return round(((i_high - i_low) / (c_high - c_low)) * (concentration - c_low) + i_low)
        return 0

    @staticmethod
    def fetch_WAQI_default():
        url = "https://airnet.waqi.info/airnet/sse/historic/daily/420154"
        try:
            r = requests.get(url, stream=True, timeout=15)
            if r.status_code != 200:
                return []
        except Exception:
            return []

        data_list = []
        for line in r.iter_lines(decode_unicode=True):
            if line and line.startswith("data: "):
                try:
                    json_part = line.replace("data: ", "")
                    parsed = json.loads(json_part)
                    data_list.append(parsed)
                except json.JSONDecodeError:
                    continue
        return data_list
    
    @staticmethod
    def prediksi_aqi():
        data = WaqiController.fetch_WAQI_default()
        if not data or len(data) < 2:
            return {"aqi": []}

        polutan_list = ["pm25", "pm10", "co", "so2", "no2", "o3"]
        hasil_harian = []

        # Ambil data historis valid
        for item in data[1:]:
            if not item or "day" not in item or "median" not in item:
                continue

            tanggal = item["day"]
            median_val = item["median"]
            nilai_harian = {}

            for p in polutan_list:
                if isinstance(median_val, dict):
                    kons = median_val.get(p, 0)
                else:
                    kons = float(median_val)
                nilai_harian[p] = kons

            nilai_harian["tanggal"] = tanggal
            hasil_harian.append(nilai_harian)

        if not hasil_harian:
            return {"aqi": []}

        # 🔮 Buat model regresi linear untuk setiap polutan
        X = np.arange(len(hasil_harian)).reshape(-1, 1)
        model_dict = {}
        for p in polutan_list:
            y = np.array([h[p] for h in hasil_harian])
            model_dict[p] = LinearRegression().fit(X, y)

        # Hari ini
        hari_ini = datetime.today().date()

        # Mulai prediksi dari besok
        future_X = np.arange(len(hasil_harian), len(hasil_harian) + 7).reshape(-1, 1)
        pred_dict = {p: model_dict[p].predict(future_X) for p in polutan_list}

        hasil_prediksi = []
        for i in range(7):
            tanggal_pred = (hari_ini + timedelta(days=i+1)).strftime("%Y-%m-%d")
            pred_item = {}
            for p in polutan_list:
                pred_item[p] = WaqiController.hitung_aqi(p, float(pred_dict[p][i]))
            pred_item["aqi"] = max(pred_item.values())
            pred_item["tanggal"] = tanggal_pred
            hasil_prediksi.append(pred_item)

        return hasil_prediksi


    @staticmethod
    def prediksi_aqi_web():
        data = WaqiController.fetch_WAQI_default()
        if not data or len(data) < 2:
            return {"aqi": []}

        polutan_list = ["pm25", "pm10", "co", "so2", "no2", "o3"]
        hasil_harian = []

        # Ambil data historis valid
        for item in data[1:]:
            if not item or "day" not in item or "median" not in item:
                continue

            tanggal = item["day"]
            median_val = item["median"]
            nilai_harian = {}

            for p in polutan_list:
                if isinstance(median_val, dict):
                    kons = median_val.get(p, 0)
                else:
                    kons = float(median_val)
                nilai_harian[p] = kons

            nilai_harian["tanggal"] = tanggal
            hasil_harian.append(nilai_harian)

        if not hasil_harian:
            return {"aqi": []}

        # 🔮 Buat model regresi linear untuk setiap polutan
        X = np.arange(len(hasil_harian)).reshape(-1, 1)
        model_dict = {}
        for p in polutan_list:
            y = np.array([h[p] for h in hasil_harian])
            model_dict[p] = LinearRegression().fit(X, y)

        # Hari ini
        hari_ini = datetime.today().date()

        # Mulai prediksi dari besok
        future_X = np.arange(len(hasil_harian), len(hasil_harian) + 7).reshape(-1, 1)
        pred_dict = {p: model_dict[p].predict(future_X) for p in polutan_list}

        hasil_prediksi = []
        for i in range(7):
            tanggal_pred = (hari_ini + timedelta(days=i+1)).strftime("%Y-%m-%d")
            pred_item = {}
            for p in polutan_list:
                pred_item[p] = WaqiController.hitung_aqi(p, float(pred_dict[p][i]))
            pred_item["aqi"] = max(pred_item.values())
            pred_item["tanggal"] = tanggal_pred
            hasil_prediksi.append(pred_item)

        return {"aqi": hasil_prediksi}
    
    