import logging

from .database import get_doll_by_num
from . import util

BUFF_MESSAGE = """도감 NO. : {0}
이름 : {1}
버프 효과{2}:
{3}
버프 형태:
"""

def buff(bot, update):
    try:
        num = util.command_doll(update)
        if num is None: return
        doll = get_doll_by_num(num)
        buff = doll['buff']

        # description
        s = BUFF_MESSAGE.format(doll['no'], doll['name'], buff['buff_option'], buff['buff_desc'])

        # buff
        s += "```\n"
        for i in range(0, 9, 3):
            s += "+---+---+---+\n"
            for j in range(3):
                c = buff['buff'][i+j]
                if c == '0': s += "|   "
                elif c == '1': s += "| ! "
                else: s += "| D "
            s += "|\n"

        s += "+---+---+---+```"
        update.message.reply_text(s, parse_mode="Markdown")
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.buff): ")