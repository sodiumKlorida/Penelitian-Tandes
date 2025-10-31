from flask import Blueprint, render_template, jsonify
from controllers.aqicn_controller import AqicnController 
from controllers.bmkg_controller import BmkgController
from controllers.waqi_controller import WaqiController
from controllers.tips_controller import TipsController
import traceback

api_bp_web = Blueprint("try",__name__)

# =============================================
# WAQI FUNCTION
# =============================================
@api_bp_web.route('/waqi', methods=['GET'])
def get_waqi():
    try:
        waqi_data = WaqiController.fetch_WAQI_default()
        return jsonify({
            "success": True,
            "message": "Berhasil mendapatkan data WAQI",
            "data": waqi_data
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
# =============================================
# PREDIKSI AQI FUNCTION
# =============================================
@api_bp_web.route("/waqi/prediksi", methods=["GET"])
def prediksi_aqi_endpoint():
    try:
        hasil = WaqiController.prediksi_aqi_web()
        return jsonify(hasil)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
# =============================================
# WEB ROUTE
# =============================================
@api_bp_web.route("/")
def show_web():
    try:
        polutant = AqicnController.fetch_current_air()
        current_weather = BmkgController.fetch_current_weather_web()
        forecast_weather = BmkgController.fetch_forecast_weather_web()
        hasil = WaqiController.prediksi_aqi_web()
        tips = TipsController.fetch_Tips()
        
        return render_template(
            # "index.html",
            "dummy.html", 
            aqi=polutant,
            forecast=forecast_weather,
            current=current_weather,
            prediksi_aqi=hasil["aqi"],
            tips=tips
        )
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
# =============================================
# CURRENT WEATHER FUNCTION
# =============================================
def current_weather():
    try:
        list_weather = BmkgController.fetch_BMKG_default()
        current_weather = list_weather["data"][0].get("cuaca", [])[0][0]

        current = {
            "curah_hujan": current_weather.get("tp"),
            "kelembapan": current_weather.get("hu"),
            "suhu": current_weather.get("t"),
            "waktu": current_weather.get("local_datetime", current_weather.get("datetime")),
            "weatherdesc": current_weather.get("weather_desc"),
            "kecepatan_angin": current_weather.get("ws"),
            "ikon": current_weather.get("image")
        }

        return current

    except Exception as e:
        traceback.print_exc()
        return f"success: {False} error {str(e)}", 500
    
# =============================================
# CURRENT AQI FUNCTION
# =============================================
def current_aqi():
    try:
        data = AqicnController.fetch_AQICN_default()
        iaqi = data.get("data", {}).get("iaqi", {})

        aqi = {
            "pm25": iaqi.get("pm25", {}).get("v", 0),
            "no2": iaqi.get("no2", {}).get("v", 0),
            "co": iaqi.get("co", {}).get("v", 0),
            "pm10": iaqi.get("pm10", {}).get("v", 0),
            "so2": iaqi.get("so2", {}).get("v", 0),
            "o3": iaqi.get("o3", {}).get("v", 0),
        }

        # kirim data ke template (index.html atau dashboard.html)
        return aqi

    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

    
    