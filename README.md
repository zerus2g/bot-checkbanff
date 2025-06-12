# Bot Telegram Check Ban Free Fire

## Chức năng
- Kiểm tra UID Free Fire có bị ban không qua API: https://blrx-ban-bancheck.vercel.app/check_banned
- Hỗ trợ lệnh Telegram: `/check <uid>`
- Hỗ trợ endpoint cho cron-job.org để tự động kiểm tra UID và gửi kết quả về Telegram

## Cài đặt
1. Cài Python 3.8+
2. Cài thư viện:
   ```bash
   pip install -r requirements.txt
   ```
3. Tạo bot Telegram qua @BotFather, lấy token và đặt vào biến môi trường `TELEGRAM_TOKEN`

## Chạy bot
```bash
python bot.py
```

## Deploy trên Render.com
- Đưa toàn bộ mã nguồn lên GitHub
- Deploy repo lên Render.com (Python)
- Đặt biến môi trường `TELEGRAM_TOKEN`
- Lệnh start: `python bot.py`

## Sử dụng cron-job.org
- Tạo job GET tới:
  ```
  https://<your-render-app>.onrender.com/cron?uid=<UID>&chat_id=<CHAT_ID>
  ```
- Để lấy `chat_id`: Nhắn /start cho bot, sau đó truy cập:
  ```
  https://api.telegram.org/bot<TELEGRAM_TOKEN>/getUpdates
  ```
  và tìm `chat.id` trong kết quả.

## Liên hệ
- Credits API: [@blrxban](https://t.me/bot_bx_ban) 