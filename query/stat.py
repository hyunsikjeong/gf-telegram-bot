import logging

from .database import get_doll_by_num
from . import util

STAT_MESSAGE = """도감 NO. : {0}
이름 : {1}
- 스탯 -
"""

def stat(bot, update):
    try:
        num = util.command_doll(update)
        if num is None: return
        doll = get_doll_by_num(num)
        stats = doll['stats']

        s = STAT_MESSAGE.format(doll['no'], doll['name'])
        for stat in stats:
            s += "{0}: {1}\n".format(stat[0], stat[1])
        
        update.message.reply_text(s)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.stat): ")
