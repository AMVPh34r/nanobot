import discord
import logging
from plugin_manager import PluginManager

APP_NAME = "NaNoBot"
APP_VERSION = "1.5.1"
APP_AUTHOR = "Alex Schaeffer"

log = logging.getLogger('discord')


class ChatBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_all()
        self.last_messages = []
        self.__name__ = APP_NAME
        self.__version__ = APP_VERSION
        self.__author__ = APP_AUTHOR
        self.__copyright__ = "Copyright (c){} {}".format(
            '2016-2020', self.__author__
        )

    def run(self, *args):
        self.loop.run_until_complete(self.start(*args))

    async def on_ready(self):
        for plugin in self.plugins:
            self.loop.create_task(plugin.on_ready())

    async def get_plugins(self, server):
        plugins = await self.plugin_manager.get_all(server)
        return plugins

    async def send_message(self, channel, *args, **kwargs):
        return await channel.send(*args, **kwargs)

    async def on_message(self, message):
        if isinstance(message.channel, discord.abc.PrivateChannel):
            return

        server = message.guild

        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin._on_message(message))

    async def on_message_edit(self, before, after):
        if isinstance(before.channel, discord.abc.PrivateChannel):
            return

        server = after.guild
        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_message_edit(before, after))

    async def on_message_delete(self, message):
        if isinstance(message.channel, discord.abc.PrivateChannel):
            return

        server = message.guild
        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_message_delete(message))

    async def on_channel_create(self, channel):
        if isinstance(channel, discord.abc.PrivateChannel):
            return

        server = channel.guild
        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_channel_create(channel))

    async def on_channel_update(self, before, after):
        if isinstance(before, discord.abc.PrivateChannel):
            return

        server = after.guild
        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_channel_update(before, after))

    async def on_channel_delete(self, channel):
        if isinstance(channel, discord.abc.PrivateChannel):
            return

        server = channel.guild
        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_channel_delete(channel))

    async def on_member_join(self, member):
        server = member.guild
        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_member_join(member))

    async def on_member_remove(self, member):
        server = member.guild
        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_member_remove(member))

    async def on_member_update(self, before, after):
        server = after.guild
        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_member_update(before, after))

    async def on_server_update(self, before, after):
        server = after
        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_server_update(before, after))

    async def on_server_role_create(self, server, role):
        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_server_role_create(server, role))

    async def on_server_role_delete(self, server, role):
        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_server_role_delete(server, role))

    async def on_server_role_update(self, before, after):
        server = None
        for s in self.guilds:
            if after.id in map(lambda r: r.id, s.roles):
                server = s
                break

        if server is None:
            return

        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_server_role_update(before, after))

    async def on_voice_state_update(self, before, after):
        if after is None and before is None:
            return
        elif after is None:
            server = before.guild
        elif before is None:
            server = after.guild
        else:
            server = after.guild

        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_voice_state_update(before, after))

    async def on_member_ban(self, member):
        server = member.guild
        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_member_ban(member))

    async def on_member_unban(self, member):
        server = member.guild
        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_member_unban(member))

    async def on_typing(self, channel, user, when):
        if isinstance(channel, discord.abc.PrivateChannel):
            return

        server = channel.guild
        enabled_plugins = await self.get_plugins(server)
        for plugin in enabled_plugins:
            self.loop.create_task(plugin.on_typing(channel, user, when))
