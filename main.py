import json
import random
import datetime
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

# --- Configuration ---
TOKEN = "7408316421:AAFqxaB39EtKCepdAO-8X-4uJMna92OfecM"  # ✅ Apna actual token yahan daal
USERS_FILE = "users.json"
ADMIN_ID = 7098681454
ASK_USERNAME, ASK_PASSWORD, ASK_WALLET = range(3)

REQUIRED_CHANNELS = [
    ("@ffprivatesensi", "STAR NODE-1"),
    ("@webmakerhu", "STAR NODE-2"),
    ("@botclubhu", "STAR NODE-3")
]

DAILY_QUIZ_QUESTION = {
    "question": "Which command is used to find hidden ports in a system?\n\nA. Nmap\nB. SQLmap\nC. Hydra\nD. Nikto",
    "answer": "a"
}

REFERRAL_REWARD = 10
MIN_REFERRALS_FOR_WITHDRAW = 100

# --- Helper Functions ---
def load_json(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gif_url = "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif"
    await context.bot.send_animation(chat_id=update.effective_chat.id, animation=gif_url)

    keyboard = [
        [InlineKeyboardButton(f"{name}", url=f"https://t.me/{channel[1:]}")]
        for channel, name in REQUIRED_CHANNELS
    ]
    keyboard.append([InlineKeyboardButton("✅ I Have Joined", callback_data="check_join")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚨 ACCESS REQUIRED 🚨\n\n"
        "⚠️ Join All STAR NODES To Unlock The Bot Features!\n\n"
        "👨‍💻 Developer Node: @teamtoxic009",
        reply_markup=reply_markup
    )

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_joined = True  # ✅ Yahan actual join check later add karna

    if user_joined:
        await query.edit_message_text("✅ ACCESS GRANTED. Welcome Star User! Use /register to begin registration.")
    else:
        await query.edit_message_text("🚫 ACCESS DENIED. First Join All STAR NODES!")

# --- Flask Server ---
def start_flask():
    app = Flask('')

    @app.route('/')
    def home():
        return "🌟 Star Bot is Running!"

    app.run(host="0.0.0.0", port=8080)

# --- Main Bot Function ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))

    print("🤖 Telegram bot started with polling...")
    app.run_polling()

# --- Run Both Flask + Bot ---
if __name__ == "__main__":
    threading.Thread(target=start_flask).start()
    main()
