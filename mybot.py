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

TOKEN = os.getenv("8635819324:AAE15BelFEgaQUcokxZAMBTiUqS4EWC93MQ")

# USER BALANCES
user_balances = {}


# =========================
# MAIN MENU
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    # Default balance
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
# BUTTON SYSTEM
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
            [
                InlineKeyboardButton(
                    "Unlimited Federal Numbers",
                    callback_data="federal"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="back"
                )
            ]
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
            [
                InlineKeyboardButton(
                    "Unlimited Email Sending",
                    callback_data="sending"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="back"
                )
            ]
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
    # FEDERAL PRODUCT
    # =========================
    elif query.data == "federal":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🛒 Buy Now",
                    callback_data="buy_federal"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="voip"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"""
📞 Unlimited Federal Numbers

✅ Unlimited Calls
✅ USA Numbers
✅ Fast Setup
✅ 24/7 Support

💵 Price: $300 / Month
💰 Your Balance: ${balance:.2f}
""",
            reply_markup=reply_markup
        )

    # =========================
    # EMAIL PRODUCT
    # =========================
    elif query.data == "sending":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🛒 Buy Now",
                    callback_data="buy_email"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="email"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"""
📧 Unlimited Email Sending

✅ Unlimited Emails
✅ SMTP Included
✅ High Inbox Rate
✅ Fast Delivery

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

            await query.answer(
                "Purchase Successful ✅",
                show_alert=True
            )

        else:

            await query.answer(
                "Please deposit balance first.",
                show_alert=True
            )

    # =========================
    # BUY EMAIL
    # =========================
    elif query.data == "buy_email":

        if balance >= 300:

            user_balances[user_id] -= 300

            await query.answer(
                "Purchase Successful ✅",
                show_alert=True
            )

        else:

            await query.answer(
                "Please deposit balance first.",
                show_alert=True
            )

    # =========================
    # DEPOSIT
    # =========================
    elif query.data == "deposit":

        keyboard = [
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="back"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"""
💰 Deposit Balance

💵 Current Balance: ${balance:.2f}

Send USDT (TRC20) to:

TExampleWallet123456789

⚠ After payment contact admin.
""",
            reply_markup=reply_markup
        )

    # =========================
    # BACK BUTTON
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