from plugin import Plugin
from decorators import command


class WriteinObj(object):
    channel = None
    started_by = None
    is_active = False
    wordcounts = {}

    def __init__(self, channel, started_by):
        self.channel = channel
        self.started_by = started_by

    async def start(self):
        self.is_active = True

    async def finish(self):
        self.is_active = False

    async def submit_wordcount(self, user, count):
        if self.is_active:
            self.wordcounts[user.id] = count
        return self.is_active

    async def get_wordcount(self, user):
        if user.id in self.wordcounts.keys():
            return self.wordcounts[user.id]
        else:
            return None

    async def leaderboard(self):
        return sorted(self.wordcounts.items(), key=lambda x: x[1], reverse=True)


class Writein(Plugin):
    fancy_name = "Writeins"

    writeins = {}

    @staticmethod
    async def get_commands(server):
        commands = [
            {
                'name': '!writein start',
                'description': 'Begin a writein.'
            },
            {
                'name': '!writein report [x]',
                'description': 'Report your wordcount for the writein.'
            },
            {
                'name': '!writein check',
                'description': 'Check your current submitted wordcount.'
            },
            {
                'name': '!writein leaderboard',
                'description': 'Show a leaderboard of wordcounts for the current writein.'
            },
            {
                'name': '!writein finish',
                'description': 'Complete the writein. Only the writein starter can use this command.'
            }
        ]
        return commands

    async def get_writein(self, channel):
        if channel in self.writeins.keys():
            writein = self.writeins[channel]
            if writein.is_active:
                return writein
            else:
                del self.writeins[channel]
        return None

    async def generate_leaderboard(self, writein):
        leaderboard = await writein.leaderboard()
        record_template = "**{name}**: `{count}`"
        response = ""
        for record in leaderboard:
            user = await self.bot.get_user_info(record[0])
            count = record[1]
            response += record_template.format(name=user.name, count=count) + "\n"
        return response

    @command(pattern='^!writein start$')
    async def writein_start(self, message, args):
        writein = await self.get_writein(message.channel)
        if writein:
            response = "There is already a writein in progress, started by {started_by}.\n" \
                       "To complete it, {started_by} can issue the command `!writein finish`.".format(
                            started_by=writein.started_by.name
                        )
            await self.bot.send_message(message.channel, response)
            return

        del writein
        writein = WriteinObj(message.channel, message.author)
        await writein.start()
        self.writeins[message.channel] = writein
        response = "{} started a writein! Let's get writing!\n" \
                   "Be sure to regularly submit your wordcount for this writein with `!writein report [count]`"\
            .format(message.author.name)

        await self.bot.send_message(message.channel, response)

    @command(pattern='^!writein report ([0-9]*)$')
    async def writein_report(self, message, args):
        count = args[0]
        writein = await self.get_writein(message.channel)
        if not writein or not writein.is_active:
            response = "There's currently no active writein.\n" \
                       "To start one, send `!writein start`."
            await self.bot.send_message(message.channel, response)
            return

        await writein.submit_wordcount(message.author, count)
        response = "{}: Successfully updated your wordcount for this writein to {}!".format(
            message.author.mention, count
        )
        await self.bot.send_message(message.channel, response)

    @command(pattern='^!writein check$')
    async def writein_check(self, message, args):
        writein = await self.get_writein(message.channel)
        if not writein or not writein.is_active:
            response = "There's currently no active writein.\n" \
                       "To start one, send `!writein start`."
            await self.bot.send_message(message.channel, response)
            return

        count = await writein.get_wordcount(message.author)
        if count is None:
            response = "{}, you haven't submitted your wordcount yet! Do so with `!writein report [count]`.".format(
                message.author.mention
            )
        else:
            response = "{}, your current wordcount is {}".format(
                message.author.mention, count
            )
        await self.bot.send_message(message.channel, response)

    @command(pattern='^!writein leaderboard$')
    async def leaderbaord(self, message, args):
        writein = await self.get_writein(message.channel)
        if not writein or not writein.is_active:
            response = "There's currently no active writein.\n" \
                       "To start one, send `!writein start`."
            await self.bot.send_message(message.channel, response)
            return

        response = "Here's the leaderboard for the current writein:\n{}".format(
            await self.generate_leaderboard(writein)
        )
        await self.bot.send_message(message.channel, response)

    @command(pattern='^!writein finish$')
    async def writein_finish(self, message, args):
        writein = await self.get_writein(message.channel)
        if not writein or not writein.is_active:
            response = "There's currently no active writein.\n" \
                       "To start one, send `!writein start`."
            await self.bot.send_message(message.channel, response)
            return

        if message.author.id != writein.started_by.id:
            response = "Sorry, this writein was started by {}, only they may close it.".format(
                writein.started_by.mention
            )
            await self.bot.send_message(message.channel, response)
            return

        await writein.finish()
        response = "Writein complete! Here is the final leaderboard:\n{}".format(
            await self.generate_leaderboard(writein)
        )

        del self.writeins[message.channel]
        del writein

        await self.bot.send_message(message.channel, response)
