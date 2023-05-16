from dp_bot_store_db import *
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

class ProfileStateGroupRituals(StatesGroup):
    fill_id = State()
    fill_text = State()
    fill_id_to_del = State()
    fill_time = State()

#@dp.message_handler(commands=["ритуалы"])
async def rituals(message : types.Message):
    await message.answer(text="Привет! Добро пожаловать в раздел <b><em>Ритуалы</em></b>!\n"
                              "Здесь ты можешь создать список ритуалов, которые ты хочешь делать каждое утро/вечер. При создании ритуала,"
                              " нужно указать название ритуала, время и тип - когда ты хочешь его практиковать.\n"
                              "Затем в зависимости от выборанного времени тебе будут приходить уведомления, чтобы ты ничего "
                              "не забыл и хорошо проводил свое утро и вечер!",
                         parse_mode="HTML", reply_markup=rituals_kb)
    await message.delete()

#@dp.message_handler(commands=["Добавить_ритуал"])
async def add_ritual(message : types.Message) -> None:
    await message.answer(text="Здорово! Теперь просто напишите, что за ритуал ты хочешь проводить!",
                         parse_mode="HTML")
    await ProfileStateGroupRituals.fill_text.set()

#@dp.message_handler(commands=["Удалить_ритуал"])
async def delete_ritual(message : types.Message) -> None:
    await message.answer(text="Чтобы удалить Ритуал введите ID (Можете посмотреть в общем списке)", # тут есть уязвимость, надо добавить проверку
                         parse_mode="HTML")
    await ProfileStateGroupRituals.fill_id_to_del.set()

#@dp.message_handler(commands=["Просмотреть_список_ритуалов"])
async def show_rituals(message : types.Message):
    data = list(data_base.show_table('rituals', message.from_user.id))
    out_put_str = ''
    for rec in data:
        out_put_str += 'Ритуал: ' + str(rec[1]) + '\nВремя ритуала: ' + str(rec[2]) + '\nID ритуала: ' + str(rec[3]) + '\n\n'
    await message.answer(text="Вот ваш список ритуалов:\n\n" + out_put_str,
                         parse_mode="HTML")

#@dp.message_handler(state=ProfileStateGroupRituals.fill_id_to_del)
async def fill_ritual_id(message : types.Message, state : FSMContext) -> None:
    data_base.delete_record('rituals', message.text)
    await message.answer(text="Запись была удалена!", # тут есть уязвимость, надо добавить проверку
                         parse_mode="HTML")
    await state.finish()

#@dp.message_handler(state=ProfileStateGroupRituals.fill_text)
async def fill_ritual_txt(message : types.Message, state : FSMContext) -> None:
    async with state.proxy() as data:
        data['text'] = message.text
    await message.answer(text='Отлично! Теперь введите время когда будете делать этот ритуал в формате времени\nНапример : 8:00')
    await ProfileStateGroupRituals.fill_time.set()

#@dp.message_handler(state=ProfileStateGroupRituals.fill_time)
async def fill_ritual_time(message : types.Message, state : FSMContext) -> None:
    async with state.proxy() as data:
        data['time'] = message.text
        data_base.create_profile('rituals', message.from_user.id, data['text'], data['time'], data_base.get_id('rituals'))
    await message.answer(text='Супер! Поздравляю с добавлением нового ритуала! Вы всегда можете посмотреть свои ритуалы используя команду: /Просмотреть_список_ритуалов')
    await state.finish()

