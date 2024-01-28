import random

import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import time
import tokens
import Help
import logging
import os
import sys

class User:
    def __init__(self):
        self.grade = '-'
        self.day = '-'
        self.number_of_grade = False
        self.grade_set = False
        self.day_set = False


# Логи
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

f = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s', "%d-%m-%Y %H:%M:%S")
fh = logging.FileHandler(os.path.join('logs', 'bot.log'))

fh.setFormatter(f)
logger.addHandler(fh)

#Расписание
timesheet = Help.parsing_timesheet('Расписание УРОКОВ с 11.09.2023-ПРАВКА1.xlsx')

# вывод в консоль
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(f)
# add the handler to the root logger
logging.getLogger().addHandler(console)

# Emoji
counts_emoji = {'1': '\U00000031', '2': '\U00000032', '3': '\U00000033', '4': '\U00000034', '5': '\U00000035',
                '6': '\U00000036', '7': '\U00000037', '8': '\U00000038'}

days_emoji = {'Понедельник': ['\U0001F971', '\U0001F644', '\U0001F611', '\U0001F643', '\U0001F97A'],
              'Вторник': ['\U0001F9E0', '\U0001F978', '\U0001F913', '\U0001F9D0', '\U0001F575'],
              'Среда': ['\U0001F975', '\U0001FAE0', '\U0001F928', '\U00002764', '\U0001F979'],
              'Четверг': ['\U0001F642', '\U0001F970', '\U0001F61C', '\U0001F917', '\U0001F60A'],
              'Пятница': ['\U0001F389', '\U0001F386', '\U0001F525', '\U00002660', '\U0001F451'],
              'Суббота': ['\U0001F680', '\U0001F355', '\U0001F496', '\U0001F92F', '\U0001F60E']}

