import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv
from aiogram.types import FSInputFile, Sticker
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Состояние для стикеров
class StickerIDState(StatesGroup):
    waiting_for_sticker = State()

load_dotenv()
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: Message):
    photo = FSInputFile("TsWTk0zhCt8 — .jpg")  # Проверь путь к файлу
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption=(
            "Привет! Этот бот предназначен для получения ID фото, стикеров и пользователей.\n\n"
            "📌 Список команд:\n"
            "🔹 /myID - получение своего ID\n"
            "🔹 /stickerID - получение ID стикера\n"
            "🔹 /photoID - получение ID фото\n"
            "🔹 /donate - донат создателю 😉"
        )
    )

@dp.message(Command("myID"))
async def get_userID(message: Message):
    user_id = message.from_user.id
    await message.answer(f"Твой ID: {user_id}")

@dp.message(Command("stickerID"))
async def request_sticker(message: Message, state: FSMContext):
    await state.set_state(StickerIDState.waiting_for_sticker)
    await message.answer("Отправь мне свой стикер")

@dp.message(F.sticker, StickerIDState.waiting_for_sticker)
async def get_sticker_ID(message: Message, state: FSMContext):
    sticker_id = message.sticker.file_id
    await message.answer(f"ID стикера: {sticker_id}")
    await state.clear()

@dp.message(Command("photoID"))
async def request_photo(message: Message):
    await message.answer("Отправь фото")

@dp.message(F.photo)
async def get_photo_ID(message: Message):
    file_id = message.photo[-1].file_id  # Берём фото лучшего качества
    await message.answer(f"ID фото: {file_id}")


@dp.message(Command("donate"))
async def donate(message:Message):
    await message.answer("Донат в криптовалюте TON (Мне это очень поможет):https://t.me/xrocket?start=inv_aAr3zB3VGW3rceZ ")

# Регистрируем обработчики
# dp.message.register(get_photo_ID, F.photo)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass