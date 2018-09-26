import logging

from .database import doll_dict
from . import util

def doll(bot, update):
    try:
        hour, minute, time = util.command_time(update)

        if time is None: return
        elif time not in doll_dict:
            update.message.reply_text("DB에 존재하지 않는 시간입니다.")
            return

        s = "" 
        for obj in doll_dict[time]:
            s += "{:02d}:{:02d}:00  ★{}  {}  {}\n".format(hour, minute, obj['class'], obj['type'], obj['name'])
            
        update.message.reply_text(s)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.doll): ")