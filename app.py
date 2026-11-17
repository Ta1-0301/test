
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

state = {"enabled": False}

HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
        content="width=device-width, initial-scale=1">
  <title>Raspberry Pi Control</title>
  <style>
    body {
      font-family: sans-serif;
      background: #f4f5f7;
      text-align: center;
      padding: 40px 16px;
    }
    .panel {
      max-width: 360px;
      margin: auto;
      background: white;
      padding: 30px;
      border-radius: 18px;
      box-shadow: 0 3px 16px #0001;
    }
    button {
      width: 100%;
      padding: 18px;
      margin-top: 12px;
      border: none;
      border-radius: 10px;
      font-size: 18px;
      background: #222;
      color: white;
    }
  </style>
</head>
<body>
  <div class="panel">
    <h2>Raspberry Pi 5</h2>
    <p>Device Control</p>
    <h3 id="status">Loading...</h3>
    <button onclick="setDevice(true)">ON</button>
    <button onclick="setDevice(false)">OFF</button>
  </div>
<script>
async function refresh() {
  const r = await fetch("/status");
  const data = await r.json();
  document.getElementById("status").textContent =
    data.enabled ? "Status: ON" : "Status: OFF";
}
async function setDevice(enabled) {
  await fetch("/control/" + (enabled ? "on" : "off"),
              {method: "POST"});
  await refresh();
}
refresh();
</script>
</body>
</html>
"""

@app.get("/")
def index():
    return render_template_string(HTML)

@app.get("/status")
def status():
    return jsonify(state)

@app.post("/control/<action>")
def control(action):
    if action not in ("on", "off"):
        return jsonify({"error": "Invalid action"}), 400

    state["enabled"] = action == "on"
    return jsonify(state)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
