from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 8721950488

users = set()
balances = {}

BTC_WALLET = "17hQJ4sGmt4yMniMfAfjEgRvAPPCnycfdc"


# =========================
# PRODUCTS (ADD YOUR OWN HERE)
# =========================
products = {
    # WATCHES
    "rolex": {"name": "Rolex Submariner", "price": 12000},
    "ap": {"name": "Audemars Piguet Royal Oak", "price": 25000},

    # TOURS
    "paris": {"name": "Paris Luxury Tour", "price": 3000},
    "dubai": {"name": "Dubai VIP Tour", "price": 5000},

    # EVENTS
    "concert": {"name": "VIP Concert Ticket", "price": 1500},
    "f1": {"name": "Formula 1 VIP Ticket", "price": 8000},

    # SERVICES
    "vip": {"name": "VIP Digital Service", "price": 50},
    "tool": {"name": "Premium Tool Access", "price": 100},
}


# =========================
# MENUS
# =========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Shop", callback_data="shop")],
        [InlineKeyboardButton("💰 Deposit", callback_data="deposit")],
        [InlineKeyboardButton("💳 Balance", callback_data="balance")],
        [InlineKeyboardButton("🔐 Admin", callback_data="admin")]
    ])


def shop_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⌚ Watches", callback_data="watches")],
        [InlineKeyboardButton("✈️ Tours", callback_data="tours")],
        [InlineKeyboardButton("🎫 Events", callback_data="events")],
        [InlineKeyboardButton("💻 Services", callback_data="services")],
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ])


def product_menu(keys, back="shop"):
    keyboard = []
    for k in keys:
        p = products[k]
        keyboard.append([
            InlineKeyboardButton(
                f"{p['name']} - ${p['price']}",
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

    await update.message.reply_text(
        f"👑 Welcome to luxchainbot!\n Luxury anonymous service 🕶️💎 offering exclusive watches ⌚, VIP tours 🏝️, private events 🎟️, and international virtual numbers 📱🌍 — secure, discreet, and globally accessible anytime 🚀\n💳 Balance: ${balances[user_id]}",
        reply_markup=main_menu()
    )


# =========================
# CALLBACK (SIMPLE ROUTER)
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

    # SHOP
    elif data == "shop":
        await query.edit_message_text("🛒 Shop", reply_markup=shop_menu())

    # BALANCE
    elif data == "balance":
        await query.edit_message_text(
            f"💳 Balance: ${balances[user_id]}",
            reply_markup=main_menu()
        )

    # DEPOSIT
    elif data == "deposit":
        await query.edit_message_text(
            f"💰 Send BTC here:\n\n`{BTC_WALLET}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="back")]
            ])
        )

    # CATEGORIES
    elif data == "watches":
        keys = ["rolex", "ap"]
        await query.edit_message_text("⌚ Watches", reply_markup=product_menu(keys))

    elif data == "tours":
        keys = ["paris", "dubai"]
        await query.edit_message_text("✈️ Tours", reply_markup=product_menu(keys))

    elif data == "events":
        keys = ["concert", "f1"]
        await query.edit_message_text("🎫 Events", reply_markup=product_menu(keys))

    elif data == "services":
        keys = ["vip", "tool"]
        await query.edit_message_text("💻 Services", reply_markup=product_menu(keys))

    # BUY
    elif data.startswith("buy_"):
        key = data.replace("buy_", "")
        item = products[key]

        if balances[user_id] < item["price"]:
            await query.edit_message_text(
                f"❌ Not enough balance\n\n"
                f"{item['name']}\nPrice: ${item['price']}\n"
                f"Balance: ${balances[user_id]}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💰 Deposit", callback_data="deposit")],
                    [InlineKeyboardButton("🔙 Back", callback_data="shop")]
                ])
            )
            return

        balances[user_id] -= item["price"]

        await query.edit_message_text(
            f"✅ Bought: {item['name']}\n"
            f"Remaining: ${balances[user_id]}",
            reply_markup=main_menu()
        )

    # ADMIN
    elif data == "admin":
        if user_id != ADMIN_ID:
            await query.answer("No access ❌", show_alert=True)
            return

        await query.edit_message_text(
            f"🔐 Admin Panel\nUsers: {len(users)}\nProducts: {len(products)}",
            reply_markup=main_menu()
        )


# =========================
# MAIN
# =========================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu))

    app.run_polling()


if __name__ == "__main__":
    main()
