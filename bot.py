import os
import requests
from flask import Flask, request

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = "https://blrx-ban-bancheck.vercel.app/check_banned"
BOT_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

app = Flask(__name__)

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        if text.startswith("/check"):
            parts = text.split()
            if len(parts) == 2:
                uid = parts[1]
                params = {"uid": uid, "key": "blrx_ban"}
                resp = requests.get(API_URL, params=params)
                if resp.status_code == 200:
                    d = resp.json()
                    if d.get("is_banned"):
                        msg = f"UID {uid} đã bị BAN."
                    else:
                        msg = f"UID {uid} KHÔNG bị BAN."
                else:
                    msg = "Lỗi khi kiểm tra UID."
            else:
                msg = "Vui lòng nhập UID. Ví dụ: /check 2260069951"
            requests.get(
                f"{BOT_URL}/sendMessage",
                params={"chat_id": chat_id, "text": msg}
            )
    return "ok"

@app.route("/cron", methods=["GET"])
def cron_check():
    uid = request.args.get("uid")
    chat_id = request.args.get("chat_id")
    if not uid or not chat_id:
        return "Thiếu uid hoặc chat_id", 400
    params = {"uid": uid, "key": "blrx_ban"}
    resp = requests.get(API_URL, params=params)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("is_banned"):
            msg = f"UID {uid} đã bị BAN."
        else:
            msg = f"UID {uid} KHÔNG bị BAN."
        requests.get(
            f"{BOT_URL}/sendMessage",
            params={"chat_id": chat_id, "text": msg}
        )
        return "Đã gửi kết quả", 200
    return "Lỗi khi kiểm tra UID", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000) 