import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import time

import Help


class User:
    def __init__(self):
        self.grade = '-'
        self.day = '-'
        self.number_of_grade = False
        self.grade_set = False
        self.day_set = False


# Инициализация бота:
users = {}
id = ''
days_of_week = ['Понедельник', "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
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

# Сегодня, вчера или завтра выбор дня для расписания
keyboard_now.add(InlineKeyboardButton('Вчера', callback_data='Вчера'))
keyboard_now.add(InlineKeyboardButton('Сегодня', callback_data='Сегодня'))
keyboard_now.add(InlineKeyboardButton('Завтра', callback_data='Завтра'))
keyboard_now.add(InlineKeyboardButton('Другой день', callback_data='other'))
keyboard_now.add(InlineKeyboardButton('Назад', callback_data='return'))

# Дни недели
keyboard_days.add(InlineKeyboardButton('Понедельник', callback_data='Понедельник'))
keyboard_days.add(InlineKeyboardButton('Вторник', callback_data='Вторник'))
keyboard_days.add(InlineKeyboardButton('Среда', callback_data='Среда'))
keyboard_days.add(InlineKeyboardButton('Четверг', callback_data='Четверг'))
keyboard_days.add(InlineKeyboardButton('Пятница', callback_data='Пятница'))
keyboard_days.add(InlineKeyboardButton('Суббота', callback_data='Суббота'))
keyboard_days.add(InlineKeyboardButton('Назад', callback_data='return'))


# Функционал бота

@bot.message_handler(commands=['start'])
def handle_start(message):
    global id, users
    id = str(message.from_user.id)
    users[id] = User()

    bot.send_message(message.chat.id, f'Добро пожаловать {message.from_user.first_name}!')
    bot.send_message(message.chat.id, 'Доступные команды:')
    bot.send_message(message.chat.id, '/start - Запусить бота')
    bot.send_message(message.chat.id, '/help - Вывод доступных команд')
    bot.send_message(message.chat.id, '/timesheet - Вывод расписания')


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, 'Доступные команды:')
    bot.send_message(message.chat.id, '/start - Запусить бота')
    bot.send_message(message.chat.id, '/help - Вывод доступных команд')
    bot.send_message(message.chat.id, '/timesheet - Вывод расписания')


@bot.message_handler(commands=['timesheet'])
def timesheet(message):
    global id, users
    id = str(message.from_user.id)
    users[id] = User()
    bot.send_message(message.chat.id, 'Выберите свой класс', reply_markup=keyboard_grade)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global id, users
    # id = str(call.message.from_user.id)
    # if id in users.keys():
    # if users[id].grade_set:
    #     bot.send_message(call.message.chat.id, f'Выбран класс: {users[id].grade}')
    # if users[id].day_set:
    #     bot.send_message(call.message.chat.id, f'Выбран день: {users[id].day}')
    if not (users[id].grade_set and users[id].day_set):
        if not users[id].grade_set:
            if users[id].grade == '-':
                match call.data:
                    case '7':
                        users[id].grade = call.data
                        bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABC)
                    case '8':
                        users[id].grade = call.data
                        bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABCD)
                    case '9':
                        users[id].grade = call.data
                        bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABCD)
                    case '10':
                        users[id].grade = call.data
                        bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABCD)
                    case '11':
                        users[id].grade = call.data
                        bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_AB)
                    case _:
                        bot.send_message(call.message.chat.id, 'Неверный выбор')
            else:
                users[id].grade += call.data
                users[id].grade_set = True
                bot.send_message(call.message.chat.id, f'Выбран класс: {users[id].grade}')
                bot.send_message(call.message.chat.id, 'Выберите день', reply_markup=keyboard_now)
        elif not users[id].day_set:
            match call.data:
                case 'Вчера':
                    users[id].day_set = True
                    users[id].day = days_of_week[time.localtime(time.time()).tm_wday - 1]
                    bot.send_message(call.message.chat.id, f'Выбран день: {users[id].day}')
                case 'Сегодня':
                    users[id].day_set = True
                    users[id].day = days_of_week[time.localtime(time.time()).tm_wday]
                    bot.send_message(call.message.chat.id, f'Выбран день: {users[id].day}')
                case 'Завтра':
                    users[id].day_set = True
                    users[id].day = days_of_week[time.localtime(time.time()).tm_wday + 1]
                    bot.send_message(call.message.chat.id, f'Выбран день: {users[id].day}')
                case 'other':
                    bot.send_message(call.message.chat.id, 'Выберите день', reply_markup=keyboard_days)
                case 'return':
                    users[id].grade_set = False
                    users[id].grade = '-'
                    bot.send_message(call.message.chat.id, f'Выбран класс: {users[id].grade}')
                case _:
                    users[id].day = call.data
                    users[id].day_set = True
                    bot.send_message(call.message.chat.id, f'Выбран день: {users[id].day}')
        if users[id].grade_set and users[id].day_set:
            answer = ['\n']
            for i in Help.timesheet[users[id].grade][users[id].day].keys():
                try:
                    if len(Help.timesheet[users[id].grade][users[id].day][i]) > 0:
                        if Help.timesheet[users[id].grade][users[id].day][i][0] == 'Пусто':
                            answer.append(f'{i}: ---')
                        else:
                            answer.append(
                                f'{i}: {Help.timesheet[users[id].grade][users[id].day][i][0]} {Help.timesheet[users[id].grade][users[id].day][i][-1]}')
                    else:
                        answer.append(f'{i}: ---')
                except IndexError:
                    answer.append(f'{i}: ---')
            answer = '\n'.join(answer)
            bot.send_message(call.message.chat.id, f'Расписание на {users[id].day}: {answer}')

        # print(Help.timesheet[users[id].grade][users[id].day])
    # else:
    #     users[id] = User()


bot.polling(none_stop=True)
