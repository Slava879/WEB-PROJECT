import soundfile as sf
import telebot
import speech_recognition as sr
from telebot import types
import sqlite3
import datetime
from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import time
import threading

lock = threading.Lock()

language = 'ru_RU'

TOKEN = '6575996965:AAEHxx6jNmYvPOL-4S4NMXf7qBbwNOg087Q'
bot = telebot.TeleBot(TOKEN)

sp_admins = [5473624098, 1342468201]
sp_screen_dostup = [5473624098]

voice_sp_buy = ['⭐️💠  5 vm  💠⭐️', '⭐️💠  10 vm  💠⭐️', '⭐️💠  20 vm  💠⭐️',
                '⭐️💠  30 vm  💠⭐️', '⭐️💠  50 vm  💠⭐️', '⭐️💠  100 vm  💠⭐️',
                '⭐️💠  1000 vm  💠⭐️']
time_sp_buy = ['⭐️💠  1 день  💠⭐️', '⭐️💠  1 неделя  💠⭐️', '⭐️💠  2 недели  💠⭐️',
               '⭐️💠  1 месяц  💠⭐️', '⭐️💠  3 месяца  💠⭐️', '⭐️💠  6 месяцев  💠⭐️',
               '⭐️💠  12 месяцев  💠⭐️']
sl_buy = {'⭐️💠  5 vm  💠⭐️': 20, '⭐️💠  10 vm  💠⭐️': 30, '⭐️💠  20 vm  💠⭐️': 50,
          '⭐️💠  30 vm  💠⭐️': 60, '⭐️💠  50 vm  💠⭐️': 75, '⭐️💠  100 vm  💠⭐️': 100,
          '⭐️💠  1000 vm  💠⭐️': 500,
          '⭐️💠  1 день  💠⭐️': 15, '⭐️💠  1 неделя  💠⭐️': 30, '⭐️💠  2 недели  💠⭐️': 50,
          '⭐️💠  1 месяц  💠⭐️': 90, '⭐️💠  3 месяца  💠⭐️': 250, '⭐️💠  6 месяцев  💠⭐️': 450,
          '⭐️💠  12 месяцев  💠⭐️': 800}
sl_chet = {'⭐️💠  5 vm  💠⭐️': 5, '⭐️💠  10 vm  💠⭐️': 10, '⭐️💠  20 vm  💠⭐️': 20,
           '⭐️💠  30 vm  💠⭐️': 30, '⭐️💠  50 vm  💠⭐️': 50, '⭐️💠  100 vm  💠⭐️': 100,
           '⭐️💠  1000 vm  💠⭐️': 1000,
           '⭐️💠  1 день  💠⭐️': 1, '⭐️💠  1 неделя  💠⭐️': 7,
           '⭐️💠  2 недели  💠⭐️': 14, '⭐️💠  1 месяц  💠⭐️': 30,
           '⭐️💠  3 месяца  💠⭐️': 92, '⭐️💠  6 месяцев  💠⭐️': 183,
           '⭐️💠  12 месяцев  💠⭐️': 365}

sl_language = {'Русский': 'ru', 'Английский': 'en', 'Африкаанс': 'af', 'Албанский': 'sq', 'Амхарский': 'am',
               'Арабский': 'ar', 'Армянский': 'hy', 'Азербайджанский': 'az', 'Баскский': 'eu', 'Белорусский': 'be',
               'Бенгальский': 'bn', 'Боснийский': 'bs', 'Болгарский': 'bg', 'Каталанский': 'ca', 'Себуано': 'ceb',
               'Китайский': 'ny', 'Корсиканец': 'co', 'Хорватский': 'hr', 'Чешский': 'cs', 'Датский': 'da',
               'Голландский': 'nl', 'Эсперанто': 'eo', 'Эстонский': 'et', 'Филиппинский': 'tl', 'Финский': 'fi',
               'Французский': 'fr', 'Фризский': 'fy', 'Галисийский': 'gl', 'Грузинский': 'ka', 'Немецкий': 'de',
               'Греческий': 'el', 'Гуджарати': 'gu', 'Гаитянский Креольский ': 'ht', 'Хауса': 'ha', 'Гавайский': 'haw',
               'Иврит': 'iw', 'Хинди': 'hi', 'Хмонг': 'hmn', 'Венгерский': 'hu', 'Исландский': 'is', 'Игбо': 'ig',
               'Индонезийский': 'id', 'Ирландский': 'ga', 'Итальянский': 'it', 'Японский': 'ja', 'Яванский': 'jw',
               'Каннада': 'kn', 'Казахский': 'kk', 'Кхмерский': 'km', 'Корейский': 'ko', 'Курдский (курманджи) ': 'ku',
               'Кыргызский': 'ky', 'Лаосский': 'lo', 'Латинский': 'la', 'Латышский': 'lv', 'Литовский': 'lt',
               'Люксембургский': 'lb', 'Македонский': 'mk', 'Малагасийский': 'mg', 'Малайский': 'ms', 'Малаялам': 'ml',
               'Мальтийский': 'mt', 'Маори': 'mi', 'Маратхи': 'mr', 'Монгольский': 'mn', 'Мьянма (бирманский) ': 'my',
               'Непальский': 'ne', 'Норвежский': 'no', 'Одия': 'or', 'Пушту': 'ps', 'Персидский': 'fa',
               'Полировать': 'pl', 'Португальский': 'pt', 'Пенджабский': 'pa', 'Румынский': 'ro', 'Самоанец': 'sm',
               'Шотландский Гэльский ': 'gd', 'Сербский': 'sr', 'Сесото': 'st', 'Шона': 'sn', 'Синдхи': 'sd',
               'Сингальский': 'si', 'Словацкий': 'sk', 'Словенский': 'sl', 'Сомалийский': 'so', 'Испанский': 'es',
               'Суданский': 'su', 'Суахили': 'sw', 'Шведский': 'sv', 'Таджикский': 'tg', 'Тамильский': 'ta',
               'Телугу': 'te', 'Тайский': 'th', 'Турецкий': 'tr', 'Украинский': 'uk', 'Урду': 'ur', 'Уйгурский': 'ug',
               'Узбекский': 'uz', 'Вьетнамский': 'vi', 'Валлийский': 'cy', 'Коса': 'xh', 'Идиш': 'yi', 'Йоруба': 'yo',
               'Зулусский': 'zu'}