# Инициализация бота:
users = {}
id = ''
days_of_week = ['Понедельник', "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
# Создание бота
bot = telebot.TeleBot(tokens.main_token)
except_bot = telebot.TeleBot(tokens.except_token)

# Клавиатура
comands = ReplyKeyboardMarkup()
keyboard_grade = InlineKeyboardMarkup()
keyboard_ABC = InlineKeyboardMarkup()
keyboard_ABCD = InlineKeyboardMarkup()
keyboard_AB = InlineKeyboardMarkup()
keyboard_days = InlineKeyboardMarkup()
keyboard_now = InlineKeyboardMarkup()

# Инициализация клавиатуры
comands.add('/help', '/timesheet')

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
    logger.info(f'{message.from_user.first_name}({message.from_user.id}) has started messaging')
    global id, users
    id = str(message.from_user.id)
    users[id] = User()

    bot.send_message(message.chat.id, f'Добро пожаловать {message.from_user.first_name}!', reply_markup=comands)
    bot.send_message(message.chat.id, 'Доступные команды:')
    bot.send_message(message.chat.id, '/start - Запусить бота')
    bot.send_message(message.chat.id, '/help - Вывод доступных команд')
    bot.send_message(message.chat.id, '/timesheet - Вывод расписания')


@bot.message_handler(commands=['help'])
def handle_help(message):
    logger.info(f'{message.from_user.first_name} needs help')
    bot.send_message(message.chat.id, 'Инструкция: Бот находится на ранней стадии разработки так что писать ему не'
                                      ' очень удобно чтобы снова написать боту снова используйте команду и заполните'
                                      ' класс и день')
    bot.send_message(message.chat.id, 'Доступные команды:')
    bot.send_message(message.chat.id, '/start - Запусить бота')
    bot.send_message(message.chat.id, '/help - Вывод доступных команд')
    bot.send_message(message.chat.id, '/timesheet - Вывод расписания')


@bot.message_handler(commands=['timesheet'])
def timesheet(message):
    logger.info(f'{message.from_user.first_name} ask for timesheet')
    global users
    id = str(message.from_user.id)
    users[id] = User()
    bot.send_message(message.chat.id, 'Выберите свой класс', reply_markup=keyboard_grade)

@bot.message_handler(commands=['change'])
def change_it(comand):
    if comand.from_user.id == str(1807915254):
        @bot.message_handler(content_types=['document'])
        def handle_docs_photo(message):
            global timesheet
            try:
                chat_id = message.chat.id

                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(os.path.join(file_info.file_path))

                src = message.document.file_name
                timesheet = Help.parsing_timesheet(src)

                bot.reply_to(message, "Пожалуй, я сохраню это")
            except Exception as e:
                bot.send_message(message.chat.id, f'{e}')
    else:
        bot.send_message(comand.chat.id, 'Доступ запрещён')




@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    try:
        logger.warning(f'bot answered to {call.from_user.first_name}')
        global users, msg
        id = str(call.from_user.id)
        time.sleep(1)
        if not (users[id].grade_set and users[id].day_set):
            if not users[id].grade_set:
                if users[id].grade == '-':
                    logger.info(f'{call.from_user.first_name} from {call.data}th grade')
                    match call.data:
                        case '7':
                            time.sleep(0.5)
                            users[id].grade = call.data
                            msg = bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABC)
                        case '8':
                            time.sleep(0.5)
                            users[id].grade = call.data
                            msg = bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABCD)
                        case '9':
                            time.sleep(0.5)
                            users[id].grade = call.data
                            msg = bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABCD)
                        case '10':
                            time.sleep(0.5)
                            users[id].grade = call.data
                            msg = bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABCD)
                        case '11':
                            time.sleep(0.5)
                            users[id].grade = call.data
                            msg = bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_AB)
                        case _:
                            msg = bot.send_message(call.message.chat.id, 'Неверный выбор')
                else:
                    time.sleep(0.5)
                    if call.data == 'return':
                        bot.delete_message(call.message.chat.id, call.message.id)
                        users[id].grade = '-'
                    else:
                        users[id].grade += call.data
                        users[id].grade_set = True
                        logger.info(f'{call.from_user.first_name} from {users[id].grade} grade')
                        bot.send_message(call.message.chat.id, f'Выбран класс: {users[id].grade}')
                        msg = bot.send_message(call.message.chat.id, 'Выберите день', reply_markup=keyboard_now)
            elif not users[id].day_set:
                match call.data:
                    case 'Вчера':
                        if time.localtime(time.time()).tm_wday - 1 != 6:
                            time.sleep(0.5)
                            users[id].day_set = True
                            users[id].day = days_of_week[time.localtime(time.time()).tm_wday - 1]
                            bot.send_message(call.message.chat.id, f'Выбран день: {users[id].day}')
                        else:
                            msg = bot.send_message(call.message.chat.id, 'Неверный выбор')
                    case 'Сегодня':
                        if time.localtime(time.time()).tm_wday != 6:
                            time.sleep(0.5)
                            users[id].day_set = True
                            users[id].day = days_of_week[time.localtime(time.time()).tm_wday]
                            bot.send_message(call.message.chat.id, f'Выбран день: {users[id].day}')
                        else:
                            msg = bot.send_message(call.message.chat.id, 'Неверный выбор')
                    case 'Завтра':
                        if time.localtime(time.time()).tm_wday + 1 != 6:
                            time.sleep(0.5)
                            users[id].day_set = True
                            users[id].day = days_of_week[time.localtime(time.time()).tm_wday + 1]
                            bot.send_message(call.message.chat.id, f'Выбран день: {users[id].day}')
                        else:
                            msg = bot.send_message(call.message.chat.id, 'Неверный выбор')
                    case 'other':
                        time.sleep(0.5)
                        msg = bot.send_message(call.message.chat.id, 'Выберите день', reply_markup=keyboard_days)
                    case 'return':
                        time.sleep(0.5)
                        bot.delete_message(call.message.chat.id, call.message.id)
                        users[id].grade_set = False
                        users[id].grade = users[id].grade[0: -1]
                        match users[id].grade:
                            case '7':
                                time.sleep(0.5)
                                bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABC)
                            case '8':
                                time.sleep(0.5)
                                bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABCD)
                            case '9':
                                time.sleep(0.5)
                                bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABCD)
                            case '10':
                                time.sleep(0.5)
                                bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_ABCD)
                            case '11':
                                time.sleep(0.5)
                                bot.send_message(call.message.chat.id, 'Выберите букву', reply_markup=keyboard_AB)
                    case _:
                        users[id].day = call.data
                        users[id].day_set = True
                        logger.info(f'{call.from_user.first_name} want timesheet for {users[id].day}')
                        bot.send_message(call.message.chat.id, f'Выбран день: {users[id].day}')
            if users[id].grade_set and users[id].day_set:
                time.sleep(1.5)
                answer = ['\n']
                for i in timesheet[users[id].grade][users[id].day].keys():
                    try:
                        if len(timesheet[users[id].grade][users[id].day][i]) > 0:
                            if timesheet[users[id].grade][users[id].day][i][0] == 'Пусто':
                                answer.append(f'{counts_emoji[str(i)]}: ---')
                            else:
                                answer.append(
                                    f'{counts_emoji[str(i)]}: {timesheet[users[id].grade][users[id].day][i][0]} '
                                    f'{timesheet[users[id].grade][users[id].day][i][-1]}')
                        else:
                            answer.append(f'{counts_emoji[str(i)]}: ---')
                    except IndexError:
                        answer.append(f'{counts_emoji[str(i)]}: ---')
                answer = '\n'.join(answer)
                bot.send_message(call.message.chat.id, f'{random.choice(days_emoji[users[id].day])} '
                                                       f'{random.choice(days_emoji[users[id].day])} '
                                                       f'Расписание на {users[id].day}: '
                                                       f'{random.choice(days_emoji[users[id].day])} '
                                                       f'{random.choice(days_emoji[users[id].day])} {answer}')
    except Exception as E:
        logger.critical(f'{call.from_user.first_name} crahed the programm by {E}')
        logger.critical(f'{call.from_user.first_name} crahed the programm')
        logger.critical(E)
        sys.exit(1)

        # print(Help.timesheet[users[id].grade][users[id].day])
    # else:
    #     users[id] = User()


logger.info('Telebot started')
bot.polling(none_stop=True)
