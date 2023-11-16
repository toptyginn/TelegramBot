import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import time


class User:
    def __init__(self):
        self.grade = '-'
        self.day = '-'
        self.number_of_grade = False
        self.grade_set = False
        self.day_set = False


# Инициализация бота:
users = {}
# Создание бота
bot = telebot.TeleBot('6802450385:AAF9ytn2osGDhEQUKIqp4R3bTDjPuSr7HaM')

# Клавиатура
keyboard_grade = InlineKeyboardMarkup()
keyboard_ABC = InlineKeyboardMarkup()
keyboard_ABCD = InlineKeyboardMarkup()
keyboard_AB = InlineKeyboardMarkup()
keyboard_days = InlineKeyboardMarkup()
keyboard_now = InlineKeyboardMarkup()

# Инициализация клавиатуры

# Номера классов
keyboard_grade.add(InlineKeyboardButton('7', callback_data='7'))
keyboard_grade.add(InlineKeyboardButton('8', callback_data='8'))
keyboard_grade.add(InlineKeyboardButton('9', callback_data='9'))
keyboard_grade.add(InlineKeyboardButton('10', callback_data='10'))
keyboard_grade.add(InlineKeyboardButton('11', callback_data='11'))

# 3 буквы
keyboard_ABC.add(InlineKeyboardButton('А', callback_data='А'))
keyboard_ABC.add(InlineKeyboardButton('Б', callback_data='Б'))
keyboard_ABC.add(InlineKeyboardButton('В', callback_data='В'))
keyboard_ABC.add(InlineKeyboardButton('Назад', callback_data='return'))

# 2 буквы
keyboard_AB.add(InlineKeyboardButton('А', callback_data='А'))
keyboard_AB.add(InlineKeyboardButton('Б', callback_data='Б'))
keyboard_AB.add(InlineKeyboardButton('Назад', callback_data='return'))

# 4 буквы
keyboard_ABCD.add(InlineKeyboardButton('А', callback_data='А'))
keyboard_ABCD.add(InlineKeyboardButton('Б', callback_data='Б'))
keyboard_ABCD.add(InlineKeyboardButton('В', callback_data='В'))
keyboard_ABCD.add(InlineKeyboardButton('Г', callback_data='Г'))
keyboard_ABCD.add(InlineKeyboardButton('Назад', callback_data='return'))

#Сегодня, вчера или завтра выбор дня для расписания
keyboard_now.add(InlineKeyboardButton('Вчера', callback_data='Вчера'))
keyboard_now.add(InlineKeyboardButton('Сегодня', callback_data='Сегодня'))
keyboard_now.add(InlineKeyboardButton('Завтра', callback_data='Завтра'))
keyboard_now.add(InlineKeyboardButton('Другой день', callback_data='other'))
keyboard_now.add(InlineKeyboardButton('Назад', callback_data='return'))

# Дни недели
keyboard_days.add(InlineKeyboardButton('Понедельник', callback_data='0'))
keyboard_days.add(InlineKeyboardButton('Вторник', callback_data='1'))
keyboard_days.add(InlineKeyboardButton('Среда', callback_data='2'))
keyboard_days.add(InlineKeyboardButton('Четверг', callback_data='3'))
keyboard_days.add(InlineKeyboardButton('Пятница', callback_data='4'))
keyboard_days.add(InlineKeyboardButton('Суббота', callback_data='5'))
keyboard_days.add(InlineKeyboardButton('Назад', callback_data='return'))

# Функционал бота

@bot.message_handler(commands=['start'])
def handle_start(message):
    global id, users
    id = str(message.from_user.id)
    users[id] = User()

    bot.send_message(message.chat.id, 'Welcome to my bot!')
    bot.send_message(message.chat.id, 'Here are some helpful commands:')
    bot.send_message(message.chat.id, '/start - Start the bot')
    bot.send_message(message.chat.id, '/help - Show this help message')
    bot.send_message(message.chat.id, '/timesheet - Show your timesheet')

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, 'Here are some helpful commands:')
    bot.send_message(message.chat.id, '/start - Start the bot')
    bot.send_message(message.chat.id, '/help - Show this help message')
    bot.send_message(message.chat.id, '/timesheet - Show your timesheet')

@bot.message_handler(commands=['timesheet'])
def timesheet(message):
    global id, users
    id = str(message.from_user.id)
    users[id] = User()
    bot.send_message(message.chat.id, 'Выберите свой класс', reply_markup=keyboard_grade)

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global id, users
    id = str(call.message.from_user.id)
    if users[id].grade_set:
        bot.send_message(call.message.chat.id, f'Выбран класс: {users[id].grade}')
    if users[id].day_set:
        bot.send_message(call.message.from_user.id, f'Выбран день: {users[id].day}')
    if not users[id].grade_set:
        if users[id].grade == '-':
            match  call.data:
                case '7':
                    bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABC)
                    users[id].grade = call.data
                case '8':
                    bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABCD)
                    users[id].grade = call.data
                case '9':
                    bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABCD)
                    users[id].grade = call.data
                case '10':
                    bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABCD)
                    users[id].grade = call.data
                case '11':
                    bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_AB)
                    users[id].grade = call.data
                case _:
                    bot.send_message(call.message.chat.id, 'Неверный выбор')
        else:
            users[id].grade += call.data
            users[id].grade_set = True
            bot.send_message(call.message.chat.id, f'Выбран класс: {users[id].grade}')
            bot.send_message(call.message.chat.id, 'Выберите день', reply_markup=keyboard_now)
    elif not users[id].day_set:
        match  call.data:
            case 'Вчера':
                users[id].day = time.localtime(time.time()).tm_wday - 1
                users[id].day_set = True
            case 'Сегодня':
                users[id].day = time.localtime(time.time()).tm_wday
                users[id].day_set = True
            case 'Завра':
                users[id].day = time.localtime(time.time()).tm_wday + 1
                users[id].day_set = True
            case 'other':
                bot.send_message(call.message.chat.id, 'Выберите день', reply_markup=keyboard_days)
            case 'return':
                users[id].grade_set = False
                users[id].grade = '-'
            case _:
                users[id].day = call.data
                users[id].day_set = True
                bot.send_message(call.message.chat.id, f'Выбран день: {users[id].day}')

bot.polling(none_stop=True)