sp_language = ['Русский', 'Английский', 'Африкаанс', 'Албанский', 'Амхарский', 'Арабский', 'Армянский',
               'Азербайджанский', 'Баскский', 'Белорусский', 'Бенгальский', 'Боснийский', 'Болгарский',
               'Каталанский', 'Себуано', 'Китайский', 'Корсиканец', 'Хорватский', 'Чешский', 'Датский',
               'Голландский', 'Эсперанто', 'Эстонский', 'Филиппинский', 'Финский', 'Французский', 'Фризский',
               'Галисийский', 'Грузинский', 'Немецкий', 'Греческий', 'Гуджарати', 'Гаитянский Креольский ', 'Хауса',
               'Гавайский', 'Иврит', 'Хинди', 'Хмонг', 'Венгерский', 'Исландский', 'Игбо', 'Индонезийский',
               'Ирландский', 'Итальянский', 'Японский', 'Яванский', 'Каннада', 'Казахский', 'Кхмерский',
               'Корейский', 'Курдский (курманджи) ', 'Кыргызский', 'Лаосский', 'Латинский', 'Латышский',
               'Литовский', 'Люксембургский', 'Македонский', 'Малагасийский', 'Малайский', 'Малаялам',
               'Мальтийский', 'Маори', 'Маратхи', 'Монгольский', 'Мьянма (бирманский) ', 'Непальский',
               'Норвежский', 'Одия', 'Пушту', 'Персидский', 'Полировать', 'Португальский', 'Пенджабский',
               'Румынский', 'Самоанец', 'Шотландский Гэльский ', 'Сербский', 'Сесото', 'Шона', 'Синдхи',
               'Сингальский', 'Словацкий', 'Словенский', 'Сомалийский', 'Испанский', 'Суданский', 'Суахили',
               'Шведский', 'Таджикский', 'Тамильский', 'Телугу', 'Тайский', 'Турецкий', 'Украинский', 'Урду',
               'Уйгурский', 'Узбекский', 'Вьетнамский', 'Валлийский', 'Коса', 'Идиш', 'Йоруба', 'Зулусский']
sp_flag = [' 🇷🇺', ' 🇺🇸', ' 🇿🇦', ' 🇦🇱', ' 🇪🇹', ' 🇸🇦', ' 🇦🇲', ' 🇦🇿', ' 🇪🇸', ' 🇧🇾', ' 🇧🇩', ' 🇧🇦',
           ' 🇧🇬', ' 🇪🇸', ' 🇵🇭', ' 🇨🇳', ' 🇫🇷', ' 🇭🇷', ' 🇨🇿', ' 🇩🇰', ' 🇳🇱', ' 🌐', ' 🇪🇪',
           ' 🇵🇭', ' 🇫🇮', ' 🇫🇷', ' 🇳🇱', ' 🇪🇸', ' 🇬🇪', ' 🇩🇪', ' 🇬🇷', ' 🇮🇳', ' 🇭🇹', ' 🇳🇬',
           ' 🇺🇸', ' 🇮🇱', ' 🇮🇳', ' 🌐', ' 🇭🇺', ' 🇮🇸', ' 🇳🇬', ' 🇮🇩', ' 🇮🇪', ' 🇮🇹', ' 🇯🇵',
           ' 🇮🇩', ' 🇮🇳', ' 🇰🇿', ' 🇰🇭', ' 🇰🇷', ' 🇮🇶', ' 🇰🇬', ' 🇱🇦', ' 🌐', ' 🇱🇻', ' 🇱🇹',
           ' 🇱🇺', ' 🇲🇰', ' 🇲🇬', ' 🇲🇾', ' 🇮🇳', ' 🇲🇹', ' 🇳🇿', ' 🇮🇳', ' 🇲🇳', ' 🇲🇲',
           ' 🇳🇵', ' 🇳🇴', ' 🇮🇳', ' 🇦🇫', ' 🇮🇷', ' 🇵🇱', ' 🇵🇹', ' 🇮🇳', ' 🇷🇴', ' 🇼🇸', ' 🌐',
           ' 🇷🇸', ' 🇱🇸', ' 🇿🇼', ' 🇵🇰', ' 🇱🇰', ' 🇸🇰', ' 🇸🇮', ' 🇸🇴', ' 🇪🇸', ' 🇸🇩',
           ' 🇰🇪', ' 🇸🇪', ' 🇹🇯', ' 🇱🇰', ' 🇮🇳', ' 🇹🇭', ' 🇹🇷', ' 🇺🇦', ' 🇵🇰',
           ' 🇨🇳', ' 🇺🇿', ' 🇻🇳', ' 🏴', ' 🇿🇦', ' 🌐', ' 🇳🇬', ' 🇿🇦']

dec = ['⭐️💠 ', ' 💠⭐️', '✅', '❌']


def recognise(filename):
    sinput = filename
    r = sr.Recognizer()
    harvard = sr.AudioFile(sinput)
    with harvard as source:
        audio = r.record(source)
    out = r.recognize_google(audio, language="ru-RU,en-US")
    return out


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    with lock:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('images_pay/new_screen.png', 'wb') as new_file:
            new_file.write(downloaded_file)
        new_file.close()
        for id_admin in sp_screen_dostup:
            bot.send_message(id_admin, f'<b>{dec[0]}✅{message.chat.id} @{message.chat.username}✅{dec[1]}</b>',
                             parse_mode='html')
            bot.send_photo(id_admin, open(f"images_pay/new_screen.png", 'rb'))

        bot.send_message(message.chat.id,
                         f"<b>{dec[0]}✅Скриншот успешно отправлен, платеж будет зачислен в течение 24 часов✅{dec[1]}"
                         f"</b>", parse_mode='html')


