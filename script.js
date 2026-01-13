// ----------------------------
// Scrolling effects (existing code)
// ----------------------------
const description = document.querySelector('.hero-description');
const nextSection = document.querySelector('.next-section');

window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;
  if (scrollY > 50) {
    description.classList.add('scrolled');
  } else {
    description.classList.remove('scrolled');
  }

  const sectionTop = nextSection.offsetTop;
  const sectionHeight = nextSection.offsetHeight;

  if (scrollY > sectionTop + sectionHeight / 2) {
    nextSection.classList.add('scrolled');
  } else {
    nextSection.classList.remove('scrolled');
  }
});

// ----------------------------
// Open file picker
// ----------------------------
function openFilePicker() {
  document.getElementById("videoInput").click();
}

// ----------------------------
// Upload video + display results after YOLO finishes
// ----------------------------
document.getElementById("videoInput").addEventListener("change", function () {
  const file = this.files[0];
  if (!file) return;

  if (file.type !== "video/mp4") {
    alert("Upload an MP4 video only.");
    return;
  }

  const trafficResults = document.getElementById("trafficResults");

  // Show loading message immediately
  trafficResults.innerHTML = `
    <p style="color:#00ff88;">Processing video... check VS Code terminal logs for YOLO detection progress.</p>
  `;

  const formData = new FormData();
  formData.append("video", file);

  // Send video to Flask backend
  fetch("http://127.0.0.1:5000/analyze", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    console.log("✅ Received optimization results:", data);

    // Build results HTML
    let html = "<h2 style='color:#00ff88;'>🚦 Traffic Analysis Results</h2>";
    
    html += "<h3>🚗 Vehicle Counts per Lane:</h3><ul>";
    for (const lane in data.vehicle_counts) {
      html += `<li>${lane}: ${data.vehicle_counts[lane]} vehicles</li>`;
    }
    html += "</ul>";

    html += "<h3>⏱️ Suggested Signal Timings:</h3>";
    html += `<p>Green Time: ${data.signal_timings.green_time_sec} seconds</p>`;
    html += `<p>Red Time: ${data.signal_timings.red_time_sec} seconds</p>`;

    // Display per-lane green times if present
    if (data.signal_timings.lane_timings) {
      html += "<h3>🚦 Per-Lane Green Times:</h3><ul>";
      for (const lane in data.signal_timings.lane_timings) {
        html += `<li>${lane}: ${data.signal_timings.lane_timings[lane]} sec</li>`;
      }
      html += "</ul>";
    }

    trafficResults.innerHTML = html;

    // Scroll to results smoothly
    trafficResults.scrollIntoView({ behavior: "smooth" });
  })
  .catch(err => {
    console.error("❌ Error processing video:", err);
    trafficResults.innerHTML = `<p style="color:red;">Error processing video. Check console for details.</p>`;
  });
});
