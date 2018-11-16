# exc.py

from telegram.ext import CommandHandler
from telegram import Update


# Extended Command Handler for '!' (Exclamation mark)
# Main code is from telegram.ext.CommandHandler
class ExtendedCommandHandler(CommandHandler):
    def check_update(self, update):

        if (isinstance(update, Update) and
            (update.message or update.edited_message and self.allow_edited)):
            message = update.message or update.edited_message

            if message.text and (message.text.startswith('/')
                                 or message.text.startswith('!')) and len(
                                     message.text) > 1:
                command = message.text[1:].split(None, 1)[0].split('@')
                command.append(message.bot.username)

                if self.filters is None:
                    res = True
                elif isinstance(self.filters, list):
                    res = any(func(message) for func in self.filters)
                else:
                    res = self.filters(message)

                return res and (
                    command[0].lower() in self.command
                    and command[1].lower() == message.bot.username.lower())
            else:
                return False

        else:
            return False
