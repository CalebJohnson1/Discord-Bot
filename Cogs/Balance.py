import sqlite3

import discord
from discord.ext import commands


class Balance(commands.Cog, name="Balance.py"):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1.0, 3.0, commands.BucketType.user)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
            return

        bucket = self._cd.get_bucket(message)
        retry_after = bucket.update_rate_limit()

        db = sqlite3.connect('database.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT UserID FROM money WHERE UserID = {message.author.id}")
        result = cursor.fetchone()

        if result is None:
            sql = "INSERT INTO money(UserID, Balance, Points) VALUES(?, ?, ?)"
            val = (message.author.id, 0, 0)
            cursor.execute(sql, val)
            db.commit()
        else:
            cursor.execute(
                f"SELECT UserID, Balance FROM money WHERE UserID = {message.author.id}")
            result1 = cursor.fetchone()
            balance = int(result1[1])
            if retry_after:
                sql = "UPDATE money SET Balance = ? WHERE UserID = ?"
                val = (balance, str(message.author.id))
                cursor.execute(sql, val)
            db.commit()

    @commands.command(aliases=["bal", "balance"])
    async def credits(self, ctx, user: discord.User = None):
        if user is not None:
            db = sqlite3.connect('database.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT UserID, Balance FROM money WHERE UserID = {ctx.author.id}")
            result = cursor.fetchone()
            embed = discord.Embed(title=f"{ctx.author.display_name}'s Galactic Credits: ",
                                description=f"You currently have {int(result[1]):,} Galactic Credits.", color=0xc0d4ff)
            icon = "https://i.imgur.com/IfvzrTH.png"
            embed.set_thumbnail(url=icon)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            cursor.close()
            db.close()

        elif user is None:
            db = sqlite3.connect('database.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT UserID, Balance FROM money WHERE UserID = {ctx.author.id}")
            result = cursor.fetchone()
            if result is None:
                return
            else:
                embed = discord.Embed(title=f"{ctx.author.display_name}'s Galactic Credits: ",
                                      description=f"You currently have {int(result[1]):,} Galactic Credits.",
                                      color=0xc0d4ff)
                icon = "https://i.imgur.com/IfvzrTH.png"
                embed.set_thumbnail(url=icon)
                await ctx.send(embed=embed)
            cursor.close()
            db.close()

    @credits.error
    async def credits_error(self, error):
        print(error)

    @commands.command(aliases=["galacticpoints"])
    async def points(self, ctx, user: discord.User = None):
        if user is not None:
            db = sqlite3.connect('database.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT UserID, Points FROM money WHERE UserID = {ctx.author.id}")
            result = cursor.fetchone()
            embed = discord.Embed(title=f"{ctx.author.display_name}'s Imperial Points: ",
                                  description=f"You currently have {int(result[1]):,} Imperial Points.", color=0xc0d4ff)
            icon = "https://i.imgur.com/HA7W10l.png"
            embed.set_thumbnail(url=icon)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            cursor.close()
            db.close()

        elif user is None:
            db = sqlite3.connect('database.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT UserID, Points FROM money WHERE UserID = {ctx.author.id}")
            result = cursor.fetchone()
            if result is None:
                return
            else:
                embed = discord.Embed(title=f"{ctx.author.display_name}'s Imperial Points: ",
                                      description=f"You currently have {int(result[1]):,} Imperial Points.",
                                      color=0xc0d4ff)
                icon = "https://i.imgur.com/HA7W10l.png"
                embed.set_thumbnail(url=icon)
                await ctx.send(embed=embed)
            cursor.close()
            db.close()

    @points.error
    async def points_error(self, error):
        print(error)


def setup(bot):
    bot.add_cog(Balance(bot))
    print("Balance loaded")
