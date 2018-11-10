import logging

from .database import get_doll_by_time
from . import util

def doll(bot, update):
    try:
        hour, minute, time = util.command_time(update)
        if time is None: return

        doll = get_doll_by_time(time)
        if doll is None:
            update.message.reply_text("DB에 존재하지 않는 시간입니다.")
            return

        s = "" 
        for obj in doll:
            s += "{:02d}:{:02d}:00  ★{}  {}  {}\n".format(hour, minute, obj['class'], obj['type'], obj['name'])
            
        update.message.reply_text(s)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.doll): ")