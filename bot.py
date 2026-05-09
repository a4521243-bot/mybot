from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# =====================
# CONFIG
# =====================
TOKEN = os.getenv("BOT_TOKEN")  # Railway / GitHub ENV
BTC_WALLET = "17hQJ4sGmt4yMniMfAfjEgRvAPPCnycfdc"
ADMIN_ID = 8721950488

# =====================
# MEMORY STORAGE
# =====================
users = set()
balances = {}

WELCOME_IMAGE = "https://i.imgur.com/yourimage.jpg"

# =====================
# PRODUCTS
# =====================
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

# =====================
# HELPERS
# =====================
def is_admin(user_id: int):
    return user_id == ADMIN_ID


def get_balance(user_id: int):
    return balances.get(user_id, 0)


# =====================
# KEYBOARDS
# =====================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Shop", callback_data="shop")],
        [InlineKeyboardButton("💰 Deposit", callback_data="deposit")],
        [InlineKeyboardButton("💳 Balance", callback_data="balance")],
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
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


def category_menu(items, back="shop"):
    keyboard = []
    for key, item in items:
        keyboard.append([
            InlineKeyboardButton(
                f"{item['name']} - ${item['price']}",
                callback_data=f"buy_{key}"
            )
        ])
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=back)])
    return InlineKeyboardMarkup(keyboard)


# =====================
# START
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)

    if user_id not in balances:
        balances[user_id] = 0

    await update.message.reply_photo(
        photo=WELCOME_IMAGE,
        caption=f"👑 Welcome to Luxury Store Bot\n\n💳 Balance: ${balances[user_id]}",
        reply_markup=main_menu()
    )


# =====================
# ADMIN
# =====================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text("❌ Access denied")
        return

    keyboard = [
        [InlineKeyboardButton("👥 Users", callback_data="admin_users")],
        [InlineKeyboardButton("📊 Stats", callback_data="admin_stats")],
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ]

    await update.message.reply_text(
        "🔐 Admin Panel",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =====================
# CALLBACK ROUTER (FIXED CORE)
# =====================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not query:
        return

    await query.answer()

    data = query.data
    user_id = query.from_user.id

    if user_id not in balances:
        balances[user_id] = 0

    try:
        # BACK
        if data == "back":
            await query.edit_message_text("🏠 Main Menu", reply_markup=main_menu())

        # SHOP
        elif data == "shop":
            await query.edit_message_text("🛒 Shop", reply_markup=shop_menu())

        # BALANCE
        elif data == "balance":
            await query.edit_message_text(
                f"💳 Your Balance: ${balances[user_id]}",
                reply_markup=main_menu()
            )

        # DEPOSIT
        elif data == "deposit":
            await query.edit_message_text(
                f"💰 Send BTC:\n\n`{BTC_WALLET}`",
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

        # CATEGORIES
        elif data == "cat_watches":
            items = [(k, v) for k, v in products.items() if "rolex" in k or "ap_" in k]
            await query.edit_message_text("⌚ Watches", reply_markup=category_menu(items))

        elif data == "cat_tours":
            items = [(k, v) for k, v in products.items() if "tour" in k]
            await query.edit_message_text("✈️ Tours", reply_markup=category_menu(items))

        elif data == "cat_events":
            items = [(k, v) for k, v in products.items() if "vip_concert" in k or "formula1" in k]
            await query.edit_message_text("🎫 Events", reply_markup=category_menu(items))

        elif data == "cat_services":
            items = [(k, v) for k, v in products.items() if "service" in k or "tool" in k]
            await query.edit_message_text("💻 Services", reply_markup=category_menu(items))

        # BUY
        elif data.startswith("buy_"):
            item_id = data.replace("buy_", "")
            item = products[item_id]

            if balances[user_id] < item["price"]:
                await query.edit_message_text(
                    f"❌ Insufficient Balance\n\n"
                    f"{item['name']}\n"
                    f"Price: ${item['price']}\n"
                    f"Your Balance: ${balances[user_id]}",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("💰 Deposit", callback_data="deposit")],
                        [InlineKeyboardButton("🔙 Back", callback_data="shop")]
                    ])
                )
                return

            balances[user_id] -= item["price"]

            await query.edit_message_text(
                f"✅ Purchased: {item['name']}\n"
                f"Remaining Balance: ${balances[user_id]}",
                reply_markup=main_menu()
            )

        # ADMIN USERS
        elif data == "admin_users":
            if not is_admin(user_id):
                await query.answer("No access ❌", show_alert=True)
                return

            await query.edit_message_text(f"👥 Users: {len(users)}")

        # ADMIN STATS
        elif data == "admin_stats":
            if not is_admin(user_id):
                await query.answer("No access ❌", show_alert=True)
                return

            await query.edit_message_text(
                f"📊 Stats\nUsers: {len(users)}\nProducts: {len(products)}"
            )

    except Exception as e:
        await query.edit_message_text(f"⚠️ Error:\n{str(e)}")


# =====================
# MAIN
# =====================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CallbackQueryHandler(menu))

    app.run_polling()


if __name__ == "__main__":
    main()
