from asyncio.windows_events import NULL
from aiogram import *
#from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import sqlite3

bot = Bot(token="5137903807:AAEtrp9rSqXKStp93h2_Q_OhNfey1QUJXoo")
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('✍Добавить', '💪Список моих задач','👀Помощь')
    await message.answer(f"Здравствуйте, {message.from_user.username}🙌!\nЯ ваш личный секретарь ^))")
    await message.answer("Чем могу вам помочь?", reply_markup=keyboard)


@dp.message_handler(Text(equals='✍Добавить'))
async def about_problem(message: types.message):
    await message.answer('Впишите ваше дело и я его вам напомню!')
    await message.answer('Шаблон - где? что? когда? время?\nПример - Кванториум вебинар завтра в 12:00')
    
    
@dp.message_handler(Text(equals='💪Список моих задач'))
async def get_allproblem(message: types.message):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM problem WHERE user_id = {message.from_user.id}")
    problems = cur.fetchall()
    if len(problems)==0:
        await message.answer('У вас дел нет, нажмите Напомнить')
    else:
        for i,pr in enumerate(problems):
            key = types.InlineKeyboardButton(' ✅Завершено', callback_data=pr[1])
            key1 = types.InlineKeyboardButton('time', callback_data='time')
            inline_kb_full = types.InlineKeyboardMarkup(row_width=1).add(key)
            await message.answer(f"Дело #{i+1} - {pr[1]}", reply_markup=inline_kb_full)

@dp.message_handler(Text(equals='👀Помощь'))
async def get_help(message: types.message):
    await message.answer('Я просто бот, что ты от меня хочешь????')


@dp.callback_query_handler()
async def process_callback(callback_data: types.CallbackQuery):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM problem WHERE problem='{callback_data.data}'")
    conn.commit()
    await bot.send_message(callback_data.from_user.id,'Задача завершена!')
    
@dp.message_handler()
async def set_problem(message:types.message):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS problem(id INTEGER PRIMARY KEY, problem TEXT, user_id INTENGER)')
    cur.execute(f'INSERT INTO problem VALUES(NULL,"{message.text}", "{message.from_user.id}")')
    conn.commit()
    await message.answer('Задача добавлена в Список моих задач')


def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()