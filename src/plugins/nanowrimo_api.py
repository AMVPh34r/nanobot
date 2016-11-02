import xml.etree.ElementTree as ET
import aiohttp
from plugin import Plugin
from decorators import command


class NaNoWriMoAPI(Plugin):
    fancy_name = "NaNoWriMo API"

    @staticmethod
    async def get_commands(server):
        commands = [
            {
                'name': '!wordcount [username]',
                'description': 'Show the current wordcout for NaNo site user `[username]`.'
            }
        ]
        return commands

    @command(pattern='^!wordcount (.*)$')
    async def wordcount(self, message, args):
        username = args[0]
        url = "http://nanowrimo.org/wordcount_api/wc/{}".format(username)
        with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp_text = await resp.text()
                root = ET.fromstring(resp_text)
        if root.find('error') is not None:
            response = "Error: {}".format(
                root.find('error').text
            )
        else:
            response = "{name} has written {count} words so far!\n" \
                       "{name}'s profile: {url}".format(
                            name=root.find('uname').text,
                            count=root.find('user_wordcount').text,
                            url="http://nanowrimo.org/participants/{}".format(root.find('uname').text)
                        )

        await self.bot.send_message(message.channel, response)
