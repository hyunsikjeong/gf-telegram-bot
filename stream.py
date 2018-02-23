# stream.py

import sys, traceback
import logging, json
import tweepy
import time
from telegram.error import Unauthorized

ALERT_CHATID_LIST = json.load(open('alert_chatid.json'))

# Tweepy Streaming Listener
class GFTracker(tweepy.StreamListener):

    def __init__(self, userid, updater, api=None):
        super(GFTracker, self).__init__(api=api)
        self.userid = userid
        self.updater = updater

    def on_status(self, status):
        logger = logging.getLogger('gftrack')
        logger.debug("Checking new tweet id:{}".format(status.id))

        # Check its writer
        if self.userid != status.user.id:
            logger.debug("User ID is different: " + status.user.id_str)
            return
        # Check whether it is a reply to someone else
        elif status.in_reply_to_user_id_str is not None and self.userid != status.in_reply_to_user_id:
            logger.debug("In reply to user ID is different: " + status.in_reply_to_user_id_str)
            return 
        
        tweetid = status.id
        username = status.user.screen_name
        txt = "[새 공식 트윗] https://twitter.com/{}/status/{}".format(username, tweetid)

        logger.debug("Sending messages: " + txt)

        remove_flag = False

        for chatid in ALERT_CHATID_LIST:
            try:
                logger.debug("Sent message to " + str(chatid))
                self.updater.bot.send_message(chat_id=chatid, text=txt)

                # To avoid telegram API limit
                # Check: https://core.telegram.org/bots/faq#how-can-i-message-all-of-my-bot-39s-subscribers-at-once
                time.sleep(3)
            except Unauthorized:
                logger.info("Unauthrized user: deleting user id " + str(chatid))
                ALERT_CHATID_LIST.remove(chatid)
                remove_flag = True
            except:
                logger.exception("Unhandled Exception: ")

        if remove_flag:
            json.dump(ALERT_CHATID_LIST, open('alert_chatid.json', 'w'))

    def on_exception(self, exception):
        logger = logging.getLogger('gftrack')
        logger.error("on_exception called: \n{}".format(exception))
        return

    def on_error(self, status_code):
        logger = logging.getLogger('gftrack')
        logger.error("on_error called: {}".format(status_code))
        return True # Always reconnect


# /pin command
def pin(bot, update):
    chat_id = update.message.chat.id
    if chat_id in ALERT_CHATID_LIST:
        update.message.reply_text("이미 pin 되어있는 채팅입니다.")
        return

    ALERT_CHATID_LIST.append(chat_id)
    json.dump(ALERT_CHATID_LIST, open('alert_chatid.json', 'w'))
    update.message.reply_text("pin을 완료했습니다. 이제 새 공식 트윗이 올라오면 bot이 해당 트윗을 메세지로 보냅니다.")

# /unpin command
def unpin(bot, update):
    chat_id = update.message.chat.id
    if chat_id not in ALERT_CHATID_LIST:
        update.message.reply_text("이미 unpin 되어있는 채팅입니다.")
        return

    ALERT_CHATID_LIST.remove(chat_id)
    json.dump(ALERT_CHATID_LIST, open('alert_chatid.json', 'w'))
    update.message.reply_text("unpin을 완료했습니다. 다시 사용하고 싶으시다면 pin 명령어를 사용해주세요.")

def start_tracking(setting, updater):
    # Twitter auth
    auth = tweepy.auth.OAuthHandler(setting['tw_consumer_key'], setting['tw_consumer_secret'])
    auth.set_access_token(setting['tw_access_token'], setting['tw_access_secret'])

    # Screen name to user id
    api = tweepy.API(auth)
    user = api.get_user(screen_name=setting['tw_gf_bot_id'])
    userid = user.id

    # Set stream
    stream = tweepy.Stream(auth, GFTracker(userid, updater), timeout=None)

    # Start filter
    stream.filter([str(userid)], None, async=True)