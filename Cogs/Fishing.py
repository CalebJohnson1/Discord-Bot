import random
import sqlite3

import discord
from discord.ext import commands


class Fishing(commands.Cog, name="Fishing.py"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["fishing", "f"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def fish(self, ctx):
        fishpic = ["https://i.imgur.com/p1JN0im.png", "https://i.imgur.com/irgi2dt.png", "https://i.imgur.com/5YtcB9V.png",
                   "https://i.imgur.com/mj10V9f.png", "https://i.imgur.com/We5pQUB.png", "https://i.imgur.com/4FLLTnL.png"]

        fish = ""
        coinsgained = 0
        pointsgained = 10
        url = random.choice(fishpic)

        if random.randint(1, 100) == 1:
            url = "https://i.imgur.com/aGUUadV.png"
            coinsgained = 100
            fish = "Sando Aqua Monster"

        if random.randint(1, 1000) == 1:
            url = "https://vignette.wikia.nocookie.net/starwars/images/3/3d/Opee-Sea-Killer-SWCT.png/revision/latest?cb=20170623053643"
            coinsgained = 500
            fish = "Opee Sea Killer"

        places = ["on Naboo", "at Otoh Gunga", "at Lake Paonga", "at The Abyss"]

        if url == fishpic[0]:
            fish = "Doo Scalefish"
            coinsgained = 15
        if url == fishpic[1]:
            fish = "Faa Scalefish"
            coinsgained = 10
        if url == fishpic[2]:
            fish = "Laa Scalefish"
            coinsgained = 10
        if url == fishpic[3]:
            fish = "See Scalefish"
            coinsgained = 5
        if url == fishpic[4]:
            fish = "Tee Scalefish"
            coinsgained = 25
        if url == fishpic[5]:
            fish = "Colo Claw Fish"
            coinsgained = 10
            places = ["at the Cordaxian Sea"]

        description = f"You went fishing {random.choice(places)} and caught a {fish}!"
        embed = discord.Embed(title="Fishing", description=description, color=0xc0d4ff)
        embed.add_field(name="Galactic Credits Gained", value=str(coinsgained), inline=True)
        embed.add_field(name="Galactic Points Gained", value=str(pointsgained), inline=True)
        embed.set_thumbnail(url=url)

        db = sqlite3.connect('database.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT UserID, Balance, Points FROM money WHERE UserID = {ctx.author.id}")
        result = cursor.fetchone()

        if result is None:
            sql = "INSERT INTO money(UserID, Balance, Points) VALUES(?, ?, ?)"
            val = (ctx.author.id, coinsgained, pointsgained)
            cursor.execute(sql, val)
            db.commit()
            await ctx.send(embed=embed)

        if ctx.author.id is not None:
            balance = int(result[1])
            points = int(result[2])
            sql = "UPDATE money SET Balance = ? WHERE UserID = ?"
            sql2 = "UPDATE money SET Points = ? WHERE UserID = ?"
            val = (balance + coinsgained, str(ctx.author.id))
            val2 = (points + pointsgained, str(ctx.author.id))
            cursor.execute(sql, val)
            cursor.execute(sql2, val2)

        db.commit()

        await ctx.send(embed=embed)

    @fish.error
    async def fish_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            errormsg = await ctx.send(f"Please wait **{round(error.retry_after, 2)}** seconds to fish again.")
            await discord.Message.delete(errormsg, delay=3)

        print(error)


def setup(bot):
    bot.add_cog(Fishing(bot))
    print("Fishing Loaded")
