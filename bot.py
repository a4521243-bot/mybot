from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")
BTC_WALLET = "17hQJ4sGmt4yMniMfAfjEgRvAPPCnycfdc"

ADMIN_ID = 8721950488

users = set()
balances = {}  # 👈 NEW: user balances

WELCOME_IMAGE = "https://i.imgur.com/yourimage.jpg"


products = {
    "vip_service": {"name": "VIP Service", "price": 50},
    "premium_tool": {"name": "Premium Tool", "price": 100},
    "rolex_sub": {"name": "Rolex Submariner", "price": 12000},
    "ap_watch": {"name": "Audemars Piguet Royal Oak", "price": 25000},
    "paris_tour": {"name": "Luxury Paris Tour", "price": 3000},
    "dubai_tour": {"name": "Dubai VIP Experience", "price": 5000},
    "vip_concert": {"name": "VIP Concert Access", "price": 1500},
    "formula1": {"name": "F1 VIP Event Ticket", "price": 8000},
}


def get_balance(user_id: int):
    return balances.get(user_id, 0)


def is_admin(user_id: int):
    return user_id == ADMIN_ID


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Shop", callback_data="shop")],
        [InlineKeyboardButton("💰 Deposit", callback_data="deposit")],
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
        [InlineKeyboardButton("💳 Balance", callback_data="balance")],
        [InlineKeyboardButton("🔄 Restart", callback_data="restart")],
    ])


def shop_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⌚ Watches", callback_data="cat_watches")],
        [InlineKeyboardButton("✈️ Tours", callback_data="cat_tours")],
        [InlineKeyboardButton("🎫 Events", callback_data="cat_events")],
        [InlineKeyboardButton("💻 Services", callback_data="cat_services")],
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ])


def category_menu(items, back_to="shop"):
    keyboard = []
    for key, item in items:
        keyboard.append([
            InlineKeyboardButton(
                f"{item['name']} - ${item['price']}",
                callback_data=f"buy_{key}"
            )
        ])
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=back_to)])
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)

    if user_id not in balances:
        balances[user_id] = 0  # 👈 default balance = 0

    await update.message.reply_photo(
        photo=WELCOME_IMAGE,
        caption="👑 Welcome to Luxury Store Bot\n\nBalance: $0",
        reply_markup=main_menu()
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = query.from_user.id

    if user_id not in balances:
        balances[user_id] = 0

    # BACK
    if data == "back":
        await query.edit_message_text("🏠 Main Menu", reply_markup=main_menu())

    # SHOP
    elif data == "shop":
        await query.edit_message_text("🛒 Shop:", reply_markup=shop_menu())

    # BALANCE
    elif data == "balance":
        bal = get_balance(user_id)
        await query.edit_message_text(
            f"💳 Your Balance: ${bal}",
            reply_markup=main_menu()
        )

    # CATEGORIES
    elif data == "cat_watches":
        items = [(k, v) for k, v in products.items() if "rolex" in k or "ap_" in k]
        await query.edit_message_text("⌚ Watches:", reply_markup=category_menu(items))

    elif data == "cat_tours":
        items = [(k, v) for k, v in products.items() if "tour" in k]
        await query.edit_message_text("✈️ Tours:", reply_markup=category_menu(items))

    elif data == "cat_events":
        items = [(k, v) for k, v in products.items() if "vip_concert" in k or "formula1" in k]
        await query.edit_message_text("🎫 Events:", reply_markup=category_menu(items))

    elif data == "cat_services":
        items = [(k, v) for k, v in products.items() if "service" in k or "tool" in k]
        await query.edit_message_text("💻 Services:", reply_markup=category_menu(items))

    # BUY
    elif data.startswith("buy_"):
        item_id = data.replace("buy_", "")
        item = products[item_id]

        bal = get_balance(user_id)

        if bal < item["price"]:
            await query.edit_message_text(
                f"❌ Insufficient Balance\n\n"
                f"Product: {item['name']}\n"
                f"Price: ${item['price']}\n"
                f"Your Balance: ${bal}\n\n"
                f"Please deposit BTC.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💰 Deposit BTC", callback_data="deposit")],
                    [InlineKeyboardButton("🔙 Back", callback_data="shop")]
                ])
            )
            return

        balances[user_id] -= item["price"]

        await query.edit_message_text(
            f"✅ Purchase Successful!\n\n"
            f"You bought: {item['name']}\n"
            f"Remaining Balance: ${balances[user_id]}",
            reply_markup=main_menu()
        )

    # DEPOSIT
    elif data == "deposit":
        await query.edit_message_text(
            f"💰 Deposit BTC\n\nSend to:\n`{BTC_WALLET}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="back")]
            ])
        )

    # STATS
    elif data == "stats":
        await query.edit_message_text(
            f"📊 Users: {len(users)}",
            reply_markup=main_menu()
        )

    # RESTART
    elif data == "restart":
        await start(update, context)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu))

    app.run_polling()


if __name__ == "__main__":
    main()
