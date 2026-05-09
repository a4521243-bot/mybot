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

ADMIN_ID = 123456789  # <-- PUT YOUR TELEGRAM ID HERE

BTC_ADDRESS = "bc1qxxxxxxxxxxxxxxxxxxxx"
LTC_ADDRESS = "ltc1qxxxxxxxxxxxxxxxxxxxx"

users = set()

bot = Bot(TOKEN)
dp = Dispatcher()


# ---------------- MENUS ---------------- #

def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⌚ Watches", callback_data="watches")],
            [InlineKeyboardButton(text="🏠 Real Estate", callback_data="estate")],
            [InlineKeyboardButton(text="🛎 Services", callback_data="services")],
            [InlineKeyboardButton(text="🛒 Cart", callback_data="cart")],
            [InlineKeyboardButton(text="💰 Payment", callback_data="payment")],
            [InlineKeyboardButton(text="🔐 Admin Panel", callback_data="admin")],
        ]
    )


def buy_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Add to Cart", callback_data="addcart")],
            [InlineKeyboardButton(text="💳 Buy Now", callback_data="buy")],
            [InlineKeyboardButton(text="⬅ Back", callback_data="back")],
        ]
    )


# ---------------- START ---------------- #

@dp.message(CommandStart())
async def start(message: Message):
    users.add(message.from_user.id)

    photo = FSInputFile("welcome.jpg")

    text = """
🏆 <b>LUXCHAIN MARKETPLACE</b>

Premium anonymous luxury store:

⌚ Watches
🏠 Real Estate
🛎 Services

₿ BTC / Ł LTC Accepted
"""

    await message.answer_photo(
        photo=photo,
        caption=text,
        parse_mode="HTML",
        reply_markup=main_menu(),
    )


# ---------------- WATCHES ---------------- #

@dp.callback_query(F.data == "watches")
async def watches(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Rolex Daytona — 0.34 BTC", callback_data="rolex")],
            [InlineKeyboardButton("Patek Nautilus — 0.58 BTC", callback_data="patek")],
            [InlineKeyboardButton("Audemars Piguet — 0.41 BTC", callback_data="ap")],
            [InlineKeyboardButton("⬅ Back", callback_data="back")],
        ]
    )

    await callback.message.edit_text("⌚ <b>Luxury Watches</b>", parse_mode="HTML", reply_markup=kb)


@dp.callback_query(F.data == "rolex")
async def rolex(callback: CallbackQuery):
    await callback.message.edit_text(
        "⌚ Rolex Daytona\nPrice: 0.34 BTC (~$36,000)",
        reply_markup=buy_menu()
    )


@dp.callback_query(F.data == "patek")
async def patek(callback: CallbackQuery):
    await callback.message.edit_text(
        "⌚ Patek Philippe Nautilus\nPrice: 0.58 BTC (~$61,000)",
        reply_markup=buy_menu()
    )


@dp.callback_query(F.data == "ap")
async def ap(callback: CallbackQuery):
    await callback.message.edit_text(
        "⌚ Audemars Piguet Royal Oak\nPrice: 0.41 BTC (~$43,000)",
        reply_markup=buy_menu()
    )


# ---------------- SERVICES ---------------- #

@dp.callback_query(F.data == "services")
async def services(callback: CallbackQuery):
    await callback.message.edit_text(
        """
🛎 Services:

🚘 Chauffeur — 0.015 BTC/day  
🛥 Yacht — 0.12 BTC/day  
✈ Jet — 0.45 BTC  
🛡 Security — 0.025 BTC/day
""",
        reply_markup=buy_menu()
    )


# ---------------- ESTATE ---------------- #

@dp.callback_query(F.data == "estate")
async def estate(callback: CallbackQuery):
    await callback.message.edit_text(
        """
🏠 Real Estate Tours:

Dubai — 0.06 BTC  
Monaco — 0.11 BTC  
Island — 0.25 BTC  
London — 0.04 BTC
""",
        reply_markup=buy_menu()
    )


# ---------------- CART ---------------- #

@dp.callback_query(F.data == "cart")
async def cart(callback: CallbackQuery):
    await callback.message.edit_text(
        "🛒 Cart:\n\n• Rolex Daytona — 0.34 BTC\nTotal: 0.34 BTC",
        reply_markup=buy_menu()
    )


# ---------------- PAYMENT ---------------- #

@dp.callback_query(F.data == "payment")
async def payment(callback: CallbackQuery):
    await callback.message.edit_text(
        f"""
💰 Payment:

BTC:
<code>{BTC_ADDRESS}</code>

LTC:
<code>{LTC_ADDRESS}</code>

Send payment and click Buy Now.
""",
        parse_mode="HTML",
        reply_markup=buy_menu()
    )


# ---------------- ACTIONS ---------------- #

@dp.callback_query(F.data == "addcart")
async def addcart(callback: CallbackQuery):
    await callback.answer("Added to cart 🛒")


@dp.callback_query(F.data == "buy")
async def buy(callback: CallbackQuery):
    await callback.message.edit_text(
        f"""
⚠ Payment Required

Send BTC/LTC:

BTC:
<code>{BTC_ADDRESS}</code>

LTC:
<code>{LTC_ADDRESS}</code>

Waiting for confirmation...
""",
        parse_mode="HTML",
        reply_markup=main_menu()
    )


# ---------------- ADMIN PANEL ---------------- #

@dp.callback_query(F.data == "admin")
async def admin(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Access denied ❌", show_alert=True)
        return

    text = f"""
🔐 ADMIN PANEL

👥 Users: {len(users)}
📊 Bot status: Online
⚙ Platform: Railway

No database mode (temporary stats)
"""

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("🔄 Refresh", callback_data="admin")],
            [InlineKeyboardButton("⬅ Back", callback_data="back")]
        ]
    )

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb)


# ---------------- BACK ---------------- #

@dp.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    await callback.message.edit_text(
        "🏆 LUXCHAIN MARKETPLACE",
        reply_markup=main_menu()
    )


# ---------------- RUN ---------------- #

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
