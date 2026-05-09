import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile,
)

TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 8721950488

BTC_ADDRESS = "17hQJ4sGmt4yMniMfAfjEgRvAPPCnycfdc"

bot = Bot(TOKEN)
dp = Dispatcher()

# ---------------- MEMORY ---------------- #

users = set()

products = {
    "rolex": {"name": "Rolex Daytona", "price": 0.34},
    "patek": {"name": "Patek Nautilus", "price": 0.58},
    "ap": {"name": "Audemars Piguet", "price": 0.41},
}

admin_state = {}

# ---------------- MENUS ---------------- #

def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("⌚ Watches", callback_data="watches")],
            [InlineKeyboardButton("🛎 Services", callback_data="services")],
            [InlineKeyboardButton("🏠 Estate", callback_data="estate")],
            [InlineKeyboardButton("🛒 Cart", callback_data="cart")],
            [InlineKeyboardButton("💰 BTC Payment", callback_data="payment")],
            [InlineKeyboardButton("🔐 Admin", callback_data="admin")],
        ]
    )


def admin_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("➕ Add Product", callback_data="add_product")],
            [InlineKeyboardButton("📦 List Products", callback_data="list_products")],
            [InlineKeyboardButton("⬅ Back", callback_data="back")],
        ]
    )


def buy_menu(pid):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("💳 Buy", callback_data=f"buy_{pid}")],
            [InlineKeyboardButton("⬅ Back", callback_data="watches")],
        ]
    )


# ---------------- START ---------------- #

@dp.message(CommandStart())
async def start(message: Message):
    users.add(message.from_user.id)

    photo = FSInputFile("welcome.jpg")

    await message.answer_photo(
        photo=photo,
        caption="🏆 LUXCHAIN MARKETPLACE",
        reply_markup=main_menu(),
    )


# ---------------- WATCHES ---------------- #

@dp.callback_query(F.data == "watches")
async def watches(c: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(f"{p['name']} — {p['price']} BTC", callback_data=f"p_{k}")]
            for k, p in products.items()
        ] + [[InlineKeyboardButton("⬅ Back", callback_data="back")]]
    )

    await c.message.edit_text("⌚ Watches", reply_markup=kb)


@dp.callback_query(F.data.startswith("p_"))
async def product_page(c: CallbackQuery):
    pid = c.data.split("_")[1]
    p = products[pid]

    await c.message.edit_text(
        f"""
⌚ {p['name']}

Price: {p['price']} BTC
""",
        reply_markup=buy_menu(pid),
    )


# ---------------- BUY ---------------- #

@dp.callback_query(F.data.startswith("buy_"))
async def buy(c: CallbackQuery):
    pid = c.data.split("_")[1]
    p = products[pid]

    await c.message.edit_text(
        f"""
⚠ PAYMENT REQUIRED

Product: {p['name']}
Price: {p['price']} BTC

Send BTC to:

{BTC_ADDRESS}

After payment, your order will be processed.
"""
    )


# ---------------- SERVICES ---------------- #

@dp.callback_query(F.data == "services")
async def services(c: CallbackQuery):
    await c.message.edit_text(
        "🛎 VIP Services\nChauffeur / Yacht / Jet",
        reply_markup=main_menu()
    )


# ---------------- ESTATE ---------------- #

@dp.callback_query(F.data == "estate")
async def estate(c: CallbackQuery):
    await c.message.edit_text(
        "🏠 Real Estate Tours\nDubai / Monaco / London",
        reply_markup=main_menu()
    )


# ---------------- CART ---------------- #

@dp.callback_query(F.data == "cart")
async def cart(c: CallbackQuery):
    await c.message.edit_text("🛒 Cart empty (demo)", reply_markup=main_menu())


# ---------------- BTC PAYMENT ---------------- #

@dp.callback_query(F.data == "payment")
async def payment(c: CallbackQuery):
    await c.message.edit_text(
        f"""
💰 BTC PAYMENT ONLY

Send Bitcoin to:

{BTC_ADDRESS}
""",
        reply_markup=main_menu()
    )


# ---------------- ADMIN PANEL ---------------- #

@dp.callback_query(F.data == "admin")
async def admin(c: CallbackQuery):
    if c.from_user.id != ADMIN_ID:
        await c.answer("Access denied ❌", show_alert=True)
        return

    await c.message.edit_text(
        f"""
🔐 ADMIN PANEL

👥 Users: {len(users)}
📦 Products: {len(products)}
💰 BTC Only Mode
""",
        reply_markup=admin_menu()
    )


# ---------------- ADD PRODUCT ---------------- #

@dp.callback_query(F.data == "add_product")
async def add_product(c: CallbackQuery):
    if c.from_user.id != ADMIN_ID:
        return

    admin_state[c.from_user.id] = {"step": "name"}
    await c.message.answer("Send product name:")


@dp.message()
async def admin_flow(message: Message):
    uid = message.from_user.id

    if uid not in admin_state:
        return

    state = admin_state[uid]

    if state["step"] == "name":
        state["name"] = message.text
        state["step"] = "price"
        await message.answer("Send price in BTC:")
        return

    if state["step"] == "price":
        try:
            price = float(message.text)
        except:
            await message.answer("Invalid price")
            return

        pid = f"prod{len(products)+1}"

        products[pid] = {
            "name": state["name"],
            "price": price
        }

        del admin_state[uid]

        await message.answer("Product added successfully ✅")


# ---------------- LIST PRODUCTS ---------------- #

@dp.callback_query(F.data == "list_products")
async def list_products(c: CallbackQuery):
    if c.from_user.id != ADMIN_ID:
        return

    text = "📦 PRODUCTS:\n\n"

    for p in products.values():
        text += f"{p['name']} — {p['price']} BTC\n"

    await c.message.edit_text(text, reply_markup=admin_menu())


# ---------------- BACK ---------------- #

@dp.callback_query(F.data == "back")
async def back(c: CallbackQuery):
    await c.message.edit_text("🏆 MAIN MENU", reply_markup=main_menu())


# ---------------- RUN ---------------- #

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
