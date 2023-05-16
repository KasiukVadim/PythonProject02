from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_buttons = [KeyboardButton('/привычки'), KeyboardButton('/ритуалы'), KeyboardButton('/заметки')]
for but in start_buttons:
    start_kb.add(but)

habit_kb = ReplyKeyboardMarkup(resize_keyboard=True)
habit_buttons = [KeyboardButton('/start'), KeyboardButton('/Добавить_привычку'), KeyboardButton('/Удалить_привычку'),
                 KeyboardButton('/Просмотреть_список_привычек')]
for but in habit_buttons:
    habit_kb.add(but)

rituals_kb = ReplyKeyboardMarkup(resize_keyboard=True)
rituals_buttons = [KeyboardButton('/start'), KeyboardButton('/Добавить_ритуал'), KeyboardButton('/Удалить_ритуал'),
                 KeyboardButton('/Просмотреть_список_ритуалов')]
for but in rituals_buttons:
    rituals_kb.add(but)

notes_kb = ReplyKeyboardMarkup(resize_keyboard=True)
notes_buttons = [KeyboardButton('/start'), KeyboardButton('/Добавить_заметку'), KeyboardButton('/Удалить_заметку'),
                 KeyboardButton('/Просмотреть_список_заметок')]
for but in notes_buttons:
    notes_kb.add(but)
