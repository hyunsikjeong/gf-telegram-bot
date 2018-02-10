# query.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import sys, traceback
import json, re
import logging

# LOAD DICTS
DOLL_DICT = json.load(open('dict/doll_dict.json', 'r', encoding='utf8'))
EQUIP_DICT = json.load(open('dict/equip_dict.json', 'r', encoding='utf8'))
SEARCH_DICT = json.load(open('dict/search_dict.json', 'r', encoding='utf8'))
BUFF_DICT = json.load(open('dict/buff_dict.json', 'r', encoding='utf8'))
STAT_DICT = json.load(open('dict/stat_dict.json', 'r', encoding='utf8'))
SKILL_DICT = json.load(open('dict/skill_dict.json', 'r', encoding='utf8'))
ALIAS_DICT = json.load(open('dict/alias_dict.json', 'r', encoding='utf8'))
UPGRADE_DICT = json.load(open('dict/upgrade_dict.json', 'r', encoding='utf8'))

HELP_MESSAGE = """사용법:
/ㅇㅎ OR /doll - 제조에 걸리는 시간
예) /인형 0022 OR /doll 0022

/ㅈㅂ OR /equip - 제조에 걸리는 시간
예) /장비 0005 OR /equip 0005

/ㄱㅅ OR /search - 인형 이름 OR 별명으로 기본 정보 검색
예) /검색 스프링필드 OR /ㄱㅅ 춘전이

/ㅅㅌ OR /stat - 인형 이름 OR 별명으로 능력치 검색
예) /스탯 스프링필드 OR /ㅅㅌ 춘전이

/ㅂㅍ OR /buff - 인형 이름 OR 별명으로 버프 진형 검색
예) /버프 스프링필드 OR /ㅂㅍ 춘전이

/ㅅㅋ OR /skill - 인형 이름 OR 별명으로 스킬 검색
예) /스킬 스프링필드 OR /ㅅㅋ 춘전이

/ㄱㅈ OR /upgrade - 인형 이름 OR 별명으로 개장 정보 검색
예) /개장 스프링필드 OR /ㄱㅈ 춘전이

/pin, /unpin - 소녀전선 공식 트위터의 새 트윗이 올라오면 알림 받기, 알림 받지 않기 (기본 설정은 알림 받지 않음)

모든 명령어는 / 대신 !의 사용이 가능합니다."""

SEARCH_MESSAGE_WITH_TIME = """도감 NO. : {0}
이름 : {1}
등급 : ★{2}
타입 : {3}
획득 방법 : {4}
제조 시간 : {5}
http://rb-tree.xyz/szimage/{0}.png"""

SEARCH_MESSAGE_WITHOUT_TIME = """도감 NO. : {0}
이름 : {1}
등급 : ★{2}
타입 : {3}
획득 방법 : {4}
http://rb-tree.xyz/szimage/{0}.png"""

SKILL_MESSAGE = """도감 NO. : {0}
이름 : {1}
스킬명: {2}
효과:
{3}
- 이하 Lv.10 기준 수치 -
"""

BUFF_MESSAGE = """도감 NO. : {0}
이름 : {1}
버프 효과{2}:
{3}
버프 형태:
"""

STAT_MESSAGE = """도감 NO. : {0}
이름 : {1}
- 스탯 -
"""

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

UPGRADE_MESSAGE_3 = SKILL_MESSAGE

UPGRADE_MESSAGE_4 = """도감 NO. : {0}
이름 : {1}
전용 장비 효과:
{2}
"""

UPGRADE_MESSAGE_5 = """도감 NO. : {0}
이름 : {1}
- 스탯 (Lv.100/110/115/120) -
"""

def _get_command(update):
    logger = logging.getLogger('command')
    message = update.message.text
    user = update.message.from_user
    logger.info('New command from user {}({}) : {} '.format(user.username, user.id, message))

    command = re.sub(' +', ' ', message.strip())
    command = command.split(' ', 1)
    if len(command) <= 1: return ""
    else: return command[1]

def _command_time(update):
    time = _get_command(update)
    try:
        return (int(time) // 100, int(time) % 100, str(int(time)))
    except:
        update.message.reply_text("올바르지 않은 입력입니다.")
        return (None, None, None)

def _command_doll(update):
    alias = _get_command(update).lower()
    if alias not in ALIAS_DICT:
        update.message.reply_text("DB에서 해당 별명을 찾을 수 없습니다.")
        return None
    return ALIAS_DICT[alias]

#def _is_bot(update):
#    return update.message.from_user.is_bot

def help(bot, update):
    update.message.reply_text(HELP_MESSAGE)

def doll(bot, update):
    try:
        hour, minute, time = _command_time(update)

        if time is None: return
        elif time not in DOLL_DICT:
            update.message.reply_text("DB에 존재하지 않는 시간입니다.")
            return

        s = "" 
        for obj in DOLL_DICT[time]:
            s += "{:02d}:{:02d}:00  ★{}  {}  {}\n".format(hour, minute, obj['class'], obj['type'], obj['name'])
            
        update.message.reply_text(s)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.doll): ")

