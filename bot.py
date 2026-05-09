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

BTC_ADDRESS = "bc1qxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
LTC_ADDRESS = "ltc1qxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

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
            [InlineKeyboardButton(text="💰 Payment Info", callback_data="payment")],
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
    photo = FSInputFile("welcome.jpg")

    text = """
🏆 <b>LUXCHAIN MARKETPLACE</b>

Premium anonymous luxury store:

⌚ Watches
🏠 Real Estate Tours
🛎 Concierge Services

Payments:
₿ Bitcoin (BTC)
Ł Litecoin (LTC)

Secure • Private • Global
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
            [InlineKeyboardButton(text="Rolex Daytona — 0.34 BTC", callback_data="rolex")],
            [InlineKeyboardButton(text="Patek Nautilus — 0.58 BTC", callback_data="patek")],
            [InlineKeyboardButton(text="Audemars Piguet — 0.41 BTC", callback_data="ap")],
            [InlineKeyboardButton(text="⬅ Back", callback_data="back")],
        ]
    )

    await callback.message.edit_text("⌚ <b>Luxury Watches</b>", parse_mode="HTML", reply_markup=kb)


@dp.callback_query(F.data == "rolex")
async def rolex(callback: CallbackQuery):
    await callback.message.edit_text(
        """
⌚ <b>Rolex Daytona</b>

Price: 0.34 BTC (~$36,000)
Condition: New
Escrow: Available
Shipping: Worldwide
""",
        parse_mode="HTML",
        reply_markup=buy_menu(),
    )


@dp.callback_query(F.data == "patek")
async def patek(callback: CallbackQuery):
    await callback.message.edit_text(
        """
⌚ <b>Patek Philippe Nautilus</b>

Price: 0.58 BTC (~$61,000)
Condition: Premium
Escrow: Available
Shipping: Worldwide
""",
        parse_mode="HTML",
        reply_markup=buy_menu(),
    )


@dp.callback_query(F.data == "ap")
async def ap(callback: CallbackQuery):
    await callback.message.edit_text(
        """
⌚ <b>Audemars Piguet Royal Oak</b>

Price: 0.41 BTC (~$43,000)
Condition: Mint
Escrow: Available
Shipping: Worldwide
""",
        parse_mode="HTML",
        reply_markup=buy_menu(),
    )


# ---------------- SERVICES ---------------- #

@dp.callback_query(F.data == "services")
async def services(callback: CallbackQuery):
    await callback.message.edit_text(
        """
🛎 <b>Luxury Services</b>

🚘 Chauffeur — 0.015 BTC/day  
🛥 Yacht Rental — 0.12 BTC/day  
✈ Private Jet — 0.45 BTC  
🛡 VIP Security — 0.025 BTC/day  
🏨 Concierge — 0.008 BTC
""",
        parse_mode="HTML",
        reply_markup=buy_menu(),
    )


# ---------------- REAL ESTATE ---------------- #

@dp.callback_query(F.data == "estate")
async def estate(callback: CallbackQuery):
    await callback.message.edit_text(
        """
🏠 <b>Real Estate Tours</b>

🇦🇪 Dubai Penthouse — 0.06 BTC  
🇲🇨 Monaco Villa — 0.11 BTC  
🏝 Private Island — 0.25 BTC  
🇬🇧 London Apartment — 0.04 BTC

Private guided tours available.
""",
        parse_mode="HTML",
        reply_markup=buy_menu(),
    )


# ---------------- CART ---------------- #

@dp.callback_query(F.data == "cart")
async def cart(callback: CallbackQuery):
    await callback.message.edit_text(
        """
🛒 <b>Your Cart</b>

• Rolex Daytona — 0.34 BTC

Total: 0.34 BTC
""",
        parse_mode="HTML",
        reply_markup=buy_menu(),
    )


# ---------------- PAYMENT ---------------- #

@dp.callback_query(F.data == "payment")
async def payment(callback: CallbackQuery):
    await callback.message.edit_text(
        f"""
💰 <b>Crypto Payment</b>

Send payment to:

₿ BTC:
<code>{BTC_ADDRESS}</code>

Ł LTC:
<code>{LTC_ADDRESS}</code>

After payment click “Buy Now”.
""",
        parse_mode="HTML",
        reply_markup=buy_menu(),
    )


# ---------------- ACTIONS ---------------- #

@dp.callback_query(F.data == "addcart")
async def addcart(callback: CallbackQuery):
    await callback.answer("Added to cart 🛒")


@dp.callback_query(F.data == "buy")
async def buy(callback: CallbackQuery):
    await callback.message.edit_text(
        f"""
⚠ <b>Payment Required</b>

Send BTC or LTC to complete order.

₿ BTC:
<code>{BTC_ADDRESS}</code>

Ł LTC:
<code>{LTC_ADDRESS}</code>

Status: Awaiting payment confirmation
""",
        parse_mode="HTML",
        reply_markup=main_menu(),
    )


@dp.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    await callback.message.edit_text(
        "🏆 <b>LUXCHAIN MARKETPLACE</b>",
        parse_mode="HTML",
        reply_markup=main_menu(),
    )


# ---------------- RUN ---------------- #

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
