# импортируем нужные модули
from collections import Counter
from telegram import ReplyKeyboardMarkup

import markovify
import os
import time

a = []


stoplist = ['the', 'you', 'i', 'to', 'a', 'and', 'of', 'your', 'my', 'it', 'me', 'is', 'in', 'for', 'he', 'that',
            'have', 'what', 'not', 'be', 'no', 'do', 'will', 'are', 'him', 'we', 'with', 'was', 'this', 'his', "don't",
            'if', 'but', 'they', 'on', 'all', 'them', "i'm", 'know', 'one', 'her', 'as', "you're", "it's", 'so', 'want',
            'here', 'when', 'at', 'from', 'like', 'how', 'would', 'us', 'there', 'now', 'did', 'can', 'who', 'she', 'come',
            'about', 'why', 'go', 'see', "he's", 'their', 'take', 'back', 'tell', 'get', 'or', 'has', 'our',
            'were', 'well', 'more', 'out', "i'll", 'up', 'been', 'right', 'than', 'where', 'only', 'just',
            'had', 'an', "i've", 'could', 'need', 'yes', "that's", "can't", 'by', 'too', 'should', 'some', 'before',
            "didn't", 'am', 'oh', 'going', 'let', 'many', "you'll", 'any', 'then', 'very',
            'must', "won't", "you've", 'ever', 'first', 'off', 'told', 'these',
            'got', 'down', 'much', '"', 'every', "we're", 'into', 'does', 'said',
            'enough', 'still', 'because', 'nothing', 'done', "there's", 'thing', 'years', 'away', 'again', 'over',
            'even', "she's", 'last', 'other', 'after', 'those', 'saw', "they're", 'may', 'own',
            'once', "we'll", 'something', "i'd", 'might', "what's", 'doing', 'wanted', 'two',
            'through', 'until', 'things', 'seen', "doesn't", 'heard', 'made', 'sure', 'most',
            'took', 'thought', 'shall', 'came', 'anything', 'three', 'far', 'another', "you'd", 'yours', 'new', 'someone',
            'mine', "we've", 'without', "isn't", 'yourself', 'gave', 'wants', "wasn't", "they'll", 'maybe', 'against',
            'mean', 'coming', 'both', 'knew', 'send', 'rest', 'left', 'half', 'same', 'anyone', 'perhaps', "wouldn't", 'while', 'aye',
            'since', 'quite', 'yet', 'everything', 'really', 'such', 'young', 'realm', 'gone', 'knows',
            'hold', 'few', 'lost', "he'll", '000', 'says', 'best', 'soon', 'never', 'good', '</i>',
            '(', ')', '<i>', "haven't", '_']

# основные кнопки
def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup(
        [['Дай мне фразу'], ['Статистика по сезонам']], resize_keyboard=True
        )
    return my_keyboard

# кнопки для выбора сезона
def get_keyboard_2():
    my_keyboard = ReplyKeyboardMarkup(
        [['1', '2', '3'],
         ['4', '5', '6'],
         ['7', 'Лучше все-таки фразу']], resize_keyboard=True
        )
    return my_keyboard

# бот сначала здоровается, он вежливый
def greet_user(bot, update):
    print (update)
    text = f'Привет, {update.message.chat.first_name}'
    return update.message.reply_text(text, reply_markup=get_keyboard())

# спрашивает, хочет ли пользователь еще одну фразу
def cont(bot, update):
    return update.message.reply_text("Еще?", reply_markup=get_keyboard())

# обучение
def learn(bot, update):
    start_time = time.time()
    with open("full.txt", "r", encoding='utf-8') as f:
        text = f.read()
        text_model = markovify.Text(text)
        print("--- %s seconds ---" % (time.time() - start_time))
    return text_model

# здесь генерируется фраза
def phrase(bot, update):
    files = os.listdir("./books")

    my_dict = {}
    for f in files:
        name = "./books/" + f
        with open(name, "r", encoding="utf-8") as m:
            my_dict[f] = m.read()
    for value in my_dict.values():
        with open("full.txt", "a", encoding="utf-8") as f:
            f.write(value)
    if len(a) == 0:
        update.message.reply_text("Минуту, пожалуйста.") # иногда на первую фразу уходит некоторое время (секунд 20), а следующие уже выдаются мгновенно
        text_model = learn(bot, update)
        a.append(text_model)
    update.message.reply_text(a[0].make_short_sentence(140))
    update.message.reply_text("Еще?", reply_markup=get_keyboard())

# при нажатии кнопки "статистика по сезонам"
def stats(bot, update):
    update.message.reply_text("Я покажу самые популярные слова по сезонам ИП")
    update.message.reply_text("Какой сезон хочешь?", reply_markup=get_keyboard_2())

# ищем топ-10 слов минус стоп-слова
def top10(bot, update):
    top = Counter()
    season = update.message.text

    with open(f'./seasons/season_{season}.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.split()

    for t in text:
        if t not in stoplist:
            top[t] += 1

    top = dict(top)
    top = sorted(top.items(), key=lambda x: x[1], reverse=True)

    place = 1
    for i in top[:10]:
        update.message.reply_text(f'{place}. {i[0].capitalize()}')
        place += 1
    return cont(bot, update)






