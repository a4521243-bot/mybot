import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_CONTACT = "@mailnovacore"
DEPOSIT_ADDRESS = "LRvMZHB6rYK2cbQWqJf2WhVgNbkUuceBDM"

users = set()

# =========================
# MENU BUILDER
# =========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📱 Virtual Numbers", callback_data="virtual")],
        [InlineKeyboardButton("📞 Federal Numbers", callback_data="federal")],
        [InlineKeyboardButton("📨 SMS Service", callback_data="sms")],
        [InlineKeyboardButton("✉️ Email Service", callback_data="email")],
        [InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("💳 Deposit LTC", callback_data="deposit")],
    ])

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users.add(update.effective_user.id)

    await update.message.reply_text(
        "👋 Welcome to Services Bot\n\n"
        "💎 Payments: Litecoin (LTC)\n"
        f"👨‍💻 Support: {ADMIN_CONTACT}\n\n"
        "👇 Choose service:",
        reply_markup=main_menu()
    )

# =========================
# BUTTONS (NO EDIT = NO BUGS)
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    msg = query.message

    # ================= SERVICES =================
    if query.data == "virtual":
        await msg.reply_text(
            "📱 Virtual Numbers\n💵 200 USD\n💎 LTC Payment",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Buy", callback_data="buy_virtual")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    elif query.data == "federal":
        await msg.reply_text(
            "📞 Federal Numbers\n💵 500 USD\n💎 LTC Payment",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Buy", callback_data="buy_federal")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    elif query.data == "sms":
        await msg.reply_text(
            "📨 SMS Service\n💵 100 USD\n💎 LTC Payment",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Buy", callback_data="buy_sms")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    elif query.data == "email":
        await msg.reply_text(
            "✉️ Email Service\n💵 150 USD\n💎 LTC Payment",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Buy", callback_data="buy_email")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    # ================= BUY =================
    elif query.data.startswith("buy_"):
        await msg.reply_text(
            "🛒 Payment Instructions\n\n"
            "💎 Pay with Litecoin (LTC)\n\n"
            f"📩 Address:\n{DEPOSIT_ADDRESS}\n\n"
            f"👨‍💻 {ADMIN_CONTACT}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    # ================= BALANCE =================
    elif query.data == "balance":
        await msg.reply_text(
            "💰 Balance: 0 USD\n💎 System: LTC Wallet",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    # ================= DEPOSIT =================
    elif query.data == "deposit":
        await msg.reply_text(
            "💳 Litecoin Deposit\n\n"
            f"📩 Address:\n{DEPOSIT_ADDRESS}\n\n"
            f"👨‍💻 {ADMIN_CONTACT}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    # ================= BACK MENU =================
    elif query.data == "menu":
        await msg.reply_text(
            "🏠 Main Menu",
            reply_markup=main_menu()
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
