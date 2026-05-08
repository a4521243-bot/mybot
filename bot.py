import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# =========================
# CONFIG
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 8721950488
ADMIN_CONTACT = "@mailnovacore"

DEPOSIT_ADDRESS = "LRvMZHB6rYK2cbQWqJf2WhVgNbkUuceBDM"

IMAGE_URL = "https://i.ibb.co/7d0qYBfN/Chat-GPT-Image-May-8-2026-02-51-14-PM.png"

users = set()

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users.add(update.effective_user.id)

    keyboard = [
        [InlineKeyboardButton("📱 Virtual Numbers", callback_data="virtual_numbers")],
        [InlineKeyboardButton("📞 Federal Numbers", callback_data="federal_numbers")],
        [InlineKeyboardButton("📨 SMS Service", callback_data="sms_service")],
        [InlineKeyboardButton("✉️ Email Service", callback_data="email_service")],
        [InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("💳 Deposit", callback_data="deposit")],
        [InlineKeyboardButton("🌍 Countries", callback_data="countries")],
    ]

    text = (
        "👋 Welcome to Virtual Services Bot!\n\n"
        "🔐 Anonymous & secure system\n"
        "👨‍💻 Support: @mailnovacore\n\n"
        "to start:/start\n\n"
        "Choose service below:"
    )

    await update.message.reply_photo(
        photo=IMAGE_URL,
        caption=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================
# BUTTON HANDLER (FIXED 100%)
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = "⚠️ Error"
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]

    # ================= MENU =================
    if query.data == "virtual_numbers":
        text = "📱 Virtual Numbers\n💵 Price: 200 USD\n📞 Calling supported"
        keyboard = [
            [InlineKeyboardButton("🛒 Buy", callback_data="buy_virtual")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    elif query.data == "federal_numbers":
        text = "📞 Federal Numbers\n💵 Price: 500 USD"
        keyboard = [
            [InlineKeyboardButton("🛒 Buy", callback_data="buy_federal")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    elif query.data == "sms_service":
        text = "📨 SMS Service\n💵 Price: 100 USD/month"
        keyboard = [
            [InlineKeyboardButton("🛒 Buy", callback_data="buy_sms")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    elif query.data == "email_service":
        text = "✉️ Email Service\n💵 Price: 150 USD"
        keyboard = [
            [InlineKeyboardButton("🛒 Buy", callback_data="buy_email")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    # ================= BUY =================
    elif query.data == "buy_virtual":
        text = f"🛒 Virtual Number selected\n💳 Pay BTC\n👨‍💻 {ADMIN_CONTACT}"

    elif query.data == "buy_federal":
        text = f"🛒 Federal Number selected\n💳 Pay BTC\n👨‍💻 {ADMIN_CONTACT}"

    elif query.data == "buy_sms":
        text = f"🛒 SMS Service selected\n💳 Pay BTC\n👨‍💻 {ADMIN_CONTACT}"

    elif query.data == "buy_email":
        text = f"🛒 Email Service selected\n💳 Pay BTC\n👨‍💻 {ADMIN_CONTACT}"

    # ================= OTHER =================
    elif query.data == "balance":
        text = f"💰 Balance: 0 USD\n👨‍💻 {ADMIN_CONTACT}"

    elif query.data == "deposit":
        text = (
            "💳 Bitcoin Deposit\n\n"
            f"₿ Address:\n{DEPOSIT_ADDRESS}\n\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}\n\n"
            "⚠️ Send exact amount only."
        )

    elif query.data == "countries":
        text = (
            "🌍 Services available:\n\n"
            "🇺🇸 USA 🇬🇧 UK 🇨🇦 Canada\n"
            "🇩🇪 Germany 🇫🇷 France 🇷🇴 Romania\n\n"
            f"👨‍💻 {ADMIN_CONTACT}"
        )

    # ================= BACK =================
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("📱 Virtual Numbers", callback_data="virtual_numbers")],
            [InlineKeyboardButton("📞 Federal Numbers", callback_data="federal_numbers")],
            [InlineKeyboardButton("📨 SMS Service", callback_data="sms_service")],
            [InlineKeyboardButton("✉️ Email Service", callback_data="email_service")],
            [InlineKeyboardButton("💰 Balance", callback_data="balance")],
            [InlineKeyboardButton("💳 Deposit", callback_data="deposit")],
            [InlineKeyboardButton("🌍 Countries", callback_data="countries")],
        ]

        await query.edit_message_text(
            "🏠 Main Menu\n\n👨‍💻 @mailnovacore",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # ================= SAFE SEND (NO CRASH EVER) =================
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================
# ADMIN
# =========================
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Access denied")
        return

    await update.message.reply_text(
        "🛠 Admin Panel\n\n"
        "/stats - users count"
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(f"📊 Total Users: {len(users)}")

# =========================
# MAIN
# =========================
def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN missing!")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
