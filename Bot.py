import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import time


def if_set(data, if_data, value):
    if data == if_data:
        return value
    else:
        pass

# Инициализация бота:
# Создание бота
bot = telebot.TeleBot('6802450385:AAF9ytn2osGDhEQUKIqp4R3bTDjPuSr7HaM')

# Глобальные переменные

grade = '-'
day = '-'
grade_set = False
day_set = False


# Запрос

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
keyboard_ABC.add(InlineKeyboardButton('Вернуться к классам', callback_data='return'))

# 2 буквы
keyboard_AB.add(InlineKeyboardButton('А', callback_data='А'))
keyboard_AB.add(InlineKeyboardButton('Б', callback_data='Б'))
keyboard_ABC.add(InlineKeyboardButton('Вернуться к классам', callback_data='return'))

# 4 буквы
keyboard_ABCD.add(InlineKeyboardButton('А', callback_data='А'))
keyboard_ABCD.add(InlineKeyboardButton('Б', callback_data='Б'))
keyboard_ABCD.add(InlineKeyboardButton('В', callback_data='В'))
keyboard_ABCD.add(InlineKeyboardButton('Г', callback_data='Г'))
keyboard_ABC.add(InlineKeyboardButton('Вернуться к классам', callback_data='return'))

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
'''
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    keyboard.add(InlineKeyboardButton('7', callback_data='7'))
    keyboard.add(InlineKeyboardButton('8', callback_data='8'))
    keyboard.add(InlineKeyboardButton('9', callback_data='9'))
    keyboard.add(InlineKeyboardButton('10', callback_data='10'))
    keyboard.add(InlineKeyboardButton('11', callback_data='11'))
    bot.send_message(call.id, 'Выберите свой класс', reply_markup=keyboard)
    bot.answer_callback_query(call.id, text='Не проигнорил')
'''
@bot.message_handler(commands=['start'])
def handle_start(message):
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
    bot.send_message(message.chat.id, 'Выберите свой класс', reply_markup=keyboard_grade)

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global day, grade, grade_set, day_set
    if (grade_set):
        bot.send_message(call.message.chat.id, f'Выбран класс: {grade}')
    if (day_set):
        bot.send_message(call.message.chat.id, f'Выбран день: {day}')
    if not grade_set:
        if (grade=='-'):
            match  call.data:
                case '7':
                    bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABC)
                    grade = call.data
                case '8':
                    bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABCD)
                    grade = call.data
                case '9':
                    bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABCD)
                    grade = call.data
                case '10':
                    bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABCD)
                    grade = call.data
                case '11':
                    bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_AB)
                    grade = call.data
                case _:
                    bot.send_message(call.message.chat.id, 'Неверный выбор')
        else:
            grade += call.data
            grade_set = True
            bot.send_message(call.message.chat.id, f'Выбран класс: {grade}')
            bot.send_message(call.message.chat.id, 'Выберите день', reply_markup=keyboard_now)
    elif not day_set:
        match  call.data:
            case 'Вчера':        
                day = time.localtime(time.time()).tm_mday - 1
                day_set = True
            case 'Сегодня':        
                day = time.localtime(time.time()).tm_mday 
                day_set = True
            case 'Завра':        
                day = time.localtime(time.time()).tm_mday + 1
                day_set = True
            case 'other':        
                bot.send_message(call.message.chat.id, 'Выберите день', reply_markup=keyboard_days)
            case _:
                day = call.data
                day_set = True
                bot.send_message(call.message.chat.id, f'Выбран день: {day}')

bot.polling(none_stop=True)