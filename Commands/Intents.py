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

        if message.channel.id != 943675388616384573:
            return

        listener = ["may"]

        terms = ["hows it goin", "hows it going", "hows it hanging", "hows it hangin",
                 "hows it going helpful", "how are you", "how is your day", "hows your day"]
        someprefixes = ["give me", "give us", "gimme", "i need", "tell me", "i want", "needs"]

        for word in terms:
            for wordsuffix in listener:
                choices = ["I'm fine, thanks for asking!", "Very well, thanks!", "Not bad, what about you?",
                           "Fine, and you?", f"Hello {message.author.display_name}, I'm great!"]
                if message.content.lower().count(word) and message.content.lower().count(wordsuffix):
                    await message.reply(f"{random.choice(choices)}", mention_author = False)
                    return

        pokefacts = ["pokemon", "pokémon"]
        pokefactss = ["fact"]
        with open("PokemonFacts.txt", "r") as f:
            pokemonfacts = random.choice(f.readlines())
        for pokemessage in pokefacts:
            for messagesuf in listener:
                for givemee in someprefixes:
                    for pokemessagee in pokefactss:
                        if message.content.lower().count(pokemessage) and message.content.lower().count(messagesuf) and\
                                message.content.lower().count(pokemessagee) or message.content.lower().count(pokemessage)\
                                and message.content.lower().count(givemee) and message.content.lower().count(pokemessagee):
                            await message.reply(pokemonfacts, mention_author = False)
                            return

        quotess = ["quote"]
        with open("Quotes.txt", "r") as m:
            quotes = random.choice(m.readlines())
        for qmessage in quotess:
            for qmessagesuf in listener:
                for givemee in someprefixes:
                    if message.content.lower().count(qmessage) and message.content.lower().count(qmessagesuf) or \
                            message.content.lower().count(qmessage) and message.content.lower().count(givemee):
                        await message.reply(quotes, mention_author = False)
                        return

        factss = ["fact"]
        with open("Facts.txt", "r") as f:
            facts = random.choice(f.readlines())
        for fmessage in factss:
            for messagesuf in listener:
                for givemee in someprefixes:
                    if message.content.lower().count(fmessage) and message.content.lower().count(messagesuf) or \
                            message.content.lower().count(fmessage) and message.content.lower().count(givemee):
                        await message.reply(facts, mention_author = False)
                        return

        jokess = ["jokes", "joke"]
        with open("Jokes.txt", "r") as j:
            jokes = random.choice(j.readlines())
        for joke in jokess:
            for jokesuf in listener:
                for givemee in someprefixes:
                    if message.content.lower().count(joke) and message.content.lower().count(jokesuf) or \
                            message.content.lower().count(joke) and message.content.lower().count(givemee):
                        await message.reply(jokes, mention_author = False)
                        return

        nice = ["good job", "great job", "excellent", "fantastic", "appreciate"]

        for nicee in nice:
            for niceee in listener:
                if message.content.lower().count(nicee) and message.content.lower().count(niceee):
                    await message.reply(f"Thank you, {message.author.display_name.title()}!", mention_author = False)
                    return

        thankYouIntents = ["thank you"]
        thankYouResponses = [f"No problem, {message.author.display_name.title()}!", 
                             "My pleasure!"]
        for i in listener:
            for j in thankYouIntents:
                if message.content.lower().count(i) and message.content.lower().count(j):
                    await message.reply(f"{random.choice(thankYouResponses)}", mention_author = False)

        bookResponse = ["random book", "book to read", "read a book", "book please"]
        verbs = ['I choose', "I've picked", "I've selected"]
        randVerb = random.choice(verbs)
        books = {
            'Children of Blood and Bone': 'Tomi Adeyemi',
            'Legendborn': 'Tracy Deonn',
            '1984': 'George Orwell',
            'The Hate U Give': 'Angie Thomas',
            'Pride and Prejudice': 'Jane Austen',
            'Brave New World': 'Aldous Huxley',
            'Renegades': 'Marissa Meyer',
            'Hitchhikers Guide to the Galaxy': 'Douglas Adams',
            'Animal Farm': 'George Orwell',
            'Les Miserables': 'Victor Hugo',
            'The Da Vinci Code': 'Dan Brown',
            'Memoirs Of A Geisha': 'Arthur Golden',
            'Where The Crawdads Sing': 'Delia Owens',
            'Hunger Games': 'Suzanne Collins',
            'Percy Jackson': 'Rick Riordan'
        }
        randomBook = random.choice(list(books))
        author = books[randomBook]
        for responses in bookResponse:
            for responsess in listener:
                if message.content.lower().count(responses) and message.content.lower().count(responsess):
                    await message.reply(f"{randVerb} {randomBook} by {author} to be the next for book you to read.")
                    return


def setup(bot):
    bot.add_cog(Intents(bot))
