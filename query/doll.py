import logging

from .database import get_doll_by_time
from . import util


def doll(bot, update):
    try:
        hour, minute, time = util.command_time(update)
        if time is None:
            return

        doll_list = get_doll_by_time(time)
        if len(doll_list) == 0:
            update.message.reply_text("DB에 존재하지 않는 시간입니다.")
            return

        s = ""
        for doll in doll_list:
            s += "{:02d}:{:02d}:00  ★{}  {}  {}\n".format(
                hour, minute, doll['class'], doll['type'], doll['name'])

        update.message.reply_text(s)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.doll): ")
