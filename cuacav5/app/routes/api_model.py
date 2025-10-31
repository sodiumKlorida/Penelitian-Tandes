import traceback
from flask import Blueprint, jsonify, render_template 
from model_ds.function.air_quality_forecasting import AirQualityPipeline, AQICalculator, save_forecast_to_db
from DB.config import get_forecast_data
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_DIR = os.path.join(BASE_DIR, "model_ds", "Model")

api_bp = Blueprint("aqi_model", __name__)

@api_bp.route("/forecast/train", methods=["GET"])
def forecast_train():
    try:
        pipeline = AirQualityPipeline(model_dir=MODEL_DIR)
        aqi_calc = AQICalculator()

        # Jalankan pipeline lengkap
        df_final, forecasts, scalers = pipeline.run_complete_pipeline(num_forecast_days=7)

        # Konversi ke AQI
        forecasts_aqi = {}
        for pollutant, values in forecasts.items():
            forecasts_aqi[pollutant] = [
                {
                    "predicted_concentration": round(float(v), 2),
                    "nilai aqi": aqi_calc.calculate_aqi(pollutant, v)
                }
                for v in values
            ]
        
        save_forecast_to_db(forecasts_aqi)


        return jsonify({
            "success": True,
            "message": "Retraining selesai dan prediksi berhasil dikonversi ke AQI. db",
            "data": forecasts_aqi,
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
        
@api_bp.route("/api/forecast", methods=["GET"])
def api_get_forecast():
    """Endpoint untuk ambil data forecast dalam format JSON"""
    data = get_forecast_data()

    if "error" in data:
        return jsonify({"success": False, "error": data["error"]}), 500

    return jsonify({
        "success": True,
        "message": "Data forecast berhasil diambil dari database",
        "data": data
    })

@api_bp.route("/forecast/chart", methods=["GET"])
def forecast_chart_page():
    return render_template("chart.html")

