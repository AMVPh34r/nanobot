from plugin import Plugin
from decorators import command
import random


class Die(object):
    def __init__(self, sides=6, buff=0):
        self.sides = sides
        self.buff = buff
        self.choice = None

    def roll(self, apply_buff=True):
        self.choice = random.randint(1, self.sides) + (self.buff if apply_buff else 0)
        return self.choice


class DieRoll(Plugin):
    fancy_name = "Die Roll"

    @staticmethod
    async def get_commands(server):
        commands = [
            {
                'name': '!roll [x]d[y] +/- [z]',
                'description': 'Roll `[x]` dice with `[y]` sides each. Omit `[x]` to roll 1 die. Optionally '
                               'add/subtract [z] to the result(s).'
            }
        ]
        return commands

    @command(pattern='^!roll ([1-9])?d(0?0?[2-9]|[1-9][0-9]|100)( ?([\+-]) ?(\d{1,2}))?$')
    async def roll(self, message, args):
        print(args)
        num_dice = 1 if args[0] is None else int(args[0])
        num_sides = int(args[1])
        buff = 0 if args[4] is None else (int(args[4]) if args[3] == "+" else int(args[4]) * -1)
        results = []
        if num_sides == 2:
            response_template = "I flipped {dice} coin{plural}{buff} and got: {results}"
        else:
            response_template = "I rolled {dice} d{sides}{plural}{buff}{isweird} and got: {results}"

        for i in range(num_dice):
            results.append(str(Die(num_sides, buff).roll()))

        response = response_template.format(
            dice=num_dice if num_dice > 1 else "a",
            sides=num_sides,
            plural="s" if num_dice > 1 else "",
            buff="" if buff == 0 else (" ({}{}) ".format(
                "+" if buff > 0 else "",
                buff
            )),
            isweird=" (somehow)" if num_sides in [2, 3] else "",
            results=", ".join(results)
        )
        await self.bot.send_message(
            message.channel,
            response
        )
        return

    @command(pattern='^!roll(?! [1-9]?d(0?0?[2-9]|[1-9][0-9]|100)( ?[\+-] ?\d{1,2})?$)')
    async def roll_format(self, message, args):
        await self.bot.send_message(
            message.channel,
            "Command format: `!roll XdY +/- Z`. `X` must be between 1-9, `Y` between 2-100 and `Z` between 1-99."
        )
        return
