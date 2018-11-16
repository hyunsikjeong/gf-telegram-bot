import logging

from .database import get_doll_by_num
from . import util

SEARCH_MESSAGE_WITH_TIME = """도감 NO. : {0}
이름 : {1}
등급 : ★{2}
타입 : {3}
획득 방법 : {4}
제조 시간 : {5}
http://rb-tree.xyz/szimage/{0}.png"""

SEARCH_MESSAGE_WITHOUT_TIME = """도감 NO. : {0}
이름 : {1}
등급 : ★{2}
타입 : {3}
획득 방법 : {4}
http://rb-tree.xyz/szimage/{0}.png"""


def search(bot, update):
    try:
        num = util.command_doll(update)
        if num is None:
            return
        doll = get_doll_by_num(num)

        if doll['time'] != "00:00":
            s = SEARCH_MESSAGE_WITH_TIME.format(doll['no'], doll['name'],
                                                doll['class'], doll['type'],
                                                doll['obtain'], doll['time'])
        else:
            s = SEARCH_MESSAGE_WITHOUT_TIME.format(doll['no'], doll['name'],
                                                   doll['class'], doll['type'],
                                                   doll['obtain'])
        update.message.reply_text(s)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.search): ")
