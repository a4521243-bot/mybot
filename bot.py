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
# MENU
# =========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📱 Virtual Numbers - $200", callback_data="virtual")],
        [InlineKeyboardButton("📞 Federal Numbers - $500", callback_data="federal")],
        [InlineKeyboardButton("📨 SMS Service - $100", callback_data="sms")],
        [InlineKeyboardButton("✉️ Email Service - $150", callback_data="email")],
        [InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("💳 Deposit LTC", callback_data="deposit")]
    ])

# =========================
# START (PHOTO + WELCOME)
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users.add(update.effective_user.id)

    caption = (
        "👋 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗦𝗘𝗥𝗩𝗜𝗖𝗘 𝗕𝗢𝗧\n\n"
        "🔐 Anonymous & Secure Platform\n"
        "⚡ Instant Digital Services\n"
        "💎 Payment: Litecoin (LTC)\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📱 Virtual Numbers - $200\n"
        "📞 Federal Numbers - $500\n"
        "📨 SMS Service - $100\n"
        "✉️ Email Service - $150\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"👨‍💻 Support: {ADMIN_CONTACT}\n\n"
        "👇 Choose a service below:"
    )

    await update.message.reply_photo(
        photo=IMAGE_URL,
        caption=caption,
        reply_markup=main_menu()
    )

# =========================
# ADMIN PANEL
# =========================
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Access denied")
        return

    await update.message.reply_text(
        "🛠 ADMIN PANEL\n\nSelect option:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Stats", callback_data="admin_stats")],
            [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
        ])
    )

# =========================
# CALLBACK HANDLER
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    msg = query.message

    # ================= SERVICES =================
    if query.data == "virtual":
        await msg.reply_text(
            "📱 Virtual Numbers\n💵 $200\n💎 LTC Payment",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_virtual")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    elif query.data == "federal":
        await msg.reply_text(
            "📞 Federal Numbers\n💵 $500\n💎 LTC Payment",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_federal")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    elif query.data == "sms":
        await msg.reply_text(
            "📨 SMS Service\n💵 $100\n💎 LTC Payment",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_sms")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    elif query.data == "email":
        await msg.reply_text(
            "✉️ Email Service\n💵 $150\n💎 LTC Payment",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_email")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    # ================= BUY =================
    elif query.data.startswith("buy_"):
        await msg.reply_text(
            "🛒 PAYMENT REQUIRED\n\n"
            "💎 Pay with Litecoin (LTC)\n\n"
            f"📩 Address:\n`{DEPOSIT_ADDRESS}`\n\n"
            "⚡ Tap & hold to copy\n\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Copy Address", callback_data="copy")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    # ================= COPY =================
    elif query.data == "copy":
        await msg.reply_text(
            f"📋 LTC ADDRESS:\n\n`{DEPOSIT_ADDRESS}`\n\n⚡ Tap & hold to copy",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    # ================= BALANCE =================
    elif query.data == "balance":
        await msg.reply_text(
            "💰 BALANCE: $0\n💎 SYSTEM: LTC WALLET\n\n"
            f"👨‍💻 {ADMIN_CONTACT}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    # ================= DEPOSIT =================
    elif query.data == "deposit":
        await msg.reply_text(
            "💳 LTC DEPOSIT\n\n"
            f"📩 Address:\n`{DEPOSIT_ADDRESS}`\n\n"
            "⚡ Tap & hold to copy\n\n"
            f"👨‍💻 {ADMIN_CONTACT}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Copy Address", callback_data="copy")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    # ================= ADMIN STATS =================
    elif query.data == "admin_stats":

        if query.from_user.id != ADMIN_ID:
            return

        await msg.reply_text(
            f"📊 USERS: {len(users)}\n\n💰 SYSTEM ACTIVE",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="menu")]
            ])
        )

    # ================= MENU =================
    elif query.data == "menu":
        await msg.reply_text(
            "🏠 MAIN MENU\n\n💎 LTC SYSTEM ACTIVE",
            reply_markup=main_menu()
        )

# =========================
# MAIN
# =========================
def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
