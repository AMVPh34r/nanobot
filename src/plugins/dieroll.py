from plugin import Plugin
from decorators import command
import random


class Die(object):
    def __init__(self, sides = 6):
        self.sides = sides
        self.choice = None

    def roll(self):
        self.choice = random.randint(1, self.sides)
        return self.choice


class DieRoll(Plugin):
    fancy_name = "Die Roll"

    @staticmethod
    async def get_commands(server):
        commands = [
            {
                'name': '!roll [x]d[y]',
                'description': 'Roll `[x]` dice with `[y]` sides each. Omit `[x]` to roll 1 die.'
            }
        ]
        return commands

    @command(pattern='^!roll ([1-9])?d(0?0?[2-9]$|[1-9][0-9]$|100$)')
    async def roll(self, message, args):
        num_dice = 1 if args[0] is None else int(args[0])
        num_sides = int(args[1])
        results = []
        response_template = "I rolled {dice} d{sides}{plural} {isweird}and got: {results}"

        for i in range(num_dice):
            results.append(str(Die(num_sides).roll()))

        response = response_template.format(
            dice=num_dice,
            sides=num_sides,
            plural="s" if num_dice > 1 else "",
            isweird="(somehow) " if num_sides in [2,3] else "",
            results=", ".join(results)
        )
        await self.bot.send_message(
            message.channel,
            response
        )
        return

    @command(pattern='^!roll(?! [1-9]?d(0?0?[2-9]$|[1-9][0-9]$|100$))')
    async def roll_format(self, message, args):
        await self.bot.send_message(
            message.channel,
            "Command format: `!roll XdY`. `X` must be between 1-9 and `Y` between 2-100."
        )
        return
