from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8721950488

users = set()
balances = {}

BTC_WALLET = "17hQJ4sGmt4yMniMfAfjEgRvAPPCnycfdc"


# =========================
# PRODUCTS (UPDATED LUXURY TOURS & EVENTS)
# =========================
products = {
    # WATCHES
    "rolex": {"name": "Rolex Submariner", "price": 10000},
    "ap": {"name": "Audemars Piguet Royal Oak", "price": 25000},

    # TOURS
    "safari": {
        "name": "🛩️ African Safari Luxury Tour",
        "price": 15000,
        "description": "🌍 Location: Kenya & Tanzania\n⏳ Duration: 7–10 days\n💰 Price: $8,000–$20,000 per person"
    },
    "italy": {
        "name": "🍷 Italian Culinary & Wine Tour",
        "price": 11000,
        "description": "🌍 Location: Tuscany, Piedmont, Amalfi Coast\n⏳ Duration: 7–12 days\n💰 Price: $7,000–$15,000 per person"
    },
    "med_yacht": {
        "name": "⛵ Mediterranean Yacht Cruise",
        "price": 60000,
        "description": "🌍 Location: French Riviera, Italy, Greek Islands\n⏳ Duration: 5–14 days\n💰 Price: $20,000–$100,000+ per week"
    },
    "japan": {
        "name": "🎎 Japanese Cultural & Luxury Tour",
        "price": 15000,
        "description": "🌍 Location: Tokyo, Kyoto, Osaka, Hokkaido\n⏳ Duration: 10–14 days\n💰 Price: $10,000–$25,000 per person"
    },
    "antarctic": {
        "name": "🏔️ Antarctic Luxury Expedition",
        "price": 32500,
        "description": "🌍 Location: Antarctic Peninsula\n⏳ Duration: 10–20 days\n💰 Price: $15,000–$50,000+ per person"
    },

    # EVENTS
    "cannes": {
        "name": "🎬 Cannes Film Festival VIP",
        "price": 30000,
        "description": "🌍 Location: Cannes, France\n⏳ Duration: May 14–25, 2026\n💰 Price: $10,000–$50,000+ VIP packages"
    },
    "monaco_f1": {
        "name": "🏎️ Monaco Grand Prix F1 VIP",
        "price": 15000,
        "description": "🌍 Location: Monte Carlo, Monaco\n⏳ Duration: May 22–25, 2026\n💰 Price: $5,000–$20,000+ VIP packages"
    },

    # SERVICES
    "vip": {"name": "Unlimited Voip Calling", "price": 500},
    "tool": {"name": "Unlimited Voip Message", "price": 300},
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
        # Show description if available
        text = f"{p['name']} - ${p['price']}"
        if "description" in p:
            text += f"\n{p['description']}"
        keyboard.append([InlineKeyboardButton(text, callback_data=f"buy_{k}")])
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
        f"👑 Welcome to LuxChainBot\n 🫶 For assistance: @luxchainsupport\n 💳 Balance: ${balances[user_id]}",
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
        keys = ["safari", "italy", "med_yacht", "japan", "antarctic"]
        await query.edit_message_text("✈️ Tours", reply_markup=product_menu(keys))

    elif data == "events":
        keys = ["cannes", "monaco_f1"]
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
