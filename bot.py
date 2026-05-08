import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# =========================
# CONFIG
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 8721950488
ADMIN_CONTACT = "@mailnovacore"

# ⚠️ Litecoin address (replace with real if needed)
DEPOSIT_ADDRESS = "LRvMZHB6rYK2cbQWqJf2WhVgNbkUuceBDM"

IMAGE_URL = "https://i.ibb.co/7d0qYBfN/Chat-GPT-Image-May-8-2026-02-51-14-PM.png"

users = set()

# =========================
# START MESSAGE
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users.add(update.effective_user.id)

    keyboard = [
        [InlineKeyboardButton("📱 Virtual Numbers", callback_data="virtual_numbers")],
        [InlineKeyboardButton("📞 Federal Numbers", callback_data="federal_numbers")],
        [InlineKeyboardButton("📨 SMS Service", callback_data="sms_service")],
        [InlineKeyboardButton("✉️ Email Service", callback_data="email_service")],
        [InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("💳 Deposit LTC", callback_data="deposit")],
        [InlineKeyboardButton("🌍 Countries", callback_data="countries")],
    ]

    await update.message.reply_photo(
        photo=IMAGE_URL,
        caption=(
            "👋 Welcome to Services Bot!\n\n"
            "🔐 Anonymous & secure system\n"
            "⚡ Instant delivery services\n\n"
            "💎 Payments: Litecoin (LTC)\n\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}\n\n"
            "👇 Choose service:"
        ),
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
        text = "📱 Virtual Numbers\n💵 200 USD\n💎 Payment: LTC"
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_virtual")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    elif query.data == "federal_numbers":
        text = "📞 Federal Numbers\n💵 500 USD\n💎 Payment: LTC"
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_federal")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    elif query.data == "sms_service":
        text = "📨 SMS Service\n💵 100 USD/month\n💎 Payment: LTC"
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_sms")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    elif query.data == "email_service":
        text = "✉️ Email Service\n💵 150 USD\n💎 Payment: LTC"
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_email")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

    # ================= BUY =================
    elif query.data == "buy_virtual":
        text = (
            "🛒 Order: Virtual Number\n\n"
            "💎 Pay with Litecoin (LTC)\n\n"
            f"📩 Address:\n{DEPOSIT_ADDRESS}\n\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}"
        )

    elif query.data == "buy_federal":
        text = (
            "🛒 Order: Federal Number\n\n"
            "💎 Pay with Litecoin (LTC)\n\n"
            f"📩 Address:\n{DEPOSIT_ADDRESS}\n\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}"
        )

    elif query.data == "buy_sms":
        text = (
            "🛒 Order: SMS Service\n\n"
            "💎 Pay with Litecoin (LTC)\n\n"
            f"📩 Address:\n{DEPOSIT_ADDRESS}\n\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}"
        )

    elif query.data == "buy_email":
        text = (
            "🛒 Order: Email Service\n\n"
            "💎 Pay with Litecoin (LTC)\n\n"
            f"📩 Address:\n{DEPOSIT_ADDRESS}\n\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}"
        )

    # ================= OTHER =================
    elif query.data == "balance":
        text = f"💰 Balance: 0 USD\n💎 System: LTC Wallet\n\n👨‍💻 {ADMIN_CONTACT}"

    elif query.data == "deposit":
        text = (
            "💳 Litecoin Deposit\n\n"
            "💎 Network: LTC (Litecoin)\n\n"
            f"📩 Address:\n{DEPOSIT_ADDRESS}\n\n"
            f"👨‍💻 {ADMIN_CONTACT}"
        )

    elif query.data == "countries":
        text = "🌍 Available countries:\n🇺🇸 🇬🇧 🇨🇦 🇩🇪 🇫🇷 🇷🇴"

    # ================= BACK =================
    elif query.data == "back":

        keyboard = [
            [InlineKeyboardButton("📱 Virtual Numbers", callback_data="virtual_numbers")],
            [InlineKeyboardButton("📞 Federal Numbers", callback_data="federal_numbers")],
            [InlineKeyboardButton("📨 SMS Service", callback_data="sms_service")],
            [InlineKeyboardButton("✉️ Email Service", callback_data="email_service")],
            [InlineKeyboardButton("💰 Balance", callback_data="balance")],
            [InlineKeyboardButton("💳 Deposit LTC", callback_data="deposit")],
            [InlineKeyboardButton("🌍 Countries", callback_data="countries")],
        ]

        await query.edit_message_text(
            "🏠 Main Menu\n\n💎 LTC Payment System Active",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # ================= SAFE EDIT =================
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None
    )

# =========================
# ADMIN STATS
# =========================
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(f"📊 Total Users: {len(users)}")

# =========================
# MAIN
# =========================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
