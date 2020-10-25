import os
import aiohttp
from plugin import Plugin
from decorators import command

IMGUR_ID = os.getenv('IMGUR_ID')
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_SEARCH_ID = os.getenv("GOOGLE_SEARCH_ID")

NOT_FOUND = "Sorry, I couldn't find anything."


class Search(Plugin):
    fancy_name = "Web Search"

    @staticmethod
    async def get_commands(server):
        commands = [
            {
                'name': '!google [search_term]',
                'description': 'Search Google'
            },
            {
                'name': '!youtube [search_term]',
                'description': 'Search YouTube'
            },
            {
                'name': '!imgur [search_term]',
                'description': 'Search Imgur'
            }
        ]
        return commands

    @command(pattern='^!google (.*)$')
    async def google(self, message, args):
        query = args[0]
        url = "https://www.googleapis.com/customsearch/v1"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={"q": query,
                                                "cx": GOOGLE_SEARCH_ID,
                                                "key": GOOGLE_API_KEY}) as resp:
                data = await resp.json()
        if data['items']:
            result = data['items'][0]
            response = "{}\n`{}`".format(
                result['link'],
                result['snippet']
            )
        else:
            response = NOT_FOUND

        await self.bot.send_message(message.channel, response)

    @command(pattern='^!youtube (.*)$')
    async def youtube(self, message, args):
        query = args[0]
        url = "https://www.googleapis.com/youtube/v3/search"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={"type": "video",
                                                "q": query,
                                                "part": "snippet",
                                                "key": GOOGLE_API_KEY}) as resp:
                data = await resp.json()
        if data['items']:
            video = data['items'][0]
            response = "https://youtu.be/" + video['id']['videoId']
        else:
            response = NOT_FOUND

        await self.bot.send_message(message.channel, response)

    @command(pattern='^!imgur (.*)$')
    async def imgur(self, message, args):
        query = args[0]
        url = "https://api.imgur.com/3/gallery/search/viral"
        headers = {"Authorization": "Client-ID " + IMGUR_ID}
        async with aiohttp.ClientSession() as session:
            async with session.get(url,
                                   params={"q": query},
                                   headers=headers) as resp:
                data = await resp.json()

        if data['data']:
            result = data['data'][0]
            response = result['link']
        else:
            response = NOT_FOUND

        await self.bot.send_message(message.channel, response)
