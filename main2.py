from email import message
from email.message import Message
from aiogram import *
import aiogram
from aiogram.dispatcher.filters import Text
from sqlite3 import *


bot = Bot(token='5137903807:AAEtrp9rSqXKStp93h2_Q_OhNfey1QUJXoo')
dp =  Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(mes: types.message):
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keybord.add('Добавить задачу', 'Мои задачи', 'помощь')
    await mes.answer(f'Привет, {mes.from_user.username}, я твой личный секретарь')
    await mes.answer('Чем я могу помочь?', reply_markup = keybord)
    
@dp.message_handler(Text(equals='помощь'))
async def help(mes: types.message):
    await mes.answer('я всего лишь бот, помоги себе сам')
    
@dp.message_handler(Text(equals='Добавить задачу'))
async def fun(mes: types.message):
    await mes.answer('Добавьте задачу')
    await mes.answer('Что-то типа работа завтра в 17.50')
    
@dp.message_handler(Text(equals='Мои задачи'))
async def all_problems(mes: types.message):
    conn = connect('data.db')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM problems WHERE user_id = {mes.from_user.id}')
    problem = cur.fetchall()
    if len(problem)==0:
        await mes.answer('у вас нет задач')
    else:
        for i, pr in enumerate(problem):
            key = types.InlineKeyboardButton('✅Завершено', callback_data=pr[1])
            keybord = types.InlineKeyboardMarkup(row_width=1).add(key)
            await mes.answer(pr[1], reply_markup=keybord)
    conn.commit()
            
@dp.callback_query_handler()
async def delete_pr(pr: types.CallbackQuery):
    conn = connect('data.db')
    cur = conn.cursor()
    cur.execute(f'DELETE FROM problems WHERE problem="{pr.data}"')
    conn.commit()
    await bot.send_message(pr.from_user.id,'Задача завершена!')
    
@dp.message_handler()
async def add_problem(mes: types.message):
    conn = connect('data.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS problems(id INTEGER PRIMARY KEY, problem TEXT, user_id INTEGER)')
    cur.execute(f'INSERT INTO problems VALUES(NULL, "{mes.text}", {mes.from_user.id})')
    conn.commit()
    
def main():
    executor.start_polling(dp)
    
if __name__ == '__main__':
    main()