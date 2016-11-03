import os
import xml.etree.ElementTree as ET
import aiohttp
from plugin import Plugin
from decorators import command

BTN_API_KEY = os.getenv('BTN_API_KEY')


class NameGenerator(Plugin):
    fancy_name = "Name Generator"

    api_url_template = "http://www.behindthename.com/api/random.php?" \
                       "key={key}&number={num}&randomsurname={surname}&usage=eng"

    @staticmethod
    async def get_commands(server):
        commands = [
            {
                'name': '!randomname',
                'description': 'Generate a random first and last name.'
            }
        ]
        return commands

    @command(pattern='^!randomname$')
    async def random_name(self, message, args):
        api_url = self.api_url_template.format(
            key=BTN_API_KEY,
            num=1,
            surname="yes"
        )
        response_template = "{mention}, here's a name for you: `{firstname} {lastname}`"

        with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                resp_text = await resp.text()
                root = ET.fromstring(resp_text)
        if root.find('error') is not None:
            response = "Error: {}".format(
                root.find('error').text
            )
        else:
            response = response_template.format(
                mention=message.author.mention,
                firstname=root.find('names')[0].text,
                lastname=root.find('names')[1].text
            )

        await self.bot.send_message(message.channel, response)