@bot.message_handler(commands=['check'])
def ch(message):
    connect = sqlite3.connect('voice_bd.sqlite', check_same_thread=False)
    cursor = connect.cursor()
    if message.chat.id in sp_screen_dostup:
        if len(message.text.split()) > 1:
            if message.text.split()[1] == 'info':
                text = ''
                for i in cursor.execute("SELECT * FROM oplata").fetchall():
                    zn = ''
                    if str(i[2]) == 'True':
                        zn += f'{dec[2]} '
                    else:
                        zn += ' ⌛'
                    text += f'<b>{dec[0]}{i[0]} {i[1]} {zn} {i[3]}</b>\n'
                bot.send_message(message.chat.id, text, parse_mode='html')
            elif message.text.split()[1].isnumeric():
                flag = False
                for i in cursor.execute("SELECT number FROM oplata").fetchall():
                    if str(i[0]) == str(message.text.split()[1]):
                        flag = True
                        break
                if len(message.text.split()) == 2:
                    if flag:
                        text = cursor.execute("SELECT * FROM oplata WHERE number=?", (
                            message.text.split()[1],)).fetchall()[0]
                        deyst = '⌛ Ожидает оплаты... ⌛'
                        if str(text[2]) == 'True':
                            deyst = f'{dec[2]} Оплачен! {dec[2]}'
                        bot.send_message(message.chat.id, f'''<b>{dec[0]}Информация о чеке{dec[1]}
{dec[0]}Номер: {text[0]}
{dec[0]}Сумма: {text[1]}
{dec[0]}id: {text[3]}
{dec[0]}Действие: {deyst} </b>''', parse_mode='html')
                    else:
                        bot.send_message(message.chat.id, f'<b>{dec[0]}{dec[3]}Чек не найден!{dec[3]}{dec[1]}</b>',
                                         parse_mode='html')
                elif len(message.text.split()) == 4:
                    if not flag:
                        cursor.execute(
                            """INSERT OR IGNORE INTO oplata (number, pay, flag, id) VALUES (?, ?, ?, ?)""", (int(
                                message.text.split()[1]), message.text.split()[2], 'False', message.text.split()[3]))
                        connect.commit()
                        bot.send_message(message.chat.id, f'<b>{dec[0]} ⌛ Ожидает оплаты... ⌛ {dec[1]}</b>',
                                         parse_mode='html')
                    else:
                        if str(cursor.execute("SELECT flag FROM oplata WHERE number=?", (
                                message.text.split()[1], )).fetchall()[0][0]) == 'False':
                            bot.send_message(message.chat.id, f'<b>{dec[0]} ⌛ Ожидает оплаты... ⌛ {dec[1]}</b>',
                                             parse_mode='html')
                        elif str(cursor.execute("SELECT flag FROM oplata WHERE number=?", (
                                message.text.split()[1], )).fetchall()[0][0]) == 'True':
                            bot.send_message(message.chat.id,
                                             f'<b>{dec[0]}{dec[2]}Чек уже оплачен!{dec[2]}{dec[1]}</b>',
                                             parse_mode='html')
                elif len(message.text.split()) == 5:
                    if not flag:
                        bot.send_message(message.chat.id, f'<b>{dec[0]}{dec[3]}Чек не найден!{dec[3]}{dec[1]}</b>',
                                         parse_mode='html')
                    else:
                        if message.text.split()[2].isnumeric() and message.text.split()[3] in ['True', 'False']:
                            if message.text.split()[3] == 'True':
                                cursor.execute("UPDATE oplata SET flag=? WHERE number=?",
                                               (str('True'), (str(message.text.split()[1]))))
                                connect.commit()
                                balance = int(cursor.execute("SELECT balance FROM users WHERE id=?",
                                                             (message.text.split()[4],)).fetchall()[0][0])
                                ref_user = cursor.execute("SELECT ref_link_users FROM users WHERE id=?",
                                                          (message.text.split()[4],)).fetchall()[0][0]
                                cursor.execute("UPDATE users SET balance=? WHERE id=?",
                                               (str(balance + int(message.text.split()[2])),
                                                (str(message.text.split()[4]))))
                                connect.commit()
                                if len(str(ref_user)) != 0 and str(ref_user) != 'None':
                                    ref_balance = int(cursor.execute("SELECT balance FROM users WHERE id=?",
                                                                     (ref_user,)).fetchall()[0][0])
                                    cursor.execute("UPDATE users SET balance=? WHERE id=?",
                                                   (str(ref_balance + int(int(message.text.split()[2]) * 0.25)),
                                                    (str(ref_user))))
                                    connect.commit()
                                    bot.send_message(ref_user,
                                                     f'<b>{dec[0]}{dec[2]}Вы получили 25% от '
                                                     f'пополнения реферала!{dec[2]}{dec[1]}</b>',
                                                     parse_mode='html')
                                bot.send_message(message.chat.id,
                                                 f'<b>{dec[0]}{dec[2]}Выплата прошла успешно!{dec[2]}{dec[1]}</b>',
                                                 parse_mode='html')
                                bot.send_message(message.text.split()[4],
                                                 f'<b>{dec[0]}{dec[2]}Вам выплачен чек!{dec[2]}{dec[1]}</b>',
                                                 parse_mode='html')

                            elif message.text.split()[3] == 'False':
                                cursor.execute("UPDATE oplata SET flag=? WHERE number=?",
                                               (str('False'), (str(message.text.split()[1]))))
                                connect.commit()
                                bot.send_message(message.chat.id,
                                                 f'<b>{dec[0]}{dec[3]}Чек отклонен!{dec[3]}{dec[1]}</b>',
                                                 parse_mode='html')
                                bot.send_message(message.text.split()[4],
                                                 f'<b>{dec[0]}{dec[3]}Чек отклонен!{dec[3]}{dec[1]}</b>',
                                                 parse_mode='html')
                            else:
                                bot.send_message(message.chat.id, f'<b>❗️ Неверный формат ввода ❗️</b>',
                                                 parse_mode='html')
                        else:
                            bot.send_message(message.chat.id, f'<b>❗️ Неверный формат ввода ❗️</b>',
                                             parse_mode='html')
                else:
                    bot.send_message(message.chat.id, f'<b>❗️ Неверный формат ввода ❗️</b>', parse_mode='html')
            else:
                bot.send_message(message.chat.id, f'<b>❗️ Неверный формат ввода ❗️</b>', parse_mode='html')
        else:
            bot.send_message(message.chat.id, f'''<b>❗️ Неверный формат ввода ❗️
{dec[0]}1) /check number - информация о чеке
{dec[0]}2) /check number summa id - занести информацию о чеке
{dec[0]}3) /check number summa flag id - выплатить/отклонить
</b>''', parse_mode='html')
    else:
        bot.send_message(message.chat.id, f'<b>🔐 У вас недостаточно прав, чтобы использовать эту команду! 🔐 </b>!',
                         parse_mode='html')

    connect.close()


