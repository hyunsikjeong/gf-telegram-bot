import logging

from .database import search_dict, stat_dict
from . import util

STAT_MESSAGE = """도감 NO. : {0}
이름 : {1}
- 스탯 -
"""

def stat(bot, update):
    try:
        num = util.command_doll(update)
        if num is None: return
        obj = search_dict[num]
        stats = stat_dict[num]

        s = STAT_MESSAGE.format(obj['no'], obj['name'])
        for stat in stats:
            s += "{0}: {1}\n".format(stat[0], stat[1])
        
        update.message.reply_text(s)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.stat): ")
