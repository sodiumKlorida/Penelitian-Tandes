import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime

def create_connection():
    """Koneksi ke MySQL lokal."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",         # ganti sesuai user MySQL kamu
            password="",         # ganti jika pakai password
            database="db_aqi"  # pastikan database sudah dibuat
        )
        if connection.is_connected():
            print("✅ Koneksi ke MySQL berhasil")
        return connection
    except Error as e:
        print("❌ Gagal konek ke MySQL:", e)
        return None
    
def get_forecast_data():
    """Ambil data forecast dari tabel dan ubah ke dict (bukan JSON string)."""
    conn = create_connection()
    if conn is None:
        return {"error": "Koneksi gagal"}

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT id, pollutant, predicted_concentration, nilai_aqi, created_at
            FROM forecast_aqi
            ORDER BY id ASC
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Konversi datetime ke string
        for row in rows:
            if isinstance(row["created_at"], datetime):
                row["created_at"] = row["created_at"].strftime("%Y-%m-%d %H:%M:%S")

        return rows

    except Error as e:
        print("❌ Gagal ambil data:", e)
        return {"error": str(e)}

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    
