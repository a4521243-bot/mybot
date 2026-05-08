import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 8721950488
ADMIN_CONTACT = "@mailnovacore"

DEPOSIT_ADDRESS = "LRvMZHB6rYK2cbQWqJf2WhVgNbkUuceBDM"

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

    await update.message.reply_text(
        "👋 Welcome to Virtual Services Bot!\n\n"
        "🔐 Anonymous system\n"
        f"👨‍💻 Support: {ADMIN_CONTACT}\n\n"
        "👇 Choose service:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================
# BUTTON HANDLER
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    text = ""
    keyboard = []

    # ================= SERVICES =================
    if query.data == "virtual_numbers":
        text = "📱 Virtual Numbers\n💵 Price: 200 USD"
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_virtual")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    elif query.data == "federal_numbers":
        text = "📞 Federal Numbers\n💵 Price: 500 USD"
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_federal")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    elif query.data == "sms_service":
        text = "📨 SMS Service\n💵 100 USD/month"
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_sms")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    elif query.data == "email_service":
        text = "✉️ Email Service\n💵 150 USD"
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_email")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    # ================= BUY =================
    elif query.data == "buy_virtual":
        text = (
            "🛒 Virtual Number Purchase\n\n"
            "💳 Pay via Bitcoin:\n"
            f"{DEPOSIT_ADDRESS}\n\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}"
        )

    elif query.data == "buy_federal":
        text = (
            "🛒 Federal Number Purchase\n\n"
            "💳 Pay via Bitcoin:\n"
            f"{DEPOSIT_ADDRESS}\n\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}"
        )

    elif query.data == "buy_sms":
        text = (
            "🛒 SMS Service Purchase\n\n"
            "💳 Pay via Bitcoin:\n"
            f"{DEPOSIT_ADDRESS}\n\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}"
        )

    elif query.data == "buy_email":
        text = (
            "🛒 Email Service Purchase\n\n"
            "💳 Pay via Bitcoin:\n"
            f"{DEPOSIT_ADDRESS}\n\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}"
        )

    # ================= OTHER =================
    elif query.data == "balance":
        text = f"💰 Balance: 0 USD\n\n👨‍💻 {ADMIN_CONTACT}"

    elif query.data == "deposit":
        text = (
            "💳 Deposit BTC\n\n"
            f"Address:\n{DEPOSIT_ADDRESS}\n\n"
            f"👨‍💻 {ADMIN_CONTACT}"
        )

    elif query.data == "countries":
        text = "🌍 Available: USA, UK, Canada, Germany, France, Romania"

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

    # ================= SAFE OUTPUT =================
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None
    )

# =========================
# MAIN
# =========================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
