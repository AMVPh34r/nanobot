from plugin import Plugin
import logging

log = logging.getLogger('discord')

async def get_help_info(self, server):
    if self.fancy_name is None:
        self.fancy_name = type(self).__name__

    commands = []
    if hasattr(self, "get_commands"):
        commands += await self.get_commands(server)
    else:
        for cmd in self.commands.values():
            commands.append(cmd.info)
    data = {
        'name': type(self).__name__,
        'fancy_name': self.fancy_name,
        'commands': commands
    }
    return data


class Help(Plugin):
    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)
        # Patch the Plugin class
        Plugin.get_help_info = get_help_info

    async def generate_help(self, server):
        enabled_plugins = await self.bot.plugin_manager.get_all(server)
        enabled_plugins = sorted(enabled_plugins, key=lambda p: type(p).__name__)

        data = []
        for plugin in enabled_plugins:
            if not isinstance(plugin, Help):
                help_info = await plugin.get_help_info(server)
                data.append(help_info)

        return self.render_message(data)

    @staticmethod
    def render_message(data):
        messages = [""]
        for plugin in data:
            if plugin['commands']:
                message = "**{}**\n".format(plugin['fancy_name'])
                if len(messages[-1] + message) > 2000:
                    messages.append(message)
                else:
                    messages[-1] += message
            for cmd in plugin['commands']:
                message = "   **{}** - {}\n".format(cmd['name'], cmd.get('description', ''))
                if len(messages[-1] + message) > 2000:
                    messages.append(message)
                else:
                    messages[-1] += message
        return messages

    async def on_message(self, message):
        if message.content == '!help':
            server = message.server
            messages = await self.generate_help(server)
            if messages == [""]:
                messages = ["There's no command to show"]
            destination = message.channel
            for msg in messages:
                await self.bot.send_message(destination, msg)
        return