@bot.message_handler(commands=['buy'])
def buy(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(f'{dec[0]}🗣 VM 🗣{dec[1]}', f'{dec[0]}👑 TIME 👑{dec[1]}')
    bot.send_message(message.chat.id, f'''<b>{dec[0]}Выберите категорию:{dec[1]}
{dec[0]} 1) Количество переводов голосовых сообщений в текст. (название тарифа: VM)
{dec[0]} 2) Безлимитное количество переводов на ограниченное время. (название тарифа: TIME)
</b>''', parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    try:
        with lock:
            time_flag = True
            connect = sqlite3.connect('voice_bd.sqlite', check_same_thread=False)
            cursor = connect.cursor()
            vm = cursor.execute("SELECT VM FROM users WHERE id=?", (str(message.chat.id),)).fetchall()[0][0]
            if str(cursor.execute("SELECT sub FROM users WHERE id=?", (str(message.chat.id),)).fetchall()[0][
                       0]) == 'NO SUB':
                date1 = 'подписка не активирована!'
            else:
                date = cursor.execute("SELECT TIME FROM users WHERE id=?", (str(message.chat.id),)).fetchall()[0][0]
                dt = date.split()[0].split('-')
                year, mounth, day = int(dt[0]), int(dt[1]), int(dt[2])
                date = datetime.datetime(year, mounth, day)
                date1 = date - datetime.datetime.now()
                if date < datetime.datetime.now():
                    if int(vm) == 0:
                        date1 = 'подписка не активирована!'
                        cursor.execute("UPDATE users SET sub=? WHERE id=?", (str('NO SUB'), (str(message.chat.id))))
                        connect.commit()
                    else:
                        time_flag = False

            if date1 == 'подписка не активирована!':
                bot.send_message(message.chat.id, '❗️ <b>подписка не активирована! /sub /buy</b> ❗️',
                                 parse_mode='html')
            else:
                file_name_full = "./voice/new_file.ogg"
                file_info = bot.get_file(message.voice.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(file_name_full, 'wb') as new_file:
                    new_file.write(downloaded_file)
                data, samplerate = sf.read(file_name_full)
                sf.write('new_file.wav', data, samplerate)
                text = recognise('new_file.wav')
                if not time_flag:
                    cursor.execute("UPDATE users SET VM=? WHERE id=?", (str(int(vm - 1)), (str(message.chat.id))))
                    connect.commit()
                cursor.execute("UPDATE users SET voice_text=? WHERE id=?", (str(text), (str(message.chat.id))))
                connect.commit()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add('/start', 'получить аудио')
                n = 0
                for _ in range(len(sp_language) // 2):
                    markup.add(f'{sp_flag[n]}{sp_language[n]}{sp_flag[n]}',
                               f'{sp_flag[n + 1]}{sp_language[n + 1]}{sp_flag[n + 1]}')
                    n += 2
                if len(sp_language) % 2 == 1:
                    markup.add(f'{dec[0]}{sp_flag[n]}{sp_language[-1]}{sp_flag[n]}{dec[1]}')
                bot.send_message(message.chat.id, f'<b>{dec[0]}{dec[2]} {str(text)} {dec[2]}{dec[1]}</b>',
                                 parse_mode='html')
                bot.send_message(message.chat.id, f'<b>{dec[0]}{dec[2]} Вы можете перевести текст на другой язык!'
                                                  f' {dec[2]}{dec[1]}</b>',
                                 parse_mode='html', reply_markup=markup)
                print(message.chat.id, message.from_user.username, message.from_user.first_name, text)

            connect.close()

    except Exception as ex:
        print(ex.__class__.__name__)
        bot.send_message(message.chat.id, f'<b>{dec[0]}{dec[3]}сообщение не распознано! ({str(ex.__class__.__name__)})'
                                          f'{dec[3]}{dec[1]}</b>', parse_mode='html')


@bot.message_handler(commands=['start'])
def start(message):
    connect = sqlite3.connect('voice_bd.sqlite', check_same_thread=False)
    cursor = connect.cursor()
    try:
        avtorizacia = False
        for i in cursor.execute("SELECT id FROM users").fetchall():
            if str(i[0]) == str(message.chat.id):
                avtorizacia = True
                break
        if not avtorizacia:
            cursor.execute(
                """INSERT OR IGNORE INTO users
                 (id, sub, username, balance, VM, TIME) VALUES (?, ?, ?, ?, ?, ?)""", (str(
                    message.chat.id), str('SUB'), str(message.from_user.username), 0, 5, str(datetime.datetime.now())))
            connect.commit()
            bot.send_message(message.chat.id, f'''<b>{dec[0]}{dec[2]} Вам выдано 5 пробных переводов 
            голосовых ссобщений в текст! {dec[2]}{dec[1]} </b>''', parse_mode='html')
        if len(message.text.split()) == 2:
            cursor.execute("UPDATE users SET ref_link_users=? WHERE id=?",
                           (str(message.text.split()[1]), (str(message.chat.id))))
            connect.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('/start', '/buy', '/sub')
        markup.add('/i', '/help')
        bot.send_message(message.chat.id, f'<b>{dec[0]}Приветствую тебя в боте, присылай голосовое сообщения,'
                                          f' а я переведу его тебе в текст!{dec[1]}</b>', parse_mode='html',
                         reply_markup=markup)
    except Exception as ex:
        print(ex.__class__.__name__)
        bot.send_message(message.chat.id, f'<b>{dec[0]}{dec[3]}Возникла техническая ошибка, попробуйте позже!'
                                          f' ({str(ex.__class__.__name__)})'
                                          f'{dec[3]}{dec[1]}</b>', parse_mode='html')
        bot.send_message(5473624098, f'<b>{dec[0]}{dec[3]}У пользователя {message.chat.id} возникла ошибка '
                                     f'при входе /start ({str(ex.__class__.__name__)}){dec[3]}{dec[1]}</b>',
                         parse_mode='html')
    connect.close()


@bot.message_handler(commands=['play'])
def play(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/start')
    markup.add(types.KeyboardButton(f'{dec[0]} PLAY {dec[1]}', web_app=types.WebAppInfo(
        'https://play-for-fun.ucoz.net/')))
    bot.send_message(message.chat.id, f'<b>{dec[0]}Время азарта! '
                                      f'ВАЖНО: игровой баланс - монетки, неимеющие никакого отношения к'
                                      f'настоящим денежным средствам!!! </b>{dec[1]}',
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['all'])
def al(message):
    if message.chat.id == 5473624098:
        if len(message.text.split()) > 1:
            connect = sqlite3.connect('voice_bd.sqlite', check_same_thread=False)
            cursor = connect.cursor()
            mess = f"<b>⚜️ {message.text.replace('/all', '')} ⚜️</b>"
            for i in cursor.execute("SELECT id FROM users").fetchall():
                print(i[0])
                bot.send_message(int(i[0]), mess, parse_mode='html')
            connect.close()
        else:
            bot.send_message(message.chat.id, f'<b>❗️ Неверный формат ввода ❗️</b>',
                             parse_mode='html')
    else:
        bot.send_message(message.chat.id, f'<b>🔐 У вас недостаточно прав, чтобы использовать эту команду! 🔐 </b>!',
                         parse_mode='html')


@bot.message_handler(commands=['users'])
def users(message):
    if message.chat.id == 5473624098:
        mess = ''
        connect = sqlite3.connect('voice_bd.sqlite', check_same_thread=False)
        cursor = connect.cursor()
        for i in cursor.execute("SELECT id, username FROM users").fetchall():
            sub = cursor.execute("SELECT sub FROM users WHERE id=?", (str(i[0]),)).fetchall()[0][0]
            vm = cursor.execute("SELECT VM FROM users WHERE id=?", (str(i[0]),)).fetchall()[0][0]
            ref_user = \
                cursor.execute("SELECT ref_link_users FROM users WHERE id=?", (str(i[0]),)).fetchall()[0][0]
            if str(sub) != 'NO SUB':
                date = cursor.execute("SELECT TIME FROM users WHERE id=?", (str(i[0]),)).fetchall()[0][0]
                dt = date.split()[0].split('-')
                year, mounth, day = int(dt[0]), int(dt[1]), int(dt[2])
                date = datetime.datetime(year, mounth, day)
                date1 = date - datetime.datetime.now()
                if date < datetime.datetime.now():
                    if int(vm) == 0:
                        date1 = 'подписка не активирована!'
                        cursor.execute("UPDATE users SET sub=? WHERE id=?", (str('NO SUB'), (str(i[0]))))
                        connect.commit()
                    else:
                        date1 = '0:00:00'
            else:
                date1 = 'подписка не активирована!'
            balance = cursor.execute("SELECT balance FROM users WHERE id=?", (str(i[0]),)).fetchall()[0][0]
            mess += f'{dec[2]}{dec[0]}️ <b>{i[0]}</b>\t@{i[1]}️\n⏳ TIME: {date1} ⏳\n' \
                    f' 🗣 VM: {vm} 🗣\n 💰 Баланс: {balance} 💰\n 🌐Реферер: {ref_user}🌐\n\n'
        bot.send_message(5473624098, mess, parse_mode='html')
        connect.close()
    else:
        bot.send_message(message.chat.id, f'<b>🔐 У вас недостаточно прав, чтобы использовать эту команду! 🔐 </b>',
                         parse_mode='html')


@bot.message_handler(commands=['i'])
def i(message):
    connect = sqlite3.connect('voice_bd.sqlite', check_same_thread=False)
    cursor = connect.cursor()

    balance = cursor.execute("SELECT balance FROM users WHERE id=?", (str(message.chat.id),)).fetchall()[0][0]
    vm = cursor.execute("SELECT VM FROM users WHERE id=?", (str(message.chat.id),)).fetchall()[0][0]
    ref_link = cursor.execute("SELECT ref_link FROM users WHERE id=?", (str(message.chat.id),)).fetchall()[0][0]
    ref_user = cursor.execute("SELECT ref_link_users FROM users WHERE id=?", (str(message.chat.id),)).fetchall()[0][0]
    if str(cursor.execute("SELECT sub FROM users WHERE id=?", (str(message.chat.id),)).fetchall()[0][
               0]) == 'NO SUB':
        date1 = 'подписка не активирована!'
    else:
        date = cursor.execute("SELECT TIME FROM users WHERE id=?", (str(message.chat.id),)).fetchall()[0][0]
        dt = date.split()[0].split('-')
        year, mounth, day = int(dt[0]), int(dt[1]), int(dt[2])
        date = datetime.datetime(year, mounth, day)
        date1 = date - datetime.datetime.now()
        if date < datetime.datetime.now():
            if int(vm) == 0:
                date1 = 'подписка не активирована!'
                cursor.execute("UPDATE users SET sub=? WHERE id=?", (str('NO SUB'), (str(message.chat.id))))
                connect.commit()
            else:
                date1 = '0:00:00'
    bot.send_message(message.chat.id, f'''<b>{dec[0]} id - {message.chat.id}
{dec[0]}⏳ Оставшееся время подписки: {date1} ⏳
{dec[0]}🗣 Оставшееся количество VM: {vm} 🗣
{dec[0]}💸 На вашем балансе: {balance} монеток! 💸
{dec[0]}🌐 Ваша реферальная ссылка: 🌐 {ref_link}
{dec[0]}⚜️ Ваш Реферер: {ref_user}  ⚜️
{dec[0]}👑 За монетки вы можете купить подписку /buy в любой момент 👑
{dec[0]}{dec[3]} Деньги вывести нельзя! {dec[3]}
{dec[0]}Информация о подписке /sub</b>
''', parse_mode='html')
    connect.close()


@bot.message_handler(commands=['ban'])
def ban(message):
    if message.chat.id in sp_admins:
        if len(message.text.split()) == 2:
            if message.text.split()[1].isnumeric():
                if int(message.text.split()[1]) != 5473624098 or message.chat.id == 5473624098:
                    need = False
                    connect = sqlite3.connect('voice_bd.sqlite', check_same_thread=False)
                    cursor = connect.cursor()
                    for i in cursor.execute("SELECT id FROM users").fetchall():
                        if str(i[0]) == str(message.text.split()[1]):
                            need = True
                            break
                    if need:
                        cursor.execute("UPDATE users SET sub=? WHERE id=?", (str('NO SUB'), (str(
                            message.text.split()[1]))))
                        connect.commit()
                        cursor.execute("UPDATE users SET VM=? WHERE id=?", (str(0), (str(
                            message.text.split()[1]))))
                        connect.commit()
                        cursor.execute("UPDATE users SET TIME=? WHERE id=?", (str(datetime.datetime.now()), (str(
                            message.text.split()[1]))))
                        connect.commit()
                        bot.send_message(message.chat.id, f'✅ У пользователя <b>{message.text.split()[1]} </b> '
                                                          f'была снята подписка! ✅', parse_mode='html')
                        if message.chat.id != 5473624098:
                            bot.send_message(5473624098, f'✅ У пользователя <b>{message.text.split()[1]} </b>'
                                                         f' была снята подписка! ✅ (подписку забрал'
                                                         f' {message.chat.id})', parse_mode='html')
                    else:
                        bot.send_message(message.chat.id, f'❗️ Пользователь <b> {message.text.split()[1]} </b> '
                                                          f'не найден! ❗️', parse_mode='html')
                    connect.close()
                else:
                    bot.send_message(message.chat.id, f'<b>🔐 У вас не достаточно прав! 🔐</b>!', parse_mode='html')
            else:
                bot.send_message(message.chat.id, f'<b>❗️ Неверный формат ввода ❗️</b>!',
                                 parse_mode='html')
        else:
            bot.send_message(message.chat.id, f'<b>❗️ Неверный формат ввода ❗️</b>!',
                             parse_mode='html')
    else:
        bot.send_message(message.chat.id, f'<b>🔐 У вас недостаточно прав, чтобы использовать эту команду! 🔐 </b>!',
                         parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):
    sp_help = ['/start - перезапустить бота', '/help - вызвать это сообщение', '/i - информация об аккаунте',
               '/sub - информация  подписках', '/buy - купить подписку', '/id - посмотреть свой id',
               '/ref_link_create - создать реферальную ссылку (подробнее /ref)', '/play - играть в мини-игры']
    sp_help_admin = ['/ban - забрать подписку (обнуление VM и TIME)', '/info - инфо о боте']
    sp_help_creator = ['/users - просмотр всех пользователей', '/all - рассылка', '/check - управление чеками']
    text = ''
    for i in sp_help:
        text += f'<b>{dec[0]}{i}</b>\n'
    if message.chat.id in sp_admins:
        text += f'{dec[0]} <b>🔴 АДМИНИСТРАТОРАМ: 🔴</b>\n'
        for i in sp_help_admin:
            text += f'<b>{dec[0]}{i}</b>\n'
    if message.chat.id == 5473624098:
        text += f'{dec[0]} <b>🟣 СОЗДАТЕЛЮ (СОАВТОРАМ): 🟣</b>\n'
        for i in sp_help_creator:
            text += f'<b>{dec[0]}{i}</b>\n'
    bot.send_message(message.chat.id, text, parse_mode='html')


@bot.message_handler(commands=['info'])
def info(message):
    if message.chat.id in sp_admins:
        connect = sqlite3.connect('voice_bd.sqlite', check_same_thread=False)
        cursor = connect.cursor()
        user_count = 0
        for _ in cursor.execute("SELECT id FROM users").fetchall():
            user_count += 1
        bot.send_message(message.chat.id, f'''<b>💠⭐️ Сейчас в боте: {user_count} пользователей!💠⭐️</b>''',
                         parse_mode='html')
        connect.close()


@bot.message_handler(commands=['sub'])
def sub(message):
    bot.send_message(message.chat.id, f'''{dec[0]} Покупка подписки! {dec[1]}
{dec[0]} 💰Чтобы купить подписку: 💰
{dec[0]} 💳1) Оплатите по ссылке  /pay
💸 Любую сумму 💸 и пришлите боту скриншот чека 
(он придет на указанную вами почту при оплате) 💳
{dec[0]}  ✅ 2) Ожидайте подтверждения оплаты (это может занять до 24 часов) ✅
{dec[0]} 💰 После подтверждения на ваш баланс зачислится сумма в монетках (посмотреть баланс: /i),
 после чего за эти монетки вы сможете купить подписку (подробнее о покупке подписке /buy) 💰
{dec[0]}❗ ВАЖНО! ❗
{dec[0]} 🌓 1) Если вы пришлете fake квитанцию, то вы получите бан! 🌓
{dec[0]} ⌛ 2) Если монетки не пришли за 24 часа в момента оплаты, обратитесь в поддержку /sub_help! ⌛
{dec[0]} ⌛ 3) Подписка заканчивается в 0:00:00 
(т. е. если вы купили подписку в 23:00, то у вас останется 1 час пользования) ⌛
{dec[0]} ⌛ 4) Посмотреть время бота (по нему 0:00:00 снимается подписка) /time_bot! ⌛
''', parse_mode='html')


@bot.message_handler(commands=['id'])
def id_users(message):
    bot.send_message(message.chat.id, f'<b>{dec[0]}Ваш id: {message.chat.id}{dec[1]}</b>', parse_mode='html')


@bot.message_handler(commands=['ref_link_create'])
def ref_link_create(message):
    connect = sqlite3.connect('voice_bd.sqlite', check_same_thread=False)
    cursor = connect.cursor()

    cursor.execute("UPDATE users SET ref_link=? WHERE id=?",
                   (str(f'https://t.me/voice_544879_bot?start={message.chat.id}'), (str(message.chat.id))))
    connect.commit()

    bot.send_message(message.chat.id,
                     f'<b>{dec[0]}{dec[2]}Ваша реферальная ссылка: '
                     f'https://t.me/voice_544879_bot?start={message.chat.id}'
                     f' {dec[2]}{dec[1]}</b>', parse_mode='html')

    connect.close()


@bot.message_handler(commands=['time_bot'])
def time_bot(message):
    bot.send_message(message.chat.id, f'<b>{dec[0]}{dec[2]} {datetime.datetime.now()} '
                                      f'{dec[2]}{dec[0]}</b>', parse_mode='html')


@bot.message_handler(commands=['sub_help'])
def sub_help(message):
    bot.send_message(message.chat.id,
                     f'<b>{dec[0]}{dec[2]} Вы обратились к поддержке, ожидайте ее решения '
                     f'(с вами могут связаться, ВАЖНО: наша поддержка не будет запрашивать никаких личных данных) '
                     f'{dec[2]}{dec[1]}</b>', parse_mode='html')
    for admin in sp_admins:
        bot.send_message(admin,
                         f'<b>{dec[0]} Пользователь {message.chat.id} запрашивает оплату чека! {dec[1]}</b>',
                         parse_mode='html')


@bot.message_handler(commands=['ref'])
def ref(message):
    bot.send_message(message.chat.id,
                     f'<b>{dec[0]}Вы будете получать 25% с каждого пополнения тех пользователей,'
                     f' которые перешли по вашей реферальной ссылке{dec[1]}</b>', parse_mode='html')


@bot.message_handler(commands=['pay'])
def play(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/start')
    markup.add(types.KeyboardButton(f'{dec[0]}💰 PAY 💰{dec[1]}', web_app=types.WebAppInfo(
        'https://pay.ucoz.net/')))
    bot.send_message(message.chat.id, f'<b>{dec[0]}Для проведения оплаты нажмите {dec[0]}💰 PAY 💰{dec[1]}{dec[1]}</b>',
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    with lock:
        connect = sqlite3.connect('voice_bd.sqlite', check_same_thread=False)
        cursor = connect.cursor()
        if message.text == f'{dec[0]}🗣 VM 🗣{dec[1]}':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('/start')
            text = ''
            sp_voice = [
                '5 20',
                '10 30',
                '20 50',
                '30 60',
                '50 75',
                '100 100',
                '1000 500'

            ]
            sp_control = [20, 50, 1000]
            sp_name = ['Маленькие тарифы:', 'Средние тарифы:', 'Большие тарифы:']
            sp_add = []
            for i in range(3):
                name = sp_name[i]
                sp_add = []
                if i == 0:
                    text += f'<b>{dec[0]}🟥 {name} 🟥</b>\n'
                elif i == 1:
                    text += f'<b>{dec[0]}🟧 {name} 🟧</b>\n'
                elif i == 2:
                    text += f'<b>{dec[0]}🟩 {name} 🟩</b>\n'
                for voice in sp_voice:
                    if i == 0:
                        if int(voice.split()[0]) <= sp_control[i]:
                            text += f'<b>{dec[0]} {voice.split()[0]} vm - {voice.split()[1]} монеток' \
                                    f' ({int(voice.split()[1]) / int(voice.split()[0])} монет. за 1)</b>\n'
                    elif i > 0:
                        if sp_control[i - 1] < int(voice.split()[0]) <= sp_control[i]:
                            text += f'<b>{dec[0]} {voice.split()[0]} vm - {voice.split()[1]} монеток' \
                                    f' ({int(voice.split()[1]) / int(voice.split()[0])} монет. за 1)</b>\n'
                    sp_add.append(f'{dec[0]} {voice.split()[0]} vm {dec[1]}')
            markup.add(*sp_add)
            bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup)
        elif message.text == f'{dec[0]}👑 TIME 👑{dec[1]}':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('/start')
            text = ''
            sp_time = [
                '1 день 15',
                '1 неделя 30',
                '2 недели 50',
                '1 месяц 90',
                '3 месяца 250',
                '6 месяцев 450',
                '12 месяцев 800'

            ]
            sp_add = []
            sp_control = [80, 400, 1400]
            sp_name = ['Маленькие тарифы:', 'Средние тарифы:', 'Большие тарифы:']
            for i in range(3):
                name = sp_name[i]
                sp_add = []
                if i == 0:
                    text += f'<b>{dec[0]}🟥 {name} 🟥</b>\n'
                elif i == 1:
                    text += f'<b>{dec[0]}🟧 {name} 🟧</b>\n'
                elif i == 2:
                    text += f'<b>{dec[0]}🟩 {name} 🟩</b>\n'
                for voice in sp_time:
                    if i == 0:
                        if int(voice.split()[2]) <= sp_control[i]:
                            text += f'<b>{dec[0]} {" ".join(voice.split()[:2])} - {voice.split()[2]} монеток</b>\n'
                    elif i > 0:
                        if sp_control[i - 1] < int(voice.split()[2]) <= sp_control[i]:
                            text += f'<b>{dec[0]} {" ".join(voice.split()[:2])} - {voice.split()[2]} монеток</b>\n'
                    sp_add.append(f'{dec[0]} {" ".join(voice.split()[:2])} {dec[1]}')
            markup.add(*sp_add)
            bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup)
        elif message.text in voice_sp_buy or message.text in time_sp_buy:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('/start', 'Купить')
            cursor.execute("UPDATE users SET tovar=? WHERE id=?", (str(message.text), (str(message.chat.id))))
            connect.commit()
            bot.send_message(message.chat.id, f'''<b>❗️{dec[0]}При нажатии кнопку купить вы приобретете выбранный 
            товар, без подтверждения оплаты (при наличии средств)❗️{dec[1]}</b>''', parse_mode='html',
                             reply_markup=markup)
        elif message.text == 'Купить':
            tovar = str(cursor.execute('SELECT tovar FROM users WHERE id=?', (str(message.chat.id),)).fetchall()[0][0])
            balance = str(cursor.execute('SELECT balance FROM users WHERE id=?', (str(message.chat.id),)).fetchall()[0][0])
            if int(balance) >= sl_buy[tovar]:
                cursor.execute("UPDATE users SET balance=? WHERE id=?", (str(int(balance) - sl_buy[tovar]),
                                                                         (str(message.chat.id))))
                connect.commit()
                vm = cursor.execute("SELECT VM FROM users WHERE id=?", (str(message.chat.id),)).fetchall()[0][0]
                if tovar in time_sp_buy:
                    date = cursor.execute("SELECT TIME FROM users WHERE id=?", (str(message.chat.id),)).fetchall()[0][0]
                    dt = date.split()[0].split('-')
                    year, mounth, day = int(dt[0]), int(dt[1]), int(dt[2])
                    date = datetime.datetime(year, mounth, day)
                    if date < datetime.datetime.now():
                        date = datetime.datetime.now() + datetime.timedelta(days=int(sl_chet[tovar]))
                    else:
                        date = date + datetime.timedelta(days=int(sl_chet[tovar]))
                    cursor.execute("UPDATE users SET TIME=? WHERE id=?", (str(date), (str(message.chat.id))))
                    connect.commit()
                else:
                    cursor.execute("UPDATE users SET VM=? WHERE id=?", (str(int(vm) + int(sl_chet[tovar])),
                                                                          (str(message.chat.id))))
                    connect.commit()
                cursor.execute("UPDATE users SET sub=? WHERE id=?", (str('SUB'), (str(message.chat.id))))
                connect.commit()
                bot.send_message(message.chat.id, f'<b>{dec[0]}{dec[2]} Вы приобрели {tovar} '
                                                  f'за {sl_buy[tovar]} монеток! {dec[2]}{dec[1]}</b>', parse_mode='html')
            else:
                bot.send_message(message.chat.id, f'<b>{dec[0]}{dec[3]} У вас недостаточно средств!'
                                                  f'{dec[3]}{dec[1]}</b>', parse_mode='html')
        elif message.text[2:-3] in sl_language:
            text = cursor.execute("SELECT voice_text FROM users WHERE id=?", (str(message.chat.id),)).fetchall()[0][0]
            translated = GoogleTranslator(source='auto', target=sl_language[message.text[2:-3]]).translate(str(text))
            cursor.execute("UPDATE users SET language=? WHERE id=?", (str(sl_language[message.text[2:-3]]),
                                                                      (str(message.chat.id))))
            connect.commit()
            bot.send_message(message.chat.id, f'<b>{dec[0]}{dec[2]} {translated} {dec[2]}{dec[1]}</b>', parse_mode='html')
        elif message.text == 'получить аудио':
            try:
                text = cursor.execute("SELECT voice_text FROM users WHERE id=?", (str(
                    message.chat.id),)).fetchall()[0][0]
                language = str(cursor.execute("SELECT language FROM users WHERE id=?", (str(
                    message.chat.id),)).fetchall()[0][0])
                translated = GoogleTranslator(source='auto', target=language).translate(str(text))
                tts = gTTS(translated, lang=language)
                voice_file = io.BytesIO()
                tts.write_to_fp(voice_file)
                voice_file.seek(0)
                bot.send_voice(message.chat.id, voice_file)
            except Exception as ex:
                print(ex.__class__.__name__)
                bot.send_message(message.chat.id,
                                 f'<b>{dec[0]}{dec[3]}нельзя получить аудио на этом языке!'
                                 f' ({str(ex.__class__.__name__)})'
                                 f'{dec[3]}{dec[1]}</b>', parse_mode='html')
        connect.close()
        print(message.chat.id, message.chat.username, message.text)


while True:
    try:
        bot.polling(none_stop=True, timeout=90)
    except Exception as e:
        print(datetime.datetime.now(), e)
        time.sleep(5)