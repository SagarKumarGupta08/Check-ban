from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/check_ban/<uid>")
def check_ban(uid):
    url = f"https://ff.garena.com/en/checkban?uid={uid}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        return jsonify({"status": 500, "error": "request_failed"})

    if r.status_code != 200:
        return jsonify({"status": 500, "error": "site_down"})

    html = r.text.lower()

    if "banned" in html:
        return jsonify({
            "status": 200,
            "data": {
                "is_banned": 1,
                "period": "Permanent"
            }
        })

    return jsonify({
        "status": 200,
        "data": {
            "is_banned": 0,
            "period": "N/A"
        }
    })

# Vercel entry
def handler(request, context):
    return app(request, context)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
