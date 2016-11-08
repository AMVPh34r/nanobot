import os
import random
import aiohttp
from plugin import Plugin
from decorators import command

BHL_API_KEY = os.getenv('BHL_API_KEY')


class Thesaurus(Plugin):
    fancy_name = "Thesaurus"

    @staticmethod
    async def get_commands(server):
        commands = [
            {
                'name': '!synonym/syn [word]',
                'description': 'Show some synonyms for the given `[word]`.'
            }
        ]
        return commands

    @command(pattern='^!syn(onym)? (.*)$')
    async def synonym(self, message, args):
        word = args[1]
        syn_list = []
        api_url = "http://words.bighugelabs.com/api/2/{key}/{word}/json".format(
            key=BHL_API_KEY,
            word=word
        )
        response_template = "Here are a few synonyms for `{word}`:\n" \
                            "```\n{syns}\n```"
        word_template = "{word} ({type})"

        with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                data = await resp.json()
        if data is None:
            response_template = "Sorry! I was unable to find any synonyms for `{word}`!"
            response = response_template.format(word=word)
            await self.bot.send_message(message.channel, response)
            return

        for w_type in data.keys():
            if "syn" in data[w_type]:
                syn_list += data[w_type]['syn']
        random.shuffle(syn_list)

        response = response_template.format(
            word=word,
            syns=', '.join(syn_list[:10])
        )

        await self.bot.send_message(message.channel, response)
