from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from GiveReceptService import give_recipe
import random
import string
from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_recipe = KeyboardButton('Найти рецепт')
main_keyboard.add(button_recipe)

inline_keyboard = InlineKeyboardMarkup()
button_help = InlineKeyboardButton('Помощь', callback_data='help')
inline_keyboard.add(button_help)


@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    user_name = msg.from_user.first_name
    await msg.answer(
        f"<b>Добро пожаловать {user_name} в Give Me Recipe bot!</b>"
        f"\nОтправь мне фото твоих продуктов, и я скажу, что ты можешь приготовить.",
        parse_mode='HTML', reply_markup=main_keyboard
    )


@dp.message_handler(commands=['help'])
async def help_command(msg: types.Message):
    await msg.answer(
        "Отправь мне фото твоих продуктов, и я подскажу, что можно приготовить.",
        reply_markup=inline_keyboard
    )
    await msg.delete()


@dp.message_handler(content_types=['photo'])
async def photo_command(msg: types.Message):
    path = './' + ''.join(random.choice(string.ascii_lowercase) for i in range(16)) + '.jpg'
    await msg.photo[-1].download(path)
    await give_recipe(path)


@dp.callback_query_handler(lambda c: c.data == 'help')
async def process_callback_help(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Отправь мне фото продуктов, и я подскажу рецепт.')


if __name__ == '__main__':
    executor.start_polling(dp)
