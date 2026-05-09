from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")
BTC_WALLET = "17hQJ4sGmt4yMniMfAfjEgRvAPPCnycfdc"

ADMIN_ID = 8721950488

users = set()
balances = {}

WELCOME_IMAGE = "https://i.imgur.com/yourimage.jpg"

# =========================
# PRODUCTS
# =========================
products = {
    # DIGITAL SERVICES
    "vip_service": {"name": "VIP Service", "price": 50},
    "premium_tool": {"name": "Premium Tool", "price": 100},

    # WATCHES
    "rolex_sub": {"name": "Rolex Submariner", "price": 12000},
    "ap_watch": {"name": "Audemars Piguet Royal Oak", "price": 25000},

    # TOURS
    "paris_tour": {"name": "Luxury Paris Tour", "price": 3000},
    "dubai_tour": {"name": "Dubai VIP Experience", "price": 5000},

    # EVENTS
    "vip_concert": {"name": "VIP Concert Access", "price": 1500},
    "formula1": {"name": "F1 VIP Event Ticket", "price": 8000},
}

# =========================
# HELPERS
# =========================
def is_admin(user_id: int):
    return user_id == ADMIN_ID


def get_balance(user_id: int):
    return balances.get(user_id, 0)

# =========================
# MAIN MENU (SERVICES)
# =========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💻 Services", callback_data="services")],
        [InlineKeyboardButton("💰 Deposit", callback_data="deposit")],
        [InlineKeyboardButton("💳 Balance", callback_data="balance")],
        [InlineKeyboardButton("🔐 Admin", callback_data="admin_panel")],
    ])


def services_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⌚ Watches", callback_data="cat_watches")],
        [InlineKeyboardButton("✈️ Tours", callback_data="cat_tours")],
        [InlineKeyboardButton("🎫 Events", callback_data="cat_events")],
        [InlineKeyboardButton("💻 Digital Services", callback_data="cat_services")],
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ])


def category_menu(items, back="services"):
    keyboard = []
    for k, v in items:
        keyboard.append([
            InlineKeyboardButton(
                f"{v['name']} - ${v['price']}",
                callback_data=f"buy_{k}"
            )
        ])

    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=back)])
    return InlineKeyboardMarkup(keyboard)

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)

    if user_id not in balances:
        balances[user_id] = 0

    await update.message.reply_photo(
        photo=WELCOME_IMAGE,
        caption=f"👑 Welcome to Luxury Services\n💳 Balance: ${balances[user_id]}",
        reply_markup=main_menu()
    )

# =========================
# ADMIN PANEL
# =========================
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

# =========================
# CALLBACK HANDLER
# =========================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if user_id not in balances:
        balances[user_id] = 0

    # BACK
    if data == "back":
        await query.edit_message_text("🏠 Main Menu", reply_markup=main_menu())

    # SERVICES
    elif data == "services":
        await query.edit_message_text("💻 Services:", reply_markup=services_menu())

    # BALANCE
    elif data == "balance":
        await query.edit_message_text(
            f"💳 Balance: ${balances[user_id]}",
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
        await query.edit_message_text("💻 Digital Services:", reply_markup=category_menu(items))

    # BUY
    elif data.startswith("buy_"):
        item = products[data.replace("buy_", "")]

        if balances[user_id] < item["price"]:
            await query.edit_message_text(
                f"❌ Insufficient Balance\n\n"
                f"{item['name']}\n"
                f"Price: ${item['price']}\n"
                f"Your Balance: ${balances[user_id]}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💰 Deposit", callback_data="deposit")],
                    [InlineKeyboardButton("🔙 Back", callback_data="services")]
                ])
            )
            return

        balances[user_id] -= item["price"]

        await query.edit_message_text(
            f"✅ Purchased: {item['name']}\n"
            f"Remaining: ${balances[user_id]}",
            reply_markup=main_menu()
        )

    # ADMIN
    elif data == "admin_panel":
        if not is_admin(user_id):
            await query.answer("No access ❌", show_alert=True)
            return
        await query.edit_message_text("🔐 Admin Panel opened via /admin")

    elif data == "admin_users":
        if not is_admin(user_id):
            return
        await query.edit_message_text(f"👥 Users: {len(users)}")

    elif data == "admin_stats":
        if not is_admin(user_id):
            return
        await query.edit_message_text(
            f"📊 Stats\nUsers: {len(users)}\nProducts: {len(products)}"
        )

# =========================
# MAIN
# =========================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CallbackQueryHandler(menu))

    app.run_polling()


if __name__ == "__main__":
    main()
