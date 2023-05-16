from dp_bot_stor_db import *
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from datetime import datetime

class ProfileStateGroupNotes(StatesGroup):
    fill_id = State()
    fill_text = State()
    fill_id_to_del = State()

#@dp.message_handler(commands=["заметки"])
async def notes(message : types.Message):
    await message.answer(text="Привет! Добро пожаловать в раздел <b><em>Заметки</em></b>!\n"
                              "Здесь ты можешь создать список заметок, в который можешь отмечать важную для себя информацию. "
                              "При создании заметки нужно просто написать ее текст.\n",
                         parse_mode="HTML", reply_markup=notes_kb)
    await message.delete()

#@dp.message_handler(commands=["Добавить_заметку"])
async def add_note(message : types.Message) -> None:
    await message.answer(text="Здорово! Теперь просто напишите текст заметки!",
                         parse_mode="HTML")
    await ProfileStateGroupNotes.fill_text.set()

#@dp.message_handler(commands=["Удалить_заметку"])
async def delete_note(message : types.Message) -> None:
    await message.answer(text="Чтобы удалить заметку введите ID (Можете посмотреть в общем списке)", # тут есть уязвимость, надо добавить проверку
                         parse_mode="HTML")
    await ProfileStateGroupNotes.fill_id_to_del.set()

#@dp.message_handler(commands=["Просмотреть_список_заметок"])
async def show_notes(message : types.Message):
    data = list(data_base.show_table('notes', message.from_user.id))
    out_put_str = ''
    for rec in data:
        out_put_str += 'Заметка: ' + str(rec[1]) + '\nДата добавления: ' + str(rec[2]) + '\nID заметки: ' + str(rec[3]) + '\n\n'
    await message.answer(text="Вот ваш список заметок:\n\n" + out_put_str,
                         parse_mode="HTML")

#@dp.message_handler(state=ProfileStateGroupNotes.fill_id_to_del)
async def fill_note_id(message : types.Message, state : FSMContext) -> None:
    data_base.delete_record('notes', message.text)
    await message.answer(text="Запись была удалена!", # тут есть уязвимость, надо добавить проверку
                         parse_mode="HTML")
    await state.finish()

#@dp.message_handler(state=ProfileStateGroupNotes.fill_text)
async def fill_note_txt(message : types.Message, state : FSMContext) -> None:
    async with state.proxy() as data:
        data['text'] = message.text
        data_base.create_profile('notes', message.from_user.id, data['text'], datetime.now().date() , data_base.get_id('notes'))
    await message.answer(text='Отлично! Теперь вы можете прочитать заметку когда угодно, используя команду /Просмотреть_список_привычек')
    await state.finish()

