import discord
from bot import ChatBot
import os
import logging

from plugins.help import Help
from plugins.info import Info
from plugins.moderator import Moderator
from plugins.replies import Replies
from plugins.magic_eight_ball import EightBall
from plugins.dieroll import DieRoll
from plugins.say import Say
from plugins.search import Search
from plugins.nanowrimo_api import NaNoWriMoAPI
from plugins.name_generator import NameGenerator
from plugins.thesaurus import Thesaurus
from plugins.timer import Timer
from plugins.writein import Writein

# Global plugins
from plugins.systemlog import SystemLog
from plugins.botgame import BotGame

token = os.getenv('BOT_TOKEN')
bot_debug = os.getenv('BOT_DEBUG')
if bot_debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

bot = ChatBot(intents=discord.Intents.default())
bot.run(token)
