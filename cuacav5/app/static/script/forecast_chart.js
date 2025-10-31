document.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch("/forecast/train");
    const result = await response.json();

    if (!result.success) throw new Error(result.error || "Gagal ambil data");
    const data = result.data;

    const ctx = document.getElementById("aqiChart").getContext("2d");

    // Label waktu (7 hari)
    const labels = ["Hari 1", "Hari 2", "Hari 3", "Hari 4", "Hari 5", "Hari 6", "Hari 7"];

    // Warna tiap polutan
    const colors = {
      co: "rgba(255, 99, 132, 0.8)",
      no2: "rgba(54, 162, 235, 0.8)",
      o3: "rgba(255, 206, 86, 0.8)",
      pm10: "rgba(75, 192, 192, 0.8)",
      pm25: "rgba(153, 102, 255, 0.8)",
      so2: "rgba(255, 159, 64, 0.8)"
    };

    // Dataset untuk 6 polutan
    const datasets = Object.keys(data).map((pollutant) => ({
      label: pollutant.toUpperCase(),
      data: data[pollutant].map(v => v["nilai aqi"]),
      borderColor: colors[pollutant],
      backgroundColor: colors[pollutant],
      fill: false,
      tension: 0.4,
      borderWidth: 2,
      pointRadius: 4,
      pointHoverRadius: 6,
    }));

    // Buat chart
    new Chart(ctx, {
      type: "line",
      data: { labels, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { position: "bottom" },
          title: {
            display: true,
            text: "Perkiraan Nilai AQI 7 Hari ke Depan",
            font: { size: 16 }
          }
        },
        scales: {
          x: {
            title: { display: true, text: "Hari" },
            ticks: { color: "#fff" },
            grid: { color: "rgba(255,255,255,0.1)" }
          },
          y: {
            beginAtZero: true,
            title: { display: true, text: "Nilai AQI" },
            ticks: { color: "#fff" },
            grid: { color: "rgba(255,255,255,0.1)" }
          }
        }
      }
    });
  } catch (err) {
    console.error("Gagal memuat chart AQI:", err);
  }
});
