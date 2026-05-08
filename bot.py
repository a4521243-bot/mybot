import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# =========================
# CONFIG
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8721950488  # შეცვალე შენი Telegram ID

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
        "🔐 Your anonymity is protected.\n"
        "No personal data is stored.\n\n"
        f"👨‍💻 Support: {ADMIN_CONTACT}\n\n"
        "Choose a service below:"
    )

    await update.message.reply_photo(
        photo=IMAGE_URL,
        caption=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================
# BUTTON HANDLER
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = []

    # ================= SERVICES =================
    if query.data == "virtual_numbers":
        text = (
            "📱 Virtual Numbers\n"
            "💵 Price: 200 USD\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}"
        )
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_virtual")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    elif query.data == "federal_numbers":
        text = (
            "📞 Federal Numbers\n"
            "💵 Price: 500 USD\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}"
        )
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_federal")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    elif query.data == "sms_service":
        text = (
            "📨 SMS Service\n"
            "💵 Price: 100 USD/month\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}"
        )
        keyboard = [
            [InlineKeyboardButton("🛒 Subscribe", callback_data="buy_sms")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    elif query.data == "email_service":
        text = (
            "✉️ Email Service\n"
            "💵 Price: 150 USD\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}"
        )
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_email")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    # ================= BUY ACTIONS =================
    elif query.data == "buy_virtual":
        text = f"🛒 Virtual Number selected\n💳 Pay via Bitcoin\n👨‍💻 Support: {ADMIN_CONTACT}"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]

    elif query.data == "buy_federal":
        text = f"🛒 Federal Number selected\n💳 BTC payment required\n👨‍💻 Support: {ADMIN_CONTACT}"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]

    elif query.data == "buy_sms":
        text = f"🛒 SMS Subscription selected\n💳 Send BTC payment\n👨‍💻 Support: {ADMIN_CONTACT}"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]

    elif query.data == "buy_email":
        text = f"🛒 Email Service selected\n💳 BTC payment required\n👨‍💻 Support: {ADMIN_CONTACT}"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]

    # ================= OTHER =================
    elif query.data == "balance":
        text = f"💰 Balance: 0 USD\n👨‍💻 Support: {ADMIN_CONTACT}"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]

    elif query.data == "deposit":
        text = (
            "💳 Bitcoin Deposit\n\n"
            f"₿ Address:\n{DEPOSIT_ADDRESS}\n\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}\n\n"
            "⚠️ Send exact amount only."
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]

    elif query.data == "countries":
        text = (
            "🌍 Services available in:\n\n"
            "🇺🇸 USA\n🇬🇧 UK\n🇨🇦 Canada\n🇩🇪 Germany\n"
            "🇫🇷 France\n🇷🇴 Romania\n🇳🇱 Netherlands\n🇵🇱 Poland\n\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]

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
            f"🏠 Main Menu\n\n👨‍💻 Support: {ADMIN_CONTACT}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# =========================
# ADMIN PANEL
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

    await update.message.reply_text(
        f"📊 Total Users: {len(users)}"
    )

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

    print("Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
