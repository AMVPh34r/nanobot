import asyncio
from plugin import Plugin
from decorators import command


class TimerObj(object):
    def __init__(self, channel, length, reminder=None):
        self.channel = channel
        self.length = int(length) * 60
        self.reminder = int(reminder) * 60 if reminder is not None else None
        self.remaining = self.length
        self.is_active = False

    async def time_remaining(self):
        if self.remaining < 60:
            return self.remaining, "second{}".format("" if self.remaining == 1 else "s")
        rem_min = int(round(self.remaining/60))
        return rem_min, "minute{}".format("" if rem_min == 1 else "s")


class Timer(Plugin):
    fancy_name = "Timers"

    timers = {}

    @staticmethod
    async def get_commands(server):
        commands = [
            {
                'name': '!timer [x]',
                'description': 'Start an `[x]`-minute timer.'
            },
            {
                'name': '!timer check',
                'description': 'Check if a timer is running, show how many minutes remain if so.'
            },
            {
                'name': '!timer cancel',
                'description': 'Cancel an existing timer.'
            }
        ]
        return commands

    async def get_timer(self, channel):
        if channel.id in self.timers.keys():
            timer = self.timers[channel.id]
            if timer.is_active:
                return timer
            else:
                del self.timers[channel.id]
        return None

    async def timer_run(self, timer):
        timer.is_active = True
        while timer.remaining > 0:
            timer.remaining -= 1
            if timer.reminder is not None and timer.remaining == timer.reminder:
                await self.timer_reminder(timer)
            await asyncio.sleep(1)
        timer.is_active = False
        await self.timer_complete(timer)

    async def timer_reminder(self, timer):
        remaining = await timer.time_remaining()
        response = "Reminder! {} {} remaining!".format(
            remaining[0],
            remaining[1]
        )
        timer.reminder = None

        await self.bot.send_message(timer.channel, response)

    async def timer_complete(self, timer):
        response = "Ding! {}-minute timer completed!{}".format(
            timer.length // 60,
            " That was fast!" if timer.length == 0 else ""
        )
        await self.bot.send_message(timer.channel, response)
        del self.timers[timer.channel.id]
        del timer

    @command(pattern='^!timer ([0-9]*)$')
    async def timer_start(self, message, args):
        length = int(args[0])
        timer = await self.get_timer(message.channel)
        if timer:
            remaining = await timer.time_remaining()
            response = "There is already a {}-minute timer running with {} {} left.\n" \
                       "You can cancel it with `!timer cancel`".format(
                            timer.length // 60,
                            remaining[0],
                            remaining[1]
                        )
            await self.bot.send_message(message.channel, response)
            return

        del timer
        if length < 0:
            response = "Sorry, you can't set a timer in the past!"
            await self.bot.send_message(message.channel, response)
            return

        timer = TimerObj(message.channel, length)
        self.timers[message.channel.id] = timer
        self.bot.loop.create_task(self.timer_run(timer))
        response = "Started a {}-minute timer.".format(length)

        await self.bot.send_message(message.channel, response)

    @command(pattern='^!timer ([0-9]*) ([0-9]*)$')
    async def timer_reminder_start(self, message, args):
        length = int(args[0])
        reminder = int(args[1])
        timer = await self.get_timer(message.channel)
        if timer:
            remaining = await timer.time_remaining()
            response = "There is already a {}-minute timer running with {} {} left.\n" \
                       "You can cancel it with `!timer cancel`".format(
                            timer.length // 60,
                            remaining[0],
                            remaining[1]
                        )
            await self.bot.send_message(message.channel, response)
            return

        del timer
        if reminder > length:
            response = "You can't set a reminder greater than the timer's length!"
            await self.bot.send_message(message.channel, response)
            return
        if length < 0 or reminder < 0:
            response = "Sorry, you can't set a timer in the past!"
            await self.bot.send_message(message.channel, response)
            return

        timer = TimerObj(message.channel, length, reminder)
        self.timers[message.channel.id] = timer
        self.bot.loop.create_task(self.timer_run(timer))
        response = "Started a {}-minute timer.".format(length)

        await self.bot.send_message(message.channel, response)

    @command(pattern='^!timer check$')
    async def timer_check(self, message, args):
        timer = await self.get_timer(message.channel)
        if timer:
            remaining = await timer.time_remaining()
            response = "There is a {}-minute timer running with {} {} left.".format(
                            timer.length // 60,
                            remaining[0],
                            remaining[1]
                        )
            await self.bot.send_message(message.channel, response)
            return
        response = "There is currently no timer running. You can create one with `!timer [minutes]`"
        await self.bot.send_message(message.channel, response)

    @command(pattern='^!timer cancel$')
    async def timer_cancel(self, message, args):
        timer = await self.get_timer(message.channel)
        if timer:
            del self.timers[message.channel.id]
            response = "{}-minute timer canceled.".format(timer.length//60)
            del timer
        else:
            response = "There is no timer to cancel."
        await self.bot.send_message(message.channel, response)
