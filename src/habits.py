from dp_bot_stor_db import *
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

class ProfileStateGroupHabits(StatesGroup):
    fill_id = State()
    fill_text = State()
    fill_time = State()
    fill_id_to_del = State()

#@dp.message_handler(commands=["привычки"])
async def habits(message : types.Message):
    await message.answer(text="Привет! Добро пожаловать в раздел <b><em>Привычки</em></b>!\n"
                              "Здесь ты можешь создать список привычек, которые ты хочешь привить себе. При создании привычки,"
                              " нужно указать название привычки и частоту - сколько раз в неделю ты хочешь ее практиковать.\n"
                              "Затем в зависимости от выборанных дней тебе будут приходить уведомления, чтобы ты ничего "
                              "не пропустил и пришел к своей цели!",
                         parse_mode="HTML", reply_markup=habit_kb)
    await message.delete()

#@dp.message_handler(commands=["Добавить_привычку"])
async def add_habit(message : types.Message) -> None:
    await message.answer(text="Здорово! Опишите саму привычку, чтобы вам было понятно. Далее я попрошу ввести частоту привычки, можете ее не указывать сейчас.",
                         parse_mode="HTML")
    await ProfileStateGroupHabits.fill_text.set()

#@dp.message_handler(commands=["Удалить_привычку"])
async def delete_habit(message : types.Message) -> None:
    await message.answer(text="Чтобы удалить введите id (Можете посмотреть в общем списке)", # тут есть уязвимость, надо добавить проверку
                         parse_mode="HTML")
    await ProfileStateGroupHabits.fill_id_to_del.set()

#@dp.message_handler(commands=["Просмотреть_список_привычек"])
async def show_habits(message : types.Message):
    data = list(data_base.show_table('habits', message.from_user.id))
    out_put_str = ''
    for rec in data:
        out_put_str += 'Привычка: ' + str(rec[1]) + '\nГрафик: ' + str(rec[2]) + '\nID привычки: ' + str(rec[3]) + '\n\n'
    await message.answer(text="Вот твой список привычек:\n\n" + out_put_str,
                         parse_mode="HTML")

#@dp.message_handler(state=ProfileStateGroupHabits.fill_id_to_del)
async def fill_habit_id(message : types.Message, state : FSMContext) -> None:
    data_base.delete_record('habits', message.text)
    await message.answer(text="Запись была удалена!", # тут есть уязвимость, надо добавить проверку
                         parse_mode="HTML")
    await state.finish()

#@dp.message_handler(state=ProfileStateGroupHabits.fill_text)
async def fill_habit_txt(message : types.Message, state : FSMContext) -> None:
    async with state.proxy() as data:
        data['text'] = message.text
    await message.answer(text='Отлично! Теперь напиши, как часто ты хочешь практиковать свою новую привычку.'
                              ' Записать надо в формате чисел через пробел, где число - номер дня в неделе. Например : 1 3 5, что означает'
                              'понедельник, среда и пятница.')
    await ProfileStateGroupHabits.fill_time.set()

#@dp.message_handler(state=ProfileStateGroupHabits.fill_time)
async def fill_habit_date(message : types.Message, state : FSMContext) -> None:
    async with state.proxy() as data:
        data['time'] = message.text
        data_base.create_profile('habits', message.from_user.id, data['text'], data['time'], data_base.get_id('habits'))
        data_base.show_table('habits', message.from_user.id)
    await message.answer(text='Супер! Поздравляю с добавлением новой привычки. Уверен, что у тебя получится '
                              'ее развить и она принесет тебе много пользы! Теперь каждое утро тебе будут приходить '
                              'уведомления-напоминания, чтобы ты ничего не забыл)')
    await state.finish()

