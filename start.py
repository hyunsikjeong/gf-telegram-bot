from telegram.ext import Updater, CallbackQueryHandler
import json
import logging

from handler.command import ExtendedCommandHandler
from handler import twitter
from query import *

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
    init_logger('gftrack')
    init_logger('command', fileLevel=logging.INFO)
    init_logger('query')

    setting = json.load(open('setting.json', 'r'))
    updater = Updater(setting['tg_token'])
    dispatcher = updater.dispatcher

    commands = [ (['start', 'help', '도움말', '도움'], help.help),
                 (['doll', 'ㅇㅎ', '인형'], doll.doll),
                 (['equip', 'ㅈㅂ', '장비'], equip.equip),
                 (['search', 'ㄳ', 'ㄱㅅ', '검색'], search.search),
                 (['buff', '버프', 'ㅂㅍ'], buff.buff),
                 (['stat', '스탯', 'ㅅㅌ'], stat.stat),
                 (['skill', '스킬', 'ㅅㅋ'], skill.skill),
                 (['upgrade', '개장', 'ㄱㅈ'], upgrade.upgrade),
                 (['pin'], twitter.pin),
                 (['unpin'], twitter.unpin)
                 ]

    for (command_list, command_function) in commands:
        dispatcher.add_handler(ExtendedCommandHandler(command_list, command_function))
    dispatcher.add_handler(CallbackQueryHandler(upgrade.upgrade_callback))

    twitter.start_tracking(setting, updater)
    updater.start_polling(allowed_updates=['message', 'channel_post', 'callback_query'])
    updater.idle()