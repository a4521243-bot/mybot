from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "YOUR_BOT_TOKEN"
BTC_WALLET = "17hQJ4sGmt4yMniMfAfjEgRvAPPCnycfdc"

ADMIN_ID = 8721950488  # ჩასვი შენი Telegram ID

users = set()

WELCOME_IMAGE = "https://i.imgur.com/yourimage.jpg"

# PRODUCTS
products = {
    # SERVICES
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

# CHECK ADMIN
def is_admin(user_id: int):
    return user_id == ADMIN_ID


# MAIN MENU
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Shop", callback_data="shop")],
        [InlineKeyboardButton("💰 Deposit", callback_data="deposit")],
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
        [InlineKeyboardButton("🔄 Restart", callback_data="restart")],
    ])


def shop_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⌚ Watches", callback_data="cat_watches")],
        [InlineKeyboardButton("✈️ Tours", callback_data="cat_tours")],
        [InlineKeyboardButton("🎫 Events", callback_data="cat_events")],
        [InlineKeyboardButton("💻 Digital Services", callback_data="cat_services")],
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


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)

    await update.message.reply_photo(
        photo=WELCOME_IMAGE,
        caption="👑 Welcome to Luxury Store Bot\n\nExplore premium products below.",
        reply_markup=main_menu()
    )


# ADMIN PANEL
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text("❌ Access denied")
        return

    keyboard = [
        [InlineKeyboardButton("👥 Users Count", callback_data="admin_users")],
        [InlineKeyboardButton("📊 Full Stats", callback_data="admin_stats")],
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ]

    await update.message.reply_text(
        "🔐 Admin Panel",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# CALLBACK HANDLER
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    # BACK
    if data == "back":
        await query.edit_message_text("🏠 Main Menu:", reply_markup=main_menu())

    # SHOP
    elif data == "shop":
        await query.edit_message_text("🛒 Select category:", reply_markup=shop_menu())

    # CATEGORIES
    elif data == "cat_watches":
        items = [(k, v) for k, v in products.items() if "rolex" in k or "ap_" in k]
        await query.edit_message_text("⌚ Watches:", reply_markup=category_menu(items))

    elif data == "cat_tours":
        items = [(k, v) for k, v in products.items() if "tour" in k]
        await query.edit_message_text("✈️ Tours:", reply_markup=category_menu(items))

    elif data == "cat_events":
        items = [(k, v) for k, v in products.items() if "vip_concert" in k or "formula1" in k or "event" in k]
        await query.edit_message_text("🎫 Events:", reply_markup=category_menu(items))

    elif data == "cat_services":
        items = [(k, v) for k, v in products.items() if "service" in k or "tool" in k]
        await query.edit_message_text("💻 Services:", reply_markup=category_menu(items))

    # BUY
    elif data.startswith("buy_"):
        item_id = data.replace("buy_", "")
        item = products[item_id]

        await query.edit_message_text(
            f"❌ Insufficient Balance\n\n"
            f"Product: {item['name']}\n"
            f"Price: ${item['price']}\n\n"
            f"Please deposit Bitcoin.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 Deposit BTC", callback_data="deposit")],
                [InlineKeyboardButton("🔙 Back", callback_data="shop")]
            ])
        )

    # DEPOSIT
    elif data == "deposit":
        await query.edit_message_text(
            f"💰 Bitcoin Deposit\n\n"
            f"Send BTC to:\n\n`{BTC_WALLET}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Copy Address", callback_data="copy_btc")],
                [InlineKeyboardButton("🔙 Back", callback_data="back")]
            ])
        )

    # COPY BTC
    elif data == "copy_btc":
        await query.answer("BTC address copied ✅", show_alert=True)

    # STATS (public)
    elif data == "stats":
        await query.edit_message_text(
            f"📊 Users: {len(users)}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="back")]
            ])
        )

    # RESTART
    elif data == "restart":
        await query.edit_message_text("🔄 Restarting bot...")
        await start(update, context)

    # ADMIN USERS
    elif data == "admin_users":
        if not is_admin(user_id):
            await query.answer("No access ❌", show_alert=True)
            return

        await query.edit_message_text(
            f"👥 Total Users: {len(users)}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="back")]
            ])
        )

    # ADMIN STATS
    elif data == "admin_stats":
        if not is_admin(user_id):
            await query.answer("No access ❌", show_alert=True)
            return

        await query.edit_message_text(
            f"📊 Bot Statistics\n\n"
            f"👥 Users: {len(users)}\n"
            f"🛒 Products: {len(products)}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="back")]
            ])
        )


# MAIN
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CallbackQueryHandler(menu))

    app.run_polling()


if __name__ == "__main__":
    main()