def equip(bot, update):
    try:
        hour, minute, time = _command_time(update)

        if time is None: return
        elif time not in EQUIP_DICT:
            update.message.reply_text("DB에 존재하지 않는 시간입니다.")
            return

        s = ""
        for obj in EQUIP_DICT[time]:
            if obj['class'] == 6:
                s += "{:02d}:{:02d}:00  [요정]  {}\n".format(hour, minute, obj['name'])
            else:
                s += "{:02d}:{:02d}:00  ★{}  {}\n".format(hour, minute, obj['class'], obj['name'])
            
        update.message.reply_text(s)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.equip): ")
    
def search(bot, update):
    try:
        num = _command_doll(update)
        if num is None: return
        obj = SEARCH_DICT[num]

        if obj['time'] != "00:00":
            s = SEARCH_MESSAGE_WITH_TIME.format(obj['no'], obj['name'], obj['class'],
                                                obj['type'], obj['obtain'], obj['time'])
        else:
            s = SEARCH_MESSAGE_WITHOUT_TIME.format(obj['no'], obj['name'], obj['class'],
                                                    obj['type'], obj['obtain'])
        update.message.reply_text(s)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.search): ")

def skill(bot, update):
    try:
        num = _command_doll(update)
        if num is None: return
        obj = SEARCH_DICT[num]
        skill = SKILL_DICT[num]

        s = SKILL_MESSAGE.format(obj['no'], obj['name'], skill['name'], skill['desc'])

        for i in range(0, len(skill['spec'])):
            s += "{0}: {1}\n".format(skill['spec'][i][0], skill['spec'][i][1])

        update.message.reply_text(s)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.skill): ")    

def buff(bot, update):
    try:
        num = _command_doll(update)
        if num is None: return
        obj = SEARCH_DICT[num]
        buff = BUFF_DICT[num]

        # description
        s = BUFF_MESSAGE.format(obj['no'], obj['name'], buff['buff_option'], buff['buff_desc'])

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

def stat(bot, update):
    try:
        num = _command_doll(update)
        if num is None: return
        obj = SEARCH_DICT[num]
        stats = STAT_DICT[num]

        s = STAT_MESSAGE.format(obj['no'], obj['name'])
        for stat in stats:
            s += "{0}: {1}\n".format(stat[0], stat[1])
        
        update.message.reply_text(s)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.stat): ")

def upgrade_callback(bot, update):
    try:
        num, uid, option = query.data.split('_')
        if query.from_user.id != int(uid):
            return

        obj = SEARCH_DICT[num]
        upgrade = UPGRADE_DICT[num]

        if option == '1':
            buff = BUFF_DICT[num]

            s = UPGRADE_MESSAGE_1.format(obj['no'], obj['name'], buff['buff_option'], upgrade['buff_desc'])

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
        elif option == '2':
            skill = upgrade['orig_skill']
            s = UPGRADE_MESSAGE_2.format(obj['no'], obj['name'], skill['name'], skill['desc'])

            for i in range(0, len(skill['spec'])):
                s += "{0}: {1}\n".format(skill['spec'][i][0], skill['spec'][i][1])
        elif option == '3':
            skill = upgrade['new_skill']
            s = UPGRADE_MESSAGE_3.format(obj['no'], obj['name'], skill['name'], skill['desc'])

            for i in range(0, len(skill['spec'])):
                s += "{0}: {1}\n".format(skill['spec'][i][0], skill['spec'][i][1])
        elif option == '4':
            s = UPGRADE_MESSAGE_4.format(obj['no'], obj['name'], upgrade['equip'])
        elif option == '5':
            stats = upgrade['stat']

            s = UPGRADE_MESSAGE_5.format(obj['no'], obj['name'])
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
        num = _command_doll(update)
        if num is None: return
        obj = SEARCH_DICT[num]
        if num not in UPGRADE_DICT:
            update.message.reply_text("개장 정보가 없거나, 개장이 불가능한 인형입니다.")
            return

        s = "선택한 인형: {}\n보고 싶은 개장 정보를 선택하세요.".format(obj['name'])

        uid = update.message.from_user.id
        button_list = [
            [InlineKeyboardButton("1단계 버프", callback_data="{}_{}_1".format(obj['no'], uid)),
            InlineKeyboardButton("1단계 스킬", callback_data="{}_{}_2".format(obj['no'], uid))],
            [InlineKeyboardButton("2단계 추가 스킬", callback_data="{}_{}_3".format(obj['no'], uid)),
            InlineKeyboardButton("3단계 전용 장비", callback_data="{}_{}_4".format(obj['no'], uid))],
            [InlineKeyboardButton("스탯 변화", callback_data="{}_{}_5".format(obj['no'], uid))]
        ]
        reply_markup = InlineKeyboardMarkup(button_list)
        update.message.reply_text(text=s, reply_markup=reply_markup)
    except:
        logger = logging.getLogger('query')
        logger.exception("Unhandled Exception (query.upgrade): ")