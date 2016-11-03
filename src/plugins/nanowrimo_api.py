import datetime
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
            },
            {
                'name': '!wordhistory [username]',
                'description': 'Show recent wordcount history for NaNo site user `[username]`.'
            }
        ]
        return commands

    @command(pattern='^!wordcount (.*)$')
    async def wordcount(self, message, args):
        username = args[0]
        api_url = "http://nanowrimo.org/wordcount_api/wc/{}".format(username)
        prof_url_template = "http://nanowrimo.org/participants/{}"
        response_template = "{name} has written {count} words so far!\n" \
                            "{name}'s profile: {url}"

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
                            name=root.find('uname').text,
                            count='{:,}'.format(
                                int(root.find('user_wordcount').text)
                            ),
                            url=prof_url_template.format(root.find('uname').text)
                        )

        await self.bot.send_message(message.channel, response)

    @command(pattern='^!wordhistory (.*)$')
    async def wordcount_history(self, message, args):
        username = args[0]
        api_url = "http://nanowrimo.org/wordcount_api/wchistory/{}".format(username)
        prof_url_template = "http://nanowrimo.org/participants/{}"
        response_template = "{name}'s recent word history:\n{history}" \
                            "Total words to date: `{count}`\n\n" \
                            "{name}'s profile: {url}"
        history_template = "{hdate}: `{hcount}`\n"
        history_str = ""

        with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                resp_text = await resp.text()
                root = ET.fromstring(resp_text)
        if root.find('error') is not None:
            response = "Error: {}".format(
                root.find('error').text
            )
        else:
            for entry in root.find('wordcounts')[-5:]:
                history_str += history_template.format(
                    hdate=datetime.datetime.strptime(
                        entry.find('wcdate').text,
                        '%Y-%m-%d'
                    ).strftime('%B %d'),
                    hcount='{:,}'.format(
                        int(entry.find('wc').text)
                    )
                )

            response = response_template.format(
                name=root.find('uname').text,
                count='{:,}'.format(
                    int(root.find('user_wordcount').text)
                ),
                history=history_str,
                url=prof_url_template.format(root.find('uname').text)
            )

        await self.bot.send_message(message.channel, response)
