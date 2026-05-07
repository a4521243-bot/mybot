from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

import os

TOKEN = os.getenv("BOT_TOKEN")

# USER BALANCES
user_balances = {}


# =========================
# START MENU
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in user_balances:
        user_balances[user_id] = 0.00

    balance = user_balances[user_id]

    keyboard = [
        [InlineKeyboardButton("📞 VOIP Calls", callback_data="voip")],
        [InlineKeyboardButton("📧 Bulk Email", callback_data="email")],
        [InlineKeyboardButton("💰 Deposit", callback_data="deposit")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"""
🔥 Welcome To Premium Services 🔥

👤 User ID: {user_id}
💰 Balance: ${balance:.2f}

Choose option:
""",
        reply_markup=reply_markup
    )


# =========================
# CALLBACK HANDLER
# =========================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    balance = user_balances.get(user_id, 0.00)

    # =========================
    # VOIP MENU
    # =========================
    if query.data == "voip":

        keyboard = [
            [InlineKeyboardButton("🇺🇸 American Phone Numbers", callback_data="usa_numbers")],
            [InlineKeyboardButton("🇨🇦 Canadian Phone Numbers", callback_data="canada_numbers")],
            [InlineKeyboardButton("Unlimited Federal Numbers", callback_data="federal")],
            [InlineKeyboardButton("⬅ Back", callback_data="back")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"""
📞 VOIP Services

💰 Your Balance: ${balance:.2f}
""",
            reply_markup=reply_markup
        )

    # =========================
    # EMAIL MENU
    # =========================
    elif query.data == "email":

        keyboard = [
            [InlineKeyboardButton("Unlimited Email Sending", callback_data="sending")],
            [InlineKeyboardButton("⬅ Back", callback_data="back")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"""
📧 Bulk Email Services

💰 Your Balance: ${balance:.2f}
""",
            reply_markup=reply_markup
        )

    # =========================
    # FEDERAL PRODUCT ($300)
    # =========================
    elif query.data == "federal":

        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_federal")],
            [InlineKeyboardButton("⬅ Back", callback_data="voip")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"""
📞 Unlimited Federal Numbers

💵 Price: $300 / Month
💰 Your Balance: ${balance:.2f}
""",
            reply_markup=reply_markup
        )

    # =========================
    # USA NUMBERS ($100)
    # =========================
    elif query.data == "usa_numbers":

        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_usa")],
            [InlineKeyboardButton("⬅ Back", callback_data="voip")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"""
🇺🇸 American Phone Numbers

💵 Price: $100 / Month
💰 Your Balance: ${balance:.2f}
""",
            reply_markup=reply_markup
        )

    # =========================
    # CANADA NUMBERS ($100)
    # =========================
    elif query.data == "canada_numbers":

        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_canada")],
            [InlineKeyboardButton("⬅ Back", callback_data="voip")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"""
🇨🇦 Canadian Phone Numbers

💵 Price: $100 / Month
💰 Your Balance: ${balance:.2f}
""",
            reply_markup=reply_markup
        )

    # =========================
    # EMAIL PRODUCT ($300)
    # =========================
    elif query.data == "sending":

        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_email")],
            [InlineKeyboardButton("⬅ Back", callback_data="email")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"""
📧 Unlimited Email Sending

💵 Price: $300 / Month
💰 Your Balance: ${balance:.2f}
""",
            reply_markup=reply_markup
        )

    # =========================
    # BUY FEDERAL
    # =========================
    elif query.data == "buy_federal":

        if balance >= 300:
            user_balances[user_id] -= 300
            await query.answer("Purchase Successful ✅", show_alert=True)
        else:
            await query.answer(
                "❌ Insufficient balance. Please top up your account first.",
                show_alert=True
            )

    # =========================
    # BUY USA
    # =========================
    elif query.data == "buy_usa":

        if balance >= 100:
            user_balances[user_id] -= 100
            await query.answer("Purchase Successful ✅", show_alert=True)
        else:
            await query.answer(
                "❌ Insufficient balance. Please top up your account first.",
                show_alert=True
            )

    # =========================
    # BUY CANADA
    # =========================
    elif query.data == "buy_canada":

        if balance >= 100:
            user_balances[user_id] -= 100
            await query.answer("Purchase Successful ✅", show_alert=True)
        else:
            await query.answer(
                "❌ Insufficient balance. Please top up your account first.",
                show_alert=True
            )

    # =========================
    # DEPOSIT
    # =========================
    elif query.data == "deposit":

        keyboard = [
            [InlineKeyboardButton("⬅ Back", callback_data="back")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"""
💰 Deposit Balance

💵 Current Balance: ${balance:.2f}

Send LTC (Litecoin) to:

LRvMZHB6rYK2cbQWqJf2WhVgNbkUuceBDM

⚠ After payment contact admin @mailnovacore.
""",
            reply_markup=reply_markup
        )

    # =========================
    # EMAIL MENU (placeholder)
    # =========================
    elif query.data == "sending":

        keyboard = [
            [InlineKeyboardButton("⬅ Back", callback_data="email")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"""
📧 Bulk Email Services

💰 Your Balance: ${balance:.2f}
""",
            reply_markup=reply_markup
        )

    # =========================
    # BACK
    # =========================
    elif query.data == "back":

        keyboard = [
            [InlineKeyboardButton("📞 VOIP Calls", callback_data="voip")],
            [InlineKeyboardButton("📧 Bulk Email", callback_data="email")],
            [InlineKeyboardButton("💰 Deposit", callback_data="deposit")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"""
🔥 Welcome To Premium Services 🔥

👤 User ID: {user_id}
💰 Balance: ${balance:.2f}

Choose option:
""",
            reply_markup=reply_markup
        )


# =========================
# RUN BOT
# =========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot Running...")
app.run_polling()
