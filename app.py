from flask import Flask, render_template, request, redirect, flash, url_for
import requests
from config import *

app = Flask(__name__)
app.secret_key = 'secret123'

# 📊 گرفتن آمار از یوتیوب
def get_youtube_stats():
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    stats = data['items'][0]['statistics']
    return {
        "subscribers": f"{int(stats['subscriberCount']):,}",
        "views": f"{int(stats['viewCount']):,}",
        "videos": stats['videoCount']
    }

# 📩 ارسال پیام به تلگرام
def send_telegram(name, email, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    text = f"📩 پیام جدید از سایت\n👤 نام: {name}\n✉️ ایمیل: {email}\n📝 پیام:\n{message}"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=data)

# 🏠 صفحه اصلی
@app.route("/", methods=["GET"])
def home():
    stats = get_youtube_stats()
    return render_template("index.html", stats=stats)

# 📬 فرم تماس
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    try:
        send_telegram(name, email, message)
        flash("✅ پیام شما با موفقیت به تلگرام ارسال شد")
    except:
        flash("❌ ارسال پیام به تلگرام با خطا مواجه شد")

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
