from plugin import Plugin
import discord
import os
import logging

logs = logging.getLogger('discord')


class BotGame(Plugin):
    is_global = True
    game_name = os.getenv("BOT_GAME")
    game = None

    async def on_ready(self):
        logs.info("GAME CHANGE: {}".format(
            self.game_name
        ))

        if self.game_name:
            self.game = discord.Game(name=self.game_name)
        await self.bot.change_presence(game=self.game)
        return
