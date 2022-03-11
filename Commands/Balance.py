import sqlite3

import discord
from discord.ext import commands


class Balance(commands.Cog, name="Balance.py"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.author.bot:
            return

        db = sqlite3.connect('database.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT UserID FROM player WHERE UserID = {message.author.id}")
        result = cursor.fetchone()

        if result is None:
            sql = "INSERT INTO player(UserID, Balance, Points, isStarted, Shards) VALUES(?, ?, ?, ?, ?)"
            val = (message.author.id, 0, 0, False, 0)
            cursor.execute(sql, val)
            db.commit()

    @commands.command(name='credits', aliases=["cred", "creds"],
    usage='m!credits',
    description='Checks how many Credits you currently have.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def credits(self, ctx, user: discord.User = None):
        if user is not None:
            db = sqlite3.connect('database.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT UserID, Balance FROM player WHERE UserID = {ctx.author.id}")
            result = cursor.fetchone()
            embed = discord.Embed(title=f"{ctx.author.display_name}'s Credits: {int(result[1]):,} ",
                                color=0xc0d4ff)
            # icon = "https://i.imgur.com/IfvzrTH.png"
            # embed.set_thumbnail(url=icon)
            embed.set_author(name="Credits")
            await ctx.message.reply(embed=embed, mention_author = False)
            cursor.close()
            db.close()

        elif user is None:
            db = sqlite3.connect('database.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT UserID, Balance FROM player WHERE UserID = {ctx.author.id}")
            result = cursor.fetchone()
            if result is None:
                return
            else:
                embed = discord.Embed(title=f"{ctx.author.display_name}'s Credits: {int(result[1]):,} ",
                                color=0xc0d4ff)
                # icon = "https://i.imgur.com/IfvzrTH.png"
                # embed.set_thumbnail(url=icon)
                embed.set_author(name="Credits")
                await ctx.message.reply(embed=embed, mention_author = False)
            cursor.close()
            db.close()

    @credits.error
    async def credits_error(self, error):
        print(error)

    @commands.command(name='points', usage='m!points',
    description='Checks how many Points you currently have.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def points(self, ctx, user: discord.User = None):
        if user is not None:
            db = sqlite3.connect('database.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT UserID, Points FROM player WHERE UserID = {ctx.author.id}")
            result = cursor.fetchone()
            embed = discord.Embed(title=f"{ctx.author.display_name}'s Points: {int(result[1]):,} ",
                                color=0xc0d4ff)
            # icon = "https://i.imgur.com/HA7W10l.png"
            # embed.set_thumbnail(url=icon)
            embed.set_author(name="Points")
            await ctx.message.reply(embed=embed, mention_author = False)
            cursor.close()
            db.close()

        elif user is None:
            db = sqlite3.connect('database.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT UserID, Points FROM player WHERE UserID = {ctx.author.id}")
            result = cursor.fetchone()
            if result is None:
                return
            else:
                embed = discord.Embed(title=f"{ctx.author.display_name}'s Points: ",
                                      description=f"You currently have {int(result[1]):,} Points.",
                                      color=0xc0d4ff)
                # icon = "https://i.imgur.com/HA7W10l.png"
                # embed.set_thumbnail(url=icon)
                await ctx.message.reply(embed=embed, mention_author = False)
            cursor.close()
            db.close()

    @points.error
    async def points_error(self, error):
        print(error)

    @commands.command(name='shards', usage='m!shards',
    description='Checks how many Shards you currently have.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def shards(self, ctx, user: discord.User = None):
        if user is not None:
            db = sqlite3.connect('database.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT UserID, Shards FROM player WHERE UserID = {ctx.author.id}")
            result = cursor.fetchone()
            embed = discord.Embed(title=f"{ctx.author.display_name}'s Shards: {int(result[1]):,} ",
                                color=0xc0d4ff)
            # icon = "https://i.imgur.com/IfvzrTH.png"
            # embed.set_thumbnail(url=icon)
            embed.set_author(name="Shards")
            await ctx.message.reply(embed=embed, mention_author = False)
            cursor.close()
            db.close()

        elif user is None:
            db = sqlite3.connect('database.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT UserID, isStarted, Shards FROM player WHERE UserID = {ctx.author.id}")
            result = cursor.fetchone()
            if not result[1]:
                await ctx.message.reply("You must have started using **m!start** if you wish to see your shards")
            else:
                embed = discord.Embed(title=f"{ctx.author.display_name}'s Shards: {int(result[2]):,} ",
                                color=0xc0d4ff)
                # icon = "https://i.imgur.com/IfvzrTH.png"
                # embed.set_thumbnail(url=icon)
                embed.set_author(name="Shards")
                await ctx.message.reply(embed=embed, mention_author = False)
            cursor.close()
            db.close()


def setup(bot):
    bot.add_cog(Balance(bot))
