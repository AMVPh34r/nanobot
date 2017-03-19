from plugin import Plugin
from decorators import command


class Say(Plugin):
    fancy_name = "Simon Says"

    @staticmethod
    async def get_commands(server):
        commands = [
            {
                'name': '!say phrase',
                'description': 'Make the bot say something (if TTS is enabled).'
            }
        ]
        return commands

    @command(pattern='^!say (.*)$')
    async def ask(self, message, args):
        msg_clean = message.content.replace('!say ','')
        await self.bot.send_message(
            message.channel,
            msg_clean,
            tts=True
        )
        return
