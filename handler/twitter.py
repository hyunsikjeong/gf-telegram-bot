import sys, traceback
import logging, json
import threading, queue, oauth2, urllib
import time
from telegram.error import Unauthorized

try:
    ALERT_CHATID_LIST = json.load(open('alert_chatid.json'))
except:
    ALERT_CHATID_LIST = []
    json.dump(ALERT_CHATID_LIST, open('alert_chatid.json', 'w'))


def oauth_req(url, args, setting):
    url = url + urllib.parse.urlencode(args)
    consumer = oauth2.Consumer(
        key=setting['tw_consumer_key'], secret=setting['tw_consumer_secret'])
    token = oauth2.Token(
        key=setting['tw_access_token'], secret=setting['tw_access_secret'])
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method="GET", body=b"", headers=None)

    content = json.loads(content.decode("utf-8"))
    print(content)
    if 'errors' not in content:
        return content


message_queue = queue.Queue()


def send_message(updater):
    logger = logging.getLogger('gftrack')
    while True:
        print("send_message")
        if message_queue.empty():
            time.sleep(3)
            continue
        message = message_queue.get()
        remove_flag = False
        for chatid in ALERT_CHATID_LIST:
            try:
                logger.debug("Sent message to " + str(chatid))
                updater.bot.send_message(chat_id=chatid, text=message)

                # To avoid telegram API limit
                # Check: https://core.telegram.org/bots/faq#how-can-i-message-all-of-my-bot-39s-subscribers-at-once
                time.sleep(3)
            except Unauthorized:
                logger.info("Unauthrized user: deleting user id " +
                            str(chatid))
                ALERT_CHATID_LIST.remove(chatid)
                remove_flag = True
            except:
                logger.exception("Unhandled Exception: ")

        if remove_flag:
            json.dump(ALERT_CHATID_LIST, open('alert_chatid.json', 'w'))


def track_twitter(setting, updater):
    logger = logging.getLogger('gftrack')
    logger.debug("Starting tracking Twitter account {}".format(
        setting['tw_gf_bot_id']))
    base_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?'
    since_id = None

    while True:
        print("track_twitter")
        try:
            if since_id is None:
                args = {
                    'screen_name': setting['tw_gf_bot_id'],
                    'exclude_replies': 'true',
                    'include_rts': 'false',
                    'count': '1'
                }
                content = oauth_req(base_url, args, setting)
                if content is not None:
                    since_id = content[0]['id']
                    logger.debug("Latest Tweet ID: {}".format(since_id))
            else:
                args = {
                    'screen_name': setting['tw_gf_bot_id'],
                    'exclude_replies': 'true',
                    'include_rts': 'false',
                    'since_id': since_id
                }
                content = oauth_req(base_url, args, setting)
                if content is not None:
                    for tweet in content:
                        since_id = max(since_id, tweet['id'])
                        logger.debug("Latest Tweet ID: {}".format(since_id))

                        txt = "[새 공식 트윗] https://twitter.com/{}/status/{}".format(
                            setting['tw_gf_bot_id'], tweet['id'])

                        message_queue.put(txt)
                        logger.debug("Put message into the queue: " + txt)
        except:
            logger.exception("Unhandled Exception: ")
        time.sleep(1.5)


# /pin command
def pin(bot, update):
    chat_id = update.message.chat.id
    if chat_id in ALERT_CHATID_LIST:
        update.message.reply_text("이미 pin 되어있는 채팅입니다.")
        return

    ALERT_CHATID_LIST.append(chat_id)
    json.dump(ALERT_CHATID_LIST, open('alert_chatid.json', 'w'))
    update.message.reply_text(
        "pin을 완료했습니다. 이제 새 공식 트윗이 올라오면 bot이 해당 트윗을 메세지로 보냅니다.")


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
    message_thread = threading.Thread(target=send_message, args=(updater, ))
    message_thread.start()
    twitter_thread = threading.Thread(
        target=track_twitter, args=(
            setting,
            updater,
        ))
    twitter_thread.start()
