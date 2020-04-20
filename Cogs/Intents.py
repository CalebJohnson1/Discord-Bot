import random
import discord

from discord.ext import commands


class Intents(commands.Cog, name='Intents'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.author.bot:
            return
            
        if isinstance(message.channel, discord.DMChannel):
            return

        suffix = ["may"]

        terms = ["hows it goin", "hows it going", "hows it hanging", "hows it hangin",
                 "hows it going helpful", "how are you", "how is your day", "hows your day"]
        # someprefixes = ["give me", "give us", "gimme", "i need", "tell me", "i want", "needs"]

        for word in terms:
            for wordsuffix in suffix:
                choices = ["I'm fine, thanks for asking!", "Very well, thanks!", "Not bad, what about you?",
                           "Fine, and you?", f"Hello {message.author.display_name}, I'm great!"]
                if message.content.lower().count(word) and message.content.lower().count(wordsuffix):
                    await message.channel.send(f"{random.choice(choices)}")
                    return

        """pokefacts = ["pokemon", "pokémon"]
        pokefactss = ["fact"]
        with open("PokemonFacts.txt", "r") as f:
            pokemonfacts = random.choice(f.readlines())
        for pokemessage in pokefacts:
            for messagesuf in suffix:
                for givemee in someprefixes:
                    for pokemessagee in pokefactss:
                        if message.content.lower().count(pokemessage) and message.content.lower().count(messagesuf) and\
                                message.content.lower().count(pokemessagee) or message.content.lower().count(pokemessage)\
                                and message.content.lower().count(givemee) and message.content.lower().count(pokemessagee):
                            await message.channel.send(pokemonfacts)
                            return

        quotess = ["quote"]
        with open("Quotes.txt", "r") as m:
            quotes = random.choice(m.readlines())
        for qmessage in quotess:
            for qmessagesuf in suffix:
                for givemee in someprefixes:
                    if message.content.lower().count(qmessage) and message.content.lower().count(qmessagesuf) or \
                            message.content.lower().count(qmessage) and message.content.lower().count(givemee):
                        await message.channel.send(quotes)
                        return

        factss = ["fact"]
        with open("Facts.txt", "r") as f:
            facts = random.choice(f.readlines())
        for fmessage in factss:
            for messagesuf in suffix:
                for givemee in someprefixes:
                    if message.content.lower().count(fmessage) and message.content.lower().count(messagesuf) or \
                            message.content.lower().count(fmessage) and message.content.lower().count(givemee):
                        await message.channel.send(facts)
                        return

        jokess = ["jokes", "joke"]
        with open("Jokes.txt", "r") as j:
            jokes = random.choice(j.readlines())
        for joke in jokess:
            for jokesuf in suffix:
                for givemee in someprefixes:
                    if message.content.lower().count(joke) and message.content.lower().count(jokesuf) or \
                            message.content.lower().count(joke) and message.content.lower().count(givemee):
                        await message.channel.send(jokes)
                        return

        nice = ["nice", "good job", "great job", "excellent", "fantastic", "appreciate"]

        for nicee in nice:
            for niceee in suffix:
                if message.content.lower().count(nicee) and message.content.lower().count(niceee):
                    await message.channel.send(f"Thank you, {message.author.display_name.title()}!")
                    return"""


def setup(bot):
    bot.add_cog(Intents(bot))
    print('Intents Loaded.')
