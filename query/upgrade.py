import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .database import get_doll_by_num
from . import util

UPGRADE_MESSAGE_1 = """도감 NO. : {0}
이름 : {1}
버프 효과{2}:
{3}
버프 형태:
"""

UPGRADE_MESSAGE_2 = """도감 NO. : {0}
이름 : {1}
스킬명: {2}
효과:
{3}
- 이하 강화된 Lv.10 기준 수치 -
"""

UPGRADE_MESSAGE_3 = """도감 NO. : {0}
이름 : {1}
스킬명: {2}
효과:
{3}
- 이하 Lv.10 기준 수치 -
"""

UPGRADE_MESSAGE_4 = """도감 NO. : {0}
이름 : {1}
전용 장비 효과:
{2}
"""

UPGRADE_MESSAGE_5 = """도감 NO. : {0}
이름 : {1}
- 스탯 (Lv.100/110/115/120) -
"""

def upgrade_callback(bot, update):
    query = update.callback_query
    
    try:
        num, uid, option = query.data.split('_')
        if query.from_user.id != int(uid):
            return

        doll = get_doll_by_num(num)
        upgrade = doll['upgrade']

        if option == '1':
            buff = upgrade['buff']
            s = UPGRADE_MESSAGE_1.format(doll['no'], doll['name'], buff['option'], buff['desc'])

            s += "```\n"
            for i in range(0, 9, 3):
                s += "+---+---+---+\n"
                for j in range(3):
                    c = buff['form'][i+j]
                    if c == '0': s += "|   "
                    elif c == '1': s += "| ! "
                    else: s += "| D "
                s += "|\n"

            s += "+---+---+---+```"
        elif option == '2':
            skill = upgrade['orig_skill']
            s = UPGRADE_MESSAGE_2.format(doll['no'], doll['name'], skill['name'], skill['desc'])

            for i in range(0, len(skill['spec'])):
                s += "{0}: {1}\n".format(skill['spec'][i][0], skill['spec'][i][1])
        elif option == '3':
            skill = upgrade['new_skill']
            s = UPGRADE_MESSAGE_3.format(doll['no'], doll['name'], skill['name'], skill['desc'])

            for i in range(0, len(skill['spec'])):
                s += "{0}: {1}\n".format(skill['spec'][i][0], skill['spec'][i][1])
        elif option == '4':
            s = UPGRADE_MESSAGE_4.format(doll['no'], doll['name'], upgrade['equip'])
        elif option == '5':
            stats = upgrade['stat']

            s = UPGRADE_MESSAGE_5.format(doll['no'], doll['name'])
            for stat in stats:
                s += "{0}: {1}\n".format(stat[0], stat[1])
        else:
            s = "Something wrong: {}".format(option)
        
        bot.edit_message_text(text=s,
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id,
                            parse_mode="Markdown")
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.upgrade_callback): ")

def upgrade(bot, update):
    try:
        num = util.command_doll(update)
        if num is None: return

        doll = get_doll_by_num(num)
        if 'upgrade' not in doll:
            update.message.reply_text("개장 정보가 없거나, 개장이 불가능한 인형입니다.")
            return

        s = "선택한 인형: {}\n보고 싶은 개장 정보를 선택하세요.".format(doll['name'])

        uid = update.message.from_user.id
        button_list = [
            [InlineKeyboardButton("1단계 버프", callback_data="{}_{}_1".format(doll['no'], uid)),
            InlineKeyboardButton("1단계 스킬", callback_data="{}_{}_2".format(doll['no'], uid))],
            [InlineKeyboardButton("2단계 추가 스킬", callback_data="{}_{}_3".format(doll['no'], uid)),
            InlineKeyboardButton("3단계 전용 장비", callback_data="{}_{}_4".format(doll['no'], uid))],
            [InlineKeyboardButton("스탯 변화", callback_data="{}_{}_5".format(doll['no'], uid))]
        ]
        reply_markup = InlineKeyboardMarkup(button_list)
        update.message.reply_text(text=s, reply_markup=reply_markup)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.upgrade): ")