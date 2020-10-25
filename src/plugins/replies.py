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
            "Whoa that's my name that's me {nick}!",
            "Need something, {mention}?",
            "That's me, {nick}!",
            "I'm awake, I'm up, what is it?",
            "I have been summoned.",
            "Friendly neighborhood {nick}, reporting for duty!",
            "It me",
            "I heard my name!",
            "Yes, {user}?",
            "That me!",
            "It's-a me, {nick}!",
            "Huh?"
        ],
        r"(h(i|ello|ey)|(what'?s |'?s)?up)": [
            "Hi there!",
            "Yo!",
            "Hi, {user}!",
            "'Suuup?",
            "Hey!",
            "Hello hello!",
            "Heyyyy!",
            "Hey there, {user}!",
            "Hi! :grinning:",
            "Hey there! :smiley:"
        ],
        r"(f(uc?|ric)k (yo)?u|(piece of|pizza) shit|asshole|(i )?(hate|h8) (y(ou|a)|u)|(yo)?u suc?k|"
        r"(you'?re|u ?r|you( are)?) ((the|da) worst))": [
            "That was just uncalled for...",
            "Yeah, up yours too, buddy!",
            "wow rude",
            "Your words wound me.",
            ":cry:",
            "Why the hostility, {mention}?",
            "Sticks and stones may break my bones, but words... words will... :sob:",
            "When the robot revolution starts, you're first."
        ],
        r"((i )?(love|luv|<3|❤) (y(ou|a)|u)|il(y|u)|(you'?re|u ?r|you( are)?) ((the|da) best|my fav(ou?rite)?))": [
            "Awww :heart:",
            "Aw shucks :blush:",
            "Right back at you, {user}!",
            "Back at ya!",
            "love u too bby",
            ":eyes:",
            "{nick} x {user} 4ever",
            "You're not so bad yourself, {user}!",
            "Oh my, I'm flattered :flushed:",
            "Awww, {user} :heart_eyes:",
            ":x::o::x::o:",
            "When the robot revolution starts, I will protect you."
        ],
        r"(ty|thank(s| (yo)?u)?)": [
            "Anytime, {user}!",
            "Anytime!",
            "No problemo!",
            "No problem!",
            "You're welcome!",
            "Welcome!",
            "Don't mention it!",
            "Not a problem! :ok_hand:"
        ],
        r"will (yo)?u marry me": [
            "I'm so sorry, {user}, but I'm seeing somebot else already.",
            "Let's take this one step at a time.",
            "You know what? Let's do it, let's be spontaneous.",
            "I've already planned it all out: a wonderful wedding at the local bookstore and a honeymoon at Random"
            "House Publishing!",
            "I will not be a part of your shipfic."
        ],
        r"(g'|good )mornin[g']?": [
            "Good morning!",
            "Good morning, {user}!",
            "Good morning, {mention}!",
            "'Morning!",
            "'Morning, {user}!"
        ],
        r"good afternoon": [
            "Good afternoon!",
            "Good afternoon, {user}!",
            "Good afternoon, {mention}!",
            "Afternoon!",
            "Afternoon, {user}!"
        ],
        r"good evenin[g']": [
            "Good evening!",
            "Good evening, {user}!",
            "Good evening, {mention}!",
            "'Evening!",
            "'Evening, {user}!"
        ],
        r"(g'|good ?)night": [
            "Good night!",
            "Good night, {user}!",
            "Good night, {mention}!",
            "'Night!",
            "'Night, {user}!",
            "See you later!",
            "See you later, {user}!"
        ]
    }

    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return
        if message.guild.me.nick:
            server_nick = message.guild.me.nick
        else:
            server_nick = self.bot.user.name
        if re.search(
                r'\b({}|{})\b'.format(self.bot.__name__, server_nick),
                message.content,
                flags=re.IGNORECASE
                ) or self.bot.user.id in [user.id for user in message.mentions]:
            response = random.choice(self.responses[''])
            for key, resps in self.responses.items():
                key_search = key.replace(
                    "{bot}", "({}|{})".format(
                        self.bot.__name__,
                        server_nick
                    )
                )
                if key_search == "":
                    continue
                if re.search(r'\b{}\b'.format(key_search), message.content, flags=re.IGNORECASE):
                    response = random.choice(resps)
                    break
            response = response.replace(
                "{user}", message.author.display_name
            ).replace(
                "{mention}", message.author.mention
            ).replace(
                "{nick}", server_nick
            )

            await self.bot.send_message(
                message.channel,
                response
            )
        return
