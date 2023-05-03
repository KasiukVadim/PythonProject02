import data_base_methods
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from config import TOKEN_API
import data_base_methods as dbm


dbm.start_db()

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

sprint_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/start')) # Потом добавлю и доработаю

start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_buttons = [KeyboardButton('/привычки'), KeyboardButton('/ритуалы'), KeyboardButton('/заметки'),
                 KeyboardButton('/список_желаний'), KeyboardButton('/идеи'), KeyboardButton('/спринт')]
for but in start_buttons:
    start_kb.add(but)

habit_kb = ReplyKeyboardMarkup(resize_keyboard=True)
habit_buttons = [KeyboardButton('/start'), KeyboardButton('/Добавить_привычку'), KeyboardButton('/Удалить_привычку'), KeyboardButton('/Редактировать_привычку'),
                 KeyboardButton('/Просмотреть_список_привычек')]
for but in habit_buttons:
    habit_kb.add(but)

rituals_kb = ReplyKeyboardMarkup(resize_keyboard=True)
rituals_buttons = [KeyboardButton('/start'), KeyboardButton('/Добавить_ритуал'), KeyboardButton('/Удалить_ритуал'), KeyboardButton('/Редактировать_ритуал'),
                 KeyboardButton('/Просмотреть_список_ритуалов')]
for but in rituals_buttons:
    rituals_kb.add(but)

notes_kb = ReplyKeyboardMarkup(resize_keyboard=True)
notes_buttons = [KeyboardButton('/start'), KeyboardButton('/Добавить_заметку'), KeyboardButton('/Удалить_заметку'), KeyboardButton('/Редактировать_заметку'),
                 KeyboardButton('/Просмотреть_список_заметок')]
for but in notes_buttons:
    notes_kb.add(but)

wish_list_kb = ReplyKeyboardMarkup(resize_keyboard=True)
wish_list_buttons = [KeyboardButton('/start'), KeyboardButton('/Добавить_желание'), KeyboardButton('/Удалить_желание'), KeyboardButton('/Редактировать_желание'),
                 KeyboardButton('/Просмотреть_список_желаний')]
for but in wish_list_buttons:
    wish_list_kb.add(but)

ideas_kb = ReplyKeyboardMarkup(resize_keyboard=True)
ideas_buttons = [KeyboardButton('/start'), KeyboardButton('/Добавить_идею'), KeyboardButton('/Удалить_идею'), KeyboardButton('/Редактировать_идею'),
                 KeyboardButton('/Просмотреть_список_идей')]
for but in ideas_buttons:
    ideas_kb.add(but)

class ProfileStateGroup(StatesGroup):
    fill_id = State()
    fill_text = State()
    fill_time = State()
    fill_id_to_del = State()

async def on_startup(_):
    print('Бот был успешно запущен!')


@dp.message_handler(commands=["привычки"])
async def echo(message : types.Message):
    await message.answer(text="Привет! Добро пожаловать в раздел <b><em>Привычки</em></b>!\n"
                              "Здесь ты можешь создать список привычек, которые ты хочешь привить себе. При создании привычки,"
                              " нужно указать название привычки и частоту - сколько раз в неделю ты хочешь ее практиковать.\n"
                              "Затем в зависимости от выборанных дней тебе будут приходить уведомления, чтобы ты ничего "
                              "не пропустил и пришел к своей цели!",
                         parse_mode="HTML", reply_markup=habit_kb)
    await message.delete()

@dp.message_handler(commands=["Добавить_привычку"])
async def echo(message : types.Message) -> None:
    await message.answer(text="Здорово! Опишите саму привычку, чтобы вам было понятно. Далее я попрошу ввести частоту привычки, можете ее не указывать сейчас.",
                         parse_mode="HTML")
    await ProfileStateGroup.fill_text.set()


@dp.message_handler(commands=["Удалить_привычку"])
async def echo(message : types.Message) -> None:
    await message.answer(text="Чтобы удалить введите id (Можете посмотреть в общем списке)", # тут есть уязвимость, надо добавить проверку
                         parse_mode="HTML")
    await ProfileStateGroup.fill_id_to_del.set()


@dp.message_handler(state=ProfileStateGroup.fill_id_to_del)
async def echo(message : types.Message, state : FSMContext) -> None:
    data_base_methods.delete_record('habits', message.text)
    await message.answer(text="Запись была удалена!", # тут есть уязвимость, надо добавить проверку
                         parse_mode="HTML")
    await state.finish()


@dp.message_handler(commands=["Просмотреть_список_привычек"])
async def echo(message : types.Message):
    data = list(data_base_methods.show_table('habits', message.from_user.id))
    out_put_str = ''
    for rec in data:
        out_put_str += 'Привычка: ' + str(rec[1]) + ' График: ' + str(rec[2]) + ' id привычки ' + str(rec[3]) + '\n\n'
    await message.answer(text="Вот твой список привычек:\n\n" + out_put_str,
                         parse_mode="HTML")


@dp.message_handler(state=ProfileStateGroup.fill_text)
async def fill_txt(message : types.Message, state : FSMContext) -> None:
    async with state.proxy() as data:
        data['text'] = message.text
    await message.answer(text='Отлично! Теперь напиши, как часто ты хочешь практиковать свою новую привычку.'
                              ' Записать надо в формате чисел через пробел, где число - номер дня в неделе. Например : 1 3 5, что означает'
                              'понедельник, среда и пятница.')
    await ProfileStateGroup.fill_time.set()


