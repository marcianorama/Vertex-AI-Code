from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/locations", methods=["GET"])
def locations():
    q = request.args.get("q", "Coffee")
    location = request.args.get("location", "Austin, Texas, United States")
    hl = request.args.get("hl", "en")
    gl = request.args.get("gl", "us")
    google_domain = request.args.get("google_domain", "google.com")
    api_key = request.args.get("api_key", "YOUR_UPSTREAM_API_KEY")
    try:
        r = requests.get(
            "https://petstore-demo.apidog.com/pet/findByStatus",
            params={
                "q": q,
                "location": location,
                "hl": hl,
                "gl": gl,
                "google_domain": google_domain,
                "api_key": api_key
            },
            timeout=(5, 30),   # 5s connect, 30s read
        )
        r.raise_for_status()
        return jsonify(r.json()), 200
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to upstream API timed out"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502

