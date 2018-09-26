import logging
import re

from .database import alias_dict

def get_command(update):
    logger = logging.getLogger('command')
    message = update.message.text
    user = update.message.from_user
    logger.info('New command from user {}({}) : {} '.format(user.username, user.id, message))

    command = re.sub(' +', ' ', message.strip())
    command = command.split(' ', 1)
    if len(command) <= 1: return ""
    else: return command[1]

def command_time(update):
    time = get_command(update)
    try:
        return (int(time) // 100, int(time) % 100, str(int(time)))
    except:
        update.message.reply_text("올바르지 않은 입력입니다.")
        return (None, None, None)

def command_doll(update):
    alias = get_command(update).lower()
    if alias not in alias_dict:
        update.message.reply_text("DB에서 해당 별명을 찾을 수 없습니다.")
        return None
    return alias_dict[alias]