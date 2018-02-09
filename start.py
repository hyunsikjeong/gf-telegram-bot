# start.py

from telegram.ext import Updater, CallbackQueryHandler
import json
import logging

# Custom Modules
import stream, exc, query

def init_logger(name, fileLevel=logging.DEBUG, streamLevel=logging.ERROR):
    logger = logging.getLogger(name)
    logger.setLevel(min(fileLevel, streamLevel))

    formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    fileHandler = logging.FileHandler('./log/{}.log'.format(name), encoding='utf8')
    fileHandler.setLevel(fileLevel)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(streamLevel)
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

if __name__ == "__main__":
    # LOGGER SETTING
    init_logger('gftrack')
    init_logger('command', fileLevel=logging.INFO)
    init_logger('query')

    # LOAD SETTING
    setting = json.load(open('setting.json', 'r'))

    # TELEGRAM BOT SETTING
    updater = Updater(setting['tg_token'])
    dispatcher = updater.dispatcher

    commands = [ (['start', 'help', '도움말', '도움'], query.help),
                 (['doll', 'ㅇㅎ', '인형'], query.doll),
                 (['equip', 'ㅈㅂ', '장비'], query.equip),
                 (['search', 'ㄳ', 'ㄱㅅ', '검색'], query.search),
                 (['buff', '버프', 'ㅂㅍ'], query.buff),
                 (['stat', '스탯', 'ㅅㅌ'], query.stat),
                 (['skill', '스킬', 'ㅅㅋ'], query.skill),
                 (['upgrade', '개장', 'ㄱㅈ'], query.upgrade),
                 (['pin'], stream.pin),
                 (['unpin'], stream.unpin)
                 ]

    for (command_list, command_function) in commands:
        dispatcher.add_handler(exc.ExcCommandHandler(command_list, command_function))

    dispatcher.add_handler(CallbackQueryHandler(query.upgrade_callback))

    # BOT POLLING & TWEET STREAMING START

    stream.start_tracking(setting, updater)
    updater.start_polling(allowed_updates=['message', 'channel_post', 'callback_query'])
    updater.idle()