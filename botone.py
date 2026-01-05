import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# 1. إعداد سيرفر Flask (لإبقاء البوت حياً على Render)
app = Flask(name)

@app.route('/')
def home():
    return "Botone is Online!"

def run():
    # Render يستخدم المنفذ 10000 افتراضياً في أغلب الأحيان
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. إعداد بوت تلجرام
# سيحاول الكود جلب التوكن من "Environment Variables" في ريندر
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# رسالة الترحيب /start مع الأزرار
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('خدماتنا')
    btn2 = types.KeyboardButton('اتصل بنا')
    markup.add(btn1, btn2)
    
    welcome_msg = "مرحباً بك في بوت botone! 🤖\nكيف يمكنني مساعدتك اليوم؟"
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup)

# التعامل مع الضغط على الأزرار
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text == "خدماتنا":
        bot.send_message(message.chat.id, "✅ نحن نقدم خدمات برمجية وإنشاء بوتات ذكية.")
    elif message.text == "اتصل بنا":
        bot.send_message(message.chat.id, "📧 يمكنك التواصل مع المطور عبر: @your_username")
    else:
        bot.reply_to(message, "لم أفهم هذا الأمر، جرب استخدام الأزرار.")

# 3. تشغيل البوت والسيرفر
if __name__ == "__main__":
    print("Starting bot...")
    keep_alive()  # تشغيل السيرفر في الخلفية
    bot.infinity_polling() # تشغيل استقبال رسائل تلجرام
