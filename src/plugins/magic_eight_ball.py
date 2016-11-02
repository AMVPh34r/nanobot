from plugin import Plugin
from decorators import command
import random


class EightBall(Plugin):
    fancy_name = "Magic Eight Ball"
    responses = [
        'It is certain',
        'It is decidedly so',
        'Without a doubt',
        'Yes, definitely',
        'You may rely on it',
        'As I see it, yes',
        'Most likely',
        'Outlook good',
        'Yes',
        'Signs point to yes',

        'Reply hazy try again',
        'Ask again later',
        'Better not tell you now',
        'Cannot predict now',
        'Concentrate and ask again',

        'Don\'t count on it',
        'My reply is no',
        'My sources say no',
        'Outlook not so good',
        'Very doubtful',
        'No'
    ]

    @staticmethod
    async def get_commands(server):
        commands = [
            {
                'name': '!8ball question',
                'description': 'Ask the magic 8 ball a question'
            }
        ]
        return commands

    @command(pattern='^!8ball (.*)$')
    async def ask(self, message, args):
        await self.bot.send_message(
            message.channel,
            random.choice(self.responses)
        )
        return
