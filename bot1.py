import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request
import threading

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Đặt biến môi trường trên Render
API_URL = "https://blrx-ban-bancheck.vercel.app/check_banned"

async def check_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Vui lòng nhập UID. Ví dụ: /check 2260069951")
        return
    uid = context.args[0]
    params = {"uid": uid, "key": "blrx_ban"}
    resp = requests.get(API_URL, params=params)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("is_banned"):
            msg = f"UID {uid} đã bị BAN."
        else:
            msg = f"UID {uid} KHÔNG bị BAN."
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("Lỗi khi kiểm tra UID.")

# Flask app cho cron-job.org
app_flask = Flask(__name__)

@app_flask.route("/cron", methods=["GET"])
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
        # Gửi tin nhắn về Telegram
        requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            params={"chat_id": chat_id, "text": msg}
        )
        return "Đã gửi kết quả", 200
    return "Lỗi khi kiểm tra UID", 500

def start_telegram():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("check", check_ban))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=start_telegram).start()
    app_flask.run(host="0.0.0.0", port=10000) 