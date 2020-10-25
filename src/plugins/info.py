from plugin import Plugin
from decorators import command
import platform
import discord


class Info(Plugin):
    fancy_name = "Bot Info"

    @staticmethod
    async def get_commands(server):
        commands = [
            {
                'name': '!info',
                'description': 'Display bot info'
            },
            {
                'name': '!version',
                'description': 'Display current bot version'
            }
        ]
        return commands

    @command(pattern='^!info$')
    async def info(self, message, args):
        response = "Hi, I'm {}, here to serve!\n" \
                   "For a list of commands I know, just send `!help`".format(self.bot.__name__)

        await self.bot.send_message(message.channel, response)
        return

    @command(pattern='^!version$')
    async def version(self, message, args):
        response = "{}, v{}\nPython v{}\nDiscord.py v{}".format(
            self.bot.__name__, self.bot.__version__, platform.python_version(), discord.__version__
        )
        await self.bot.send_message(message.channel, response)
        return
