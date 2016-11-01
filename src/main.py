from bot import ChatBot
import os
import logging

from plugins.help import Help
from plugins.info import Info
from plugins.moderator import Moderator
from plugins.replies import Replies
from plugins.magic_eight_ball import EightBall
from plugins.search import Search
from plugins.timer import Timer

# Global plugins
from plugins.systemlog import SystemLog
from plugins.botgame import BotGame

token = os.getenv('BOT_TOKEN')
bot_debug = os.getenv('BOT_DEBUG')
if bot_debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

bot = ChatBot()
bot.run(token)
