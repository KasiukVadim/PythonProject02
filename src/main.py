from notes import *
from habits import *
from rituals import *

dp = Dispatcher(bot, storage=storage)
dp.register_message_handler(callback=notes, commands="заметки")
dp.register_message_handler(callback=habits, commands="привычки")
dp.register_message_handler(callback=rituals, commands="ритуалы")
dp.register_message_handler(callback=add_note, commands="Добавить_заметку")
dp.register_message_handler(callback=add_habit, commands="Добавить_привычку")
dp.register_message_handler(callback=add_ritual, commands="Добавить_ритуал")
dp.register_message_handler(callback=delete_note, commands="Удалить_заметку")
dp.register_message_handler(callback=delete_habit, commands="Удалить_привычку")
dp.register_message_handler(callback=delete_ritual, commands="Удалить_ритуал")
dp.register_message_handler(callback=show_notes, commands="Просмотреть_список_заметок")
dp.register_message_handler(callback=show_habits, commands="Просмотреть_список_привычек")
dp.register_message_handler(callback=show_rituals, commands="Просмотреть_список_ритуалов")
dp.register_message_handler(callback=fill_note_id, state=ProfileStateGroupNotes.fill_id_to_del)
dp.register_message_handler(callback=fill_ritual_id, state=ProfileStateGroupRituals.fill_id_to_del)
dp.register_message_handler(callback=fill_habit_id, state=ProfileStateGroupHabits.fill_id_to_del)
dp.register_message_handler(callback=fill_note_txt, state=ProfileStateGroupNotes.fill_text)
dp.register_message_handler(callback=fill_habit_txt, state=ProfileStateGroupHabits.fill_text)
dp.register_message_handler(callback=fill_ritual_txt, state=ProfileStateGroupRituals.fill_text)
dp.register_message_handler(callback=fill_ritual_time, state=ProfileStateGroupRituals.fill_time)
dp.register_message_handler(callback=fill_habit_date, state=ProfileStateGroupHabits.fill_time)


@dp.message_handler(commands=["start"])
async def start(message : types.Message):
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
                              "<em>/привычки</em> - переход в раздел работы с прывычками\n\n"
                              "<em>/ритуалы</em> - переход в раздел работы с ритуалами\n\n"
                              "<em>/идеи</em> - переход в раздел работы с идеями\n\n"
                              "<em>/список_желаний</em> - переход в раздел работы с ВишЛистом\n\n"
                              "<em>/заметки</em> - переход в раздел работы с заметками\n\n"
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
async def give(message : types.Message):
    await bot.send_sticker(message.from_user.id,
                           sticker='CAACAgIAAxkBAAEIxOdkTD8hWg3zoe8cdj8Ozqt1khMAAcQAAmcVAAKCsclLLV28TrMoxTQvBA')
    await message.delete()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


