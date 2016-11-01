from plugin import Plugin
import logging
import random
import re

log = logging.getLogger('discord')


class Replies(Plugin):
    responses = {
        "": [
            "Someone said my name?",
            "That's me!",
            "Who said that!?",
            "That's my name, don't wear it out.",
            "You called, {mention}?",
            "Whoa that's my name that's me NaNoBot!",
            "Need something, {mention}?"
        ],
        r"(h(i|ello|ey)|(what'?s |'?s)?up)": [
            "Hi there!",
            "Yo!",
            "Hi, {mention}!",
            "'Suuup?",
            "Hey!",
            "Hello hello!"
        ],
        r"(fuc?k (yo)?u|(piece of|pizza) shit|asshole|(i )?(hate|h8) (y(ou|a)|u))": [
            "That was just uncalled for...",
            "Yeah, up yours too, buddy!",
            "wow rude",
            "Your words wound me.",
            ":cry:",
            "Why the hostility, {mention}?"
        ],
        r"((i )?(love|luv|<3|❤) (y(ou|a)|u)|ily|(you'?re|u ?r|you( are)?) (the|da) best)": [
            "Awww :heart:",
            "Aw shucks :blush:",
            "Right back at you!",
            "love u too bby",
            ":eyes:",
            "NaNoBot x {mention} 4ever"
        ]
    }

    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return
        if re.search(r'\bnanobot\b', message.content, flags=re.IGNORECASE) \
                or self.bot.user.id in [user.id for user in message.mentions]:
            response = random.choice(self.responses[''])
            for key, resps in self.responses.items():
                if key == "":
                    continue
                if re.search(r'\b' + key + r'\b', message.content, flags=re.IGNORECASE):
                    response = random.choice(resps)
            response = response.replace("{mention}", message.author.mention)

            await self.bot.send_message(
                message.channel,
                response
            )
        return
