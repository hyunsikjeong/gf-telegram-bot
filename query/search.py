import logging

from .database import search_dict
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
        if num is None: return
        obj = search_dict[num]

        if obj['time'] != "00:00":
            s = SEARCH_MESSAGE_WITH_TIME.format(obj['no'], obj['name'], obj['class'],
                                                obj['type'], obj['obtain'], obj['time'])
        else:
            s = SEARCH_MESSAGE_WITHOUT_TIME.format(obj['no'], obj['name'], obj['class'],
                                                    obj['type'], obj['obtain'])
        update.message.reply_text(s)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.search): ")