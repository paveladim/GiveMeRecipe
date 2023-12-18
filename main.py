from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from recipe import give_recipe
import random
import string

TOKEN_API = '6539535216:AAEINREJT9pRtMl4v4jW0zw5xMGzLyr9Yro'

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    await msg.answer(text=
        '''
            Welcome to Give Me Recipe bot! Send me a photo of your products and I will tell you what you can cook with them.
        ''')


@dp.message_handler(commands=['help'])
async def help_command(msg: types.Message):
    await msg.answer(text=
        '''
            Send me a photo of your products and I will tell you what you can cook with them.
        ''')
    await msg.delete()


@dp.message_handler(content_types=['photo'])
async def photo_command(msg: types.Message):
    path = './' + ''.join(random.choice(string.ascii_lowercase) for i in range(16)) + '.jpg'
    await msg.photo[-1].download(path)
    await give_recipe(path)
    # await msg.answer(answer)


if __name__ == '__main__':
    executor.start_polling(dp)