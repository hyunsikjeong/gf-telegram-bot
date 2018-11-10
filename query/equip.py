import logging

from .database import get_equip_by_time
from . import util

def equip(bot, update):
    try:
        hour, minute, time = util.command_time(update)
        if time is None: return

        equip = get_equip_by_time(time)
        if equip is None:
            update.message.reply_text("DB에 존재하지 않는 시간입니다.")
            return

        s = ""
        for obj in equip:
            if obj['class'] == 6:
                s += "{:02d}:{:02d}:00  [요정]  {}\n".format(hour, minute, obj['name'])
            else:
                s += "{:02d}:{:02d}:00  ★{}  {}\n".format(hour, minute, obj['class'], obj['name'])
            
        update.message.reply_text(s)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.equip): ")