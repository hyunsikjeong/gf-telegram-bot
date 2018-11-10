import logging

from .database import get_doll_by_num
from . import util

SKILL_MESSAGE = """도감 NO. : {0}
이름 : {1}
스킬명: {2}
효과:
{3}
- 이하 Lv.10 기준 수치 -
"""

def skill(bot, update):
    try:
        num = util.command_doll(update)
        if num is None: return
        doll = get_doll_by_num(num)
        skill = doll['skill']

        s = SKILL_MESSAGE.format(doll['no'], doll['name'], skill['name'], skill['desc'])

        for i in range(0, len(skill['spec'])):
            s += "{0}: {1}\n".format(skill['spec'][i][0], skill['spec'][i][1])

        update.message.reply_text(s)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.skill): ")    
