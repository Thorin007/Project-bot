# импортируем нужные параметры из другого файла
from handlers import greet_user, phrase, stats, top10

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import logging

# мне было лень делать отдельный файл
PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
         'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}
         }
API_KEY = ('1198642509:AAEsDY3o14iWcc6OWwJCsp7HLdgyTDIZB5o')


def main():
    mybot = Updater(API_KEY, request_kwargs=PROXY)

    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.regex("Дай мне фразу"), phrase))
    dp.add_handler(MessageHandler(Filters.regex("Статистика по сезонам"), stats))

    dp.add_handler(MessageHandler(Filters.regex("1"), top10))
    dp.add_handler(MessageHandler(Filters.regex("2"), top10))
    dp.add_handler(MessageHandler(Filters.regex("3"), top10))
    dp.add_handler(MessageHandler(Filters.regex("4"), top10))
    dp.add_handler(MessageHandler(Filters.regex("5"), top10))
    dp.add_handler(MessageHandler(Filters.regex("6"), top10))
    dp.add_handler(MessageHandler(Filters.regex("7"), top10))

    dp.add_handler(MessageHandler(Filters.text, phrase))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
