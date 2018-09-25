import logging

from .dicts import equip_dict
from . import util

def equip(bot, update):
    try:
        hour, minute, time = util.command_time(update)

        if time is None: return
        elif time not in equip_dict:
            update.message.reply_text("DB에 존재하지 않는 시간입니다.")
            return

        s = ""
        for obj in equip_dict[time]:
            if obj['class'] == 6:
                s += "{:02d}:{:02d}:00  [요정]  {}\n".format(hour, minute, obj['name'])
            else:
                s += "{:02d}:{:02d}:00  ★{}  {}\n".format(hour, minute, obj['class'], obj['name'])
            
        update.message.reply_text(s)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.equip): ")