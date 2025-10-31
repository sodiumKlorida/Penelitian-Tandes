document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("aqiChart");
  if (!canvas) {
    console.error("❌ Elemen #aqiChart tidak ditemukan di halaman.");
    return;
  }

  const ctx = canvas.getContext("2d");
  if (!ctx) {
    console.error("❌ Tidak bisa mendapatkan context dari canvas.");
    return;
  }

  async function getAQIPrediction() {
    try {
      const res = await fetch("/waqi/prediksi");
      const json = await res.json();

      if (!json.aqi || json.aqi.length === 0) {
        alert("Tidak ada data prediksi tersedia.");
        return;
      }

      // Ambil label tanggal & daftar polutan
      const labels = json.aqi.map(item => item.tanggal);
      const pollutants = ["pm25", "pm10", "co", "so2", "no2", "o3"];
      const colors = {
        pm25: "#e74c3c",
        pm10: "#f39c12",
        co: "#3498db",
        so2: "#9b59b6",
        no2: "#2ecc71",
        o3: "#1abc9c"
      };

      // 🌙 Deteksi mode gelap Tailwind
      const isDark = document.documentElement.classList.contains("dark");
      const textColor = isDark ? "#e5e7eb" : "#1f2937"; // gray-200 vs gray-800
      const gridColor = isDark ? "rgba(255,255,255,0.1)" : "rgba(0,0,0,0.1)";
      const tooltipBg = isDark ? "rgba(255,255,255,0.9)" : "rgba(0,0,0,0.85)";
      const tooltipText = isDark ? "#111827" : "#f9fafb";

      // Buat dataset 6 polutan
      const datasets = pollutants.map(p => ({
        label: p.toUpperCase(),
        data: json.aqi.map(item => item[p]),
        borderColor: colors[p],
        backgroundColor: colors[p],
        tension: 0.35,
        fill: false,
        borderWidth: 2,
        pointRadius: 3,
        pointHoverRadius: 5
      }));

      // 🔍 Pastikan canvas ada di DOM
      const canvas = document.getElementById("aqiChart");
      if (!canvas) {
        console.warn("Canvas #aqiChart belum ditemukan di halaman.");
        return;
      }

      const ctx = canvas.getContext("2d");

      // Hapus chart lama jika ada
      if (window.aqiChartInstance) {
        window.aqiChartInstance.destroy();
      }

      // Buat chart baru
      window.aqiChartInstance = new Chart(ctx, {
        type: "line",
        data: { labels, datasets },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "bottom",
              labels: {
                color: textColor,
                font: { size: 13 }
              }
            },
            title: {
              display: true,
              text: "Prediksi Nilai AQI per Polutan Selama 7 Hari",
              color: textColor,
              font: { size: 16, weight: "bold" }
            },
            tooltip: {
              backgroundColor: tooltipBg,
              titleColor: tooltipText,
              bodyColor: tooltipText
            }
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Tanggal",
                color: textColor,
                font: { size: 14, weight: "bold" }
              },
              ticks: {
                color: textColor,
                font: { size: 10 },
                maxRotation: 0,
                minRotation: 0,
                autoSkip: true,
                padding: 10
              },
              grid: { color: gridColor }
            },
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: "Nilai AQI",
                color: textColor,
                font: { size: 14, weight: "bold" }
              },
              ticks: {
                color: textColor,
                font: { size: 12 }
              },
              grid: { color: gridColor }
            }
          },
          layout: { padding: 10 },
          animation: {
            duration: 1200,
            easing: "easeOutQuart"
          }
        }
      });
    } catch (err) {
      console.error("Gagal mengambil data:", err);
    }
  }

  // 🔄 Render awal
  getAQIPrediction();

  // 🔁 Render ulang saat mode gelap berubah
  const observer = new MutationObserver(() => getAQIPrediction());
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
});
