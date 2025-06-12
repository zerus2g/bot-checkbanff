import os
import requests
from flask import Flask, request, jsonify
import datetime

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
                        msg = (
                            f"🔎 <b>Kết quả kiểm tra UID Free Fire</b>:\n"
                            f"• <b>UID:</b> <code>{uid}</code>\n"
                            f"• <b>Trạng thái:</b> 🚫 <b>BỊ BAN</b>"
                        )
                    else:
                        msg = (
                            f"🔎 <b>Kết quả kiểm tra UID Free Fire</b>:\n"
                            f"• <b>UID:</b> <code>{uid}</code>\n"
                            f"• <b>Trạng thái:</b> ✅ <b>KHÔNG bị BAN</b>"
                        )
                else:
                    msg = "<b>Lỗi khi kiểm tra UID.</b>"
            else:
                msg = "<b>Vui lòng nhập UID. Ví dụ: /check 2260069951</b>"
            requests.get(
                f"{BOT_URL}/sendMessage",
                params={
                    "chat_id": chat_id,
                    "text": msg,
                    "parse_mode": "HTML"
                }
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
            msg = (
                f"🔎 <b>Kết quả kiểm tra UID Free Fire</b>:\n"
                f"• <b>UID:</b> <code>{uid}</code>\n"
                f"• <b>Trạng thái:</b> 🚫 <b>BỊ BAN</b>"
            )
        else:
            msg = (
                f"🔎 <b>Kết quả kiểm tra UID Free Fire</b>:\n"
                f"• <b>UID:</b> <code>{uid}</code>\n"
                f"• <b>Trạng thái:</b> ✅ <b>KHÔNG bị BAN</b>"
            )
        requests.get(
            f"{BOT_URL}/sendMessage",
            params={
                "chat_id": chat_id,
                "text": msg,
                "parse_mode": "HTML"
            }
        )
        return "Đã gửi kết quả", 200
    return "Lỗi khi kiểm tra UID", 500

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({
        "status": "ok",
        "message": "pong",
        "time": datetime.datetime.utcnow().isoformat() + "Z"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000) 