@dp.message_handler(state=ProfileStateGroup.fill_time)
async def fill_date(message : types.Message, state : FSMContext) -> None:
    async with state.proxy() as data:
        data['time'] = message.text
        data_base_methods.create_profile('habits', message.from_user.id, data['text'], data['time'], data_base_methods.give_id('habits'))
        data_base_methods.show_table('habits', message.from_user.id)
    await message.answer(text='Супер! Поздравляю с добавлением новой привычки. Уверен, что у тебя получится '
                              'ее развить и она принесет тебе много пользы! Теперь каждое утро тебе будут приходить '
                              'уведомления-напоминания, чтобы ты ничего не забыл)')
    await state.finish()



@dp.message_handler(commands=["ритуалы"])
async def echo(message : types.Message):
    await message.answer(text="Привет! Добро пожаловать в раздел <b><em>Ритуалы</em></b>!\n"
                              "Здесь ты можешь создать список ритуалов, которые ты хочешь делать каждое утро/вечер. При создании ритуала,"
                              " нужно указать название ритуала, время и тип - когда ты хочешь его практиковать.\n"
                              "Затем в зависимости от выборанного времени тебе будут приходить уведомления, чтобы ты ничего "
                              "не забыл и хорошо проводил свое утро и вечер!",
                         parse_mode="HTML", reply_markup=rituals_kb)
    await message.delete()


@dp.message_handler(commands=["спринт"])
async def echo(message : types.Message):
    await message.answer(text="Этот раздел пока находится в разработке. Автор скоро его допилит(До конца итерации на исправления)",
                         parse_mode="HTML", reply_markup=start_kb)
    await message.delete()


@dp.message_handler(commands=["заметки"])
async def echo(message : types.Message):
    await message.answer(text="Привет! Добро пожаловать в раздел <b><em>Заметки</em></b>!\n"
                              "Здесь ты можешь создать список заметок, в который можешь отмечать важную для себя информацию. "
                              "При создании заметки нужно просто написать ее текст.\n",
                         parse_mode="HTML", reply_markup=notes_kb)
    await message.delete()


@dp.message_handler(commands=["идеи"])
async def echo(message : types.Message):
    await message.answer(text="Привет! Добро пожаловать в раздел <b><em>Идеи</em></b>!\n"
                              "Здесь ты можешь создать список идей, в котором ты может записывать интересные инсайты, чтобы потом вернуться к ним позже. "
                              "При создании идеи нужно просто написать ее текст.\n",
                         parse_mode="HTML", reply_markup=ideas_kb)
    await message.delete()


@dp.message_handler(commands=["список_желаний"])
async def echo(message : types.Message):
    await message.answer(text="Привет! Добро пожаловать в раздел <b><em>ВишЛист</em></b>!\n"
                              "Здесь ты можешь добавлять вещи в свой список желаний. Чтобы не забывать реализовывать их в жизни)",
                         parse_mode="HTML", reply_markup=wish_list_kb)
    await message.delete()


@dp.message_handler(commands=["start"])
async def echo(message : types.Message):
    await message.answer(text="Привет! Добро пожаловать в <b><em>Agile Diary Bot</em></b>!\n"
                              "Надеемся, что наш бот вам понравится и ваша продуктивность вырастет).\n"
                              "Предлагаю ознакомиться с моими коммандами с помощью функции <em>/help</em>!",
                         parse_mode="HTML", reply_markup=start_kb)
    await message.delete()


@dp.message_handler(commands=["help"])
async def help(message : types.Message):
    await message.answer(text="Наш бот имеет следующие комманды!\n\n"
                              "<em>/help</em> - вывод всех доступных комманд\n\n"
                              "<em>/description</em> - вывод описания бота и его функционала\n\n"
                              "<em>/habits</em> - переход в раздел работы с прывычками\n\n"
                              "<em>/rituals</em> - переход в раздел работы с ритуалами\n\n"
                              "<em>/sprint</em> - переход в раздел работы с спринтом\n\n"
                              "<em>/ideas</em> - переход в раздел работы с идеями\n\n"
                              "<em>/wishlist</em> - переход в раздел работы с ВишЛистом\n\n"
                              "<em>/notes</em> - переход в раздел работы с заметками\n\n"
                              "При работе с определенным разделом можно ознакомиться с его функционалом внутри него,"
                              " рекомендую перейти в раздел описания и ознакомиться с ним!",
                         parse_mode="HTML")
    await message.delete()


@dp.message_handler(commands=["description"])
async def description(message : types.Message):
    await message.answer(text="Цель данного бота помочь людям более осознанно относиться к своей жизни, четко "
                              "и грамотно планировать свое время, а главное - становиться сильнее и добиваться своих целей!\n"
                              "При проектировании данного бота я заимствовал схему планирования из книги 'Просто Космос'"
                              " Катерины Ленгольд, в которой она рассказывает о своих методиках "
                              "планирования времени и об отношении к жизни.\n"
                              "Итак, бот состоит из 6 блоков:\n"
                              "<b>Идеи</b>, <b>ВишЛист</b>, <b>Заметки</b>, <b>Ритуалы</b>, "
                              "<b>Мониторинг привычек</b> и <b>Спринт</b>. Каждый блок отвечает за свой функционал,"
                              " подробнее о каждом можно прочитать внутри этого блока.\n"
                              "Переходите в один из них и начинайте контролировать свою жизнь лучше! ",
                         parse_mode="HTML")
    await message.delete()


@dp.message_handler(commands=["give"])
async def echo(message : types.Message):
    await bot.send_sticker(message.from_user.id,
                           sticker='CAACAgIAAxkBAAEIxOdkTD8hWg3zoe8cdj8Ozqt1khMAAcQAAmcVAAKCsclLLV28TrMoxTQvBA')
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


