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
# ALLPRODUCTS
    "vip": {
        "name": "☎️Unlimited Voip Calling/Monthly",
        "price": 500,
        "description":"Available: 🇺🇸🇨🇦🇩🇪\n🏢Federal Numbers: ✅"
    },
    "tool": {
        "name": "📨Unlimited Voip Message/Monthly",
        "price": 300, 
        "description":"Available: 🇺🇸🇨🇦🇩🇪\n🏢Federal Numbers: ✅"
    },
    "olst": {
        "name": "👤High income contacts",
        "price":500,
        "description":"From: 🇺🇸🇨🇦\n📱Quanity numbers: 50K✅"
    },
    "tlst": {
        "name": "👤High income contacts",
        "price":1000,
        "description":"From: 🇺🇸🇨🇦\n📱Quanity numbers: 100K✅"
    },
    "crc": {
        "name": "💳Usable credit cards",
        "price":1000,
        "description":"🌍From: 🇩🇪\n🟥Limit: 4000💶"
    },
    "trc": {
        "name": "💳Usable credit cards",
        "price":500,
        "description":"🌍From: 🇩🇪\n🟥Limit: 2000💶"
    },
}


# =========================
# MENUS
# =========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Shop", callback_data="shop")],
        [InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("🔐 Admin", callback_data="admin")]
    ])


def shop_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("☎️ VOIP SERVICES", callback_data="voip")],
        [InlineKeyboardButton("👤 CRYPTO LEADS", callback_data="leads")],
        [InlineKeyboardButton("💳 CREDIT CARDS", callback_data="cards")],
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
        f"""
✨ <b>Welcome to LuxChainBot VIP Services!</b> ✨

Step into a world of premium digital services:

📞 <b>VOIP Services</b> — Virtual numbers for CALL & SMS
💳 <b>Credit Cards</b> — Premium cards with overdraft limits
👤 <b>Exclusive Leads</b> — Targeted high-value crypto contacts
🔒 <b>Secure Transactions</b> — Safety you can trust

For personalized support, reach out: 📞 <b>@luxchainsupport</b>
    🚀 Select an option below to continue.
    """,
        parse_mode="HTML",
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
        await query.edit_message_text(
    """
     🏠 <b>Main Menu</b> 🏠
     
📞 <b>VOIP Services</b> — Virtual numbers for CALL & SMS
💳 <b>Credit Cards</b> — Premium cards with overdraft limits
👤 <b>Exclusive Leads</b> — Targeted high-value crypto contacts
🔒 <b>Secure Transactions</b> — Safety you can trust 

For personalized support, reach out: 📞 <b>@luxchainsupport</b>
    🚀 Select an option below to continue.
""",
    parse_mode="HTML",
    reply_markup=main_menu()
)

    # SHOP
    elif data == "shop":
        await query.edit_message_text(
    """
    🛒 <b>Shop Menu</b> 🛒
    
🫶 Support: @luxchainsupport

Choose a category below 👇
""",
    parse_mode="HTML",
    reply_markup=shop_menu()
)

    # BALANCE
    elif data == "balance":
        await query.edit_message_text(
            f"💰 Balance: ${balances[user_id]}",
            reply_markup=main_menu()
        )

    # DEPOSIT
    elif data == "deposit":
        await query.edit_message_text(
    f"""
❌ <b>Insufficient Balance</b>

💰 <b>Top Up Required</b>

Send BTC to the address below to continue:

<code>{BTC_WALLET}</code>

⚡ After payment, balance updates automatically
🔒 Secure blockchain transaction

""",
    parse_mode="HTML",
    reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ])
)

    # CATEGORIES
    elif data == "leads":
        keys = ["olst", "tlst"]
        await query.edit_message_text(
    """
👤 <b>Crypto Leads</b> 👤

🫶 Support: @luxchainsupport

Choose your watch below 👇
""",
    parse_mode="HTML",
    reply_markup=product_menu(keys)
)

    elif data == "cards":
        keys = ["crc", "trc"]
        await query.edit_message_text(
    """
💳 <b>Credit Cards</b> 💳

🫶 Support: @luxchainsupport

Choose your tour below 👇
""",
    parse_mode="HTML",
    reply_markup=product_menu(keys)
)

    elif data == "events":
        keys = ["cannes", "monaco_f1"]
        await query.edit_message_text(
    """
🎫 <b>Exclusive Events</b> 🎫

🫶 Support: @luxchainsupport

Choose your event below 👇
""",
    parse_mode="HTML",
    reply_markup=product_menu(keys)
)

    elif data == "voip":
        keys = ["vip", "tool"]
        await query.edit_message_text(
    """
💻 <b>Elite Services</b> 💻

🫶 Support: @luxchainsupport

Choose a service below 👇
""",
    parse_mode="HTML",
    reply_markup=product_menu(keys)
)

    # BUY
    elif data.startswith("buy_"):
        key = data.replace("buy_", "")
        item = products[key]

        if balances[user_id] < item["price"]:
            await query.edit_message_text(
                f"{item['name']}\n"
                f"{item['description']}\n"
                f"💵Price : {item['price']}$\n"
                f"💰Balance : {balances[user_id]}$",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ Order Now", callback_data="deposit")],
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
