
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

TOKEN = "8238058601:AAH1F6UgQPUTTJH6pDSUy0n6oNbi64Kt7uQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧠 Креативный", callback_data="creative"),
         InlineKeyboardButton(text="💼 Деловой", callback_data="business")],
        [InlineKeyboardButton(text="🎮 Игровой", callback_data="game")]
    ])
    await message.answer("Выбери стиль общения:", reply_markup=keyboard)

# Обработка нажатий
@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    data = callback.data

    if data == "creative":
        await callback.message.answer("🧠 Ты выбрал *Креативный* стиль!", parse_mode="Markdown")
    elif data == "business":
        await callback.message.answer("💼 Ты выбрал *Деловой* стиль!", parse_mode="Markdown")
    elif data == "game":
        await callback.message.answer("🎮 Ты выбрал *Игровой* стиль!", parse_mode="Markdown")

    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())