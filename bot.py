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
# START (WELCOME + MENU)
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

    await update.message.reply_photo(
        photo=IMAGE_URL,
        caption=(
            "👋 Welcome to Virtual Services Bot!\n\n"
            "🔐 Anonymous & secure system\n"
            "⚡ Instant access services\n\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}\n\n"
            "👇 Choose a service below:"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================
# SAFE MESSAGE EDITOR
# =========================
async def safe_edit(query, text, keyboard):
    try:
        # try caption first (for photo messages)
        await query.edit_message_caption(
            caption=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except:
        # fallback to text
        await query.edit_message_text(
            text=text,
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

    # ================= MENU =================
    if query.data == "virtual_numbers":
        text = "📱 Virtual Numbers\n💵 Price: 200 USD"
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
        text = f"🛒 Virtual Number\n💳 Pay BTC\n👨‍💻 {ADMIN_CONTACT}"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]

    elif query.data == "buy_federal":
        text = f"🛒 Federal Number\n💳 Pay BTC\n👨‍💻 {ADMIN_CONTACT}"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]

    elif query.data == "buy_sms":
        text = f"🛒 SMS Service\n💳 Pay BTC\n👨‍💻 {ADMIN_CONTACT}"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]

    elif query.data == "buy_email":
        text = f"🛒 Email Service\n💳 Pay BTC\n👨‍💻 {ADMIN_CONTACT}"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]

    # ================= OTHER =================
    elif query.data == "balance":
        text = f"💰 Balance: 0 USD\n👨‍💻 {ADMIN_CONTACT}"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]

    elif query.data == "deposit":
        text = (
            "💳 Bitcoin Deposit\n\n"
            f"₿ Address:\n{DEPOSIT_ADDRESS}\n\n"
            f"👨‍💻 {ADMIN_CONTACT}"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]

    elif query.data == "countries":
        text = "🌍 Available countries:\n🇺🇸 🇬🇧 🇨🇦 🇩🇪 🇫🇷 🇷🇴"
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

        await safe_edit(query, "🏠 Main Menu\n\n👨‍💻 @mailnovacore", keyboard)
        return

    # ================= SAFE RESPONSE =================
    await safe_edit(query, text, keyboard)

# =========================
# ADMIN
# =========================
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(f"📊 Users: {len(users)}")

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
