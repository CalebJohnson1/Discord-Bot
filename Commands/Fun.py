import random
import randfacts
from jokeapi import Jokes

import discord
from discord.ext import commands

class Fun(commands.Cog, name="Fun.py"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='quote', aliases=["randomquote", "quotes"],
    usage='quote',
    description='Get a random quote!')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def quote(self, ctx):
        with open("Quotes.txt", "r") as m:
            quote = random.choice(m.readlines())
            embed = discord.Embed(title="Quote", description = f'***{quote}***', color=0xc0d4ff)
            await ctx.message.reply(embed=embed, mention_author = False)

    @commands.command(name='fact', aliases=["randfact", "randomfact","facts"],
    usage='fact',
    description='Generate a random fact from the internet')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def fact(self, ctx):
        fact = randfacts.get_fact()
        embed = discord.Embed(title="Fact", description = f'***{fact}***', color=0xc0d4ff)
        embed.set_footer(text="Disclaimer: Facts are not guaranteed to be true.")
        await ctx.message.reply(embed=embed, mention_author = False)

    @commands.command(name='joke', aliases=["jokes"],
    usage='joke',
    description='Generates a random joke from the internet')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def joke(self, ctx):
        disclaimers = ['If you find a joke offensive, please ignore it and move on', 'Do not take any of these jokes seriously', 'Might be a programming joke. If you understand it, congratulations!', 'Sorry if the joke is bad']
        j = Jokes()
        joke = j.get_joke(response_format = 'txt', blacklist = ['racist'])
        embed = discord.Embed(title="Joke", description = f'**{joke}**', color=0xc0d4ff)
        embed.set_footer(text=f'Disclaimer: {random.choice(disclaimers)}')
        await ctx.message.reply(embed=embed, mention_author = False)

    @joke.error
    async def joke_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(name='marvelQuote', aliases=["mq", "mquote"],
    usage='marvelQuote',
    description='Get a quote from the Marvel comics!')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def marvelQuote(self, ctx):
        with open("MarvelQuotes.txt", "r") as mq:
            mquote = random.choice(mq.readlines())
            embed = discord.Embed(title=(mquote.partition("name:")[2]),
                              description=mquote.split("name:")[0],
                              color=0xc0d4ff)
            embed.set_footer(text="Quote from the Marvel comics")
            await ctx.message.reply(embed=embed, mention_author = False)
            return

    @commands.command(name='8ball', usage='8ball <question>',
    description='This fortune telling Magic 8-Ball will answer any of your questions.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def _8ball(self, ctx, question = None):
        if question is None:
            await ctx.message.reply("Please input a question.\nUsage: **8ball <question>**")
            return

        member = ctx.author.display_name
        responses = [
            "Certainly!",
            "It is decidedly so",
            "Without a doubt",
            "Yes - definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "No",
            "Signs point to yes",
            "Reply hazy, try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful"]

        await ctx.message.reply(f"{random.choice(responses)}")

    @commands.command(name='generate', aliases=["gu", "generateusername"],
    usage='generate',
    description='Generates a random username.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def generate(self, ctx):
        with open("Adjectives.txt", "r") as adjectives:
            prefix = adjectives.read().strip(' \n').split('\n')
        with open("Nouns.txt", "r") as nouns:
            suffix = nouns.read().strip(' \n').split('\n')

        firstword = random.choice(prefix)
        secondword = random.choice(suffix)

        await ctx.message.reply(f"Generated Username: {firstword.title()}{secondword.title()}", mention_author = False)

    @commands.command(name='say', aliases=['speak'],
    usage='say <message>',
    description='Speak as the bot!',)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def say(self, ctx, *, message=None):
        if message is None:
            await ctx.message.reply("Please input a message.\nUsage: **say** <message>", mention_author = False)
            return

        await discord.Message.delete(ctx.message, delay=None)
        await ctx.message.reply(message.capitalize(), mention_author = False)

    @commands.command(name='reverse', aliases=["inverse", 'back'],
    usage='reverse <message>',
    description='Reverses the given message.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def reverse(self, ctx, *, message = None):
        if message is None:
            await ctx.message.reply("Please input a message.\nUsage: **reverse** <message>", mention_author = False)
            return

        await ctx.message.reply(message[::-1], mention_author = False)

def setup(bot):
    bot.add_cog(Fun(bot))
