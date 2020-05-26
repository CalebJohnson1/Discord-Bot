import random
import sqlite3

import discord
from discord.ext import commands


class Fishing(commands.Cog, name="Fishing.py"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["fishing", "f"])
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def fish(self, ctx):
        fish = "Magikarp"
        coinsgained = 50
        pointsgained = 10
        url = "https://i.imgur.com/Dkj3fJw.png"

        if random.randint(1, 100) == 1:
            url = "https://i.imgur.com/Ygof8MD.png"
            coinsgained = 100
            fish = "Lapras"

        if random.randint(1, 1000) == 1:
            url = "https://i.imgur.com/Cb4MZrG.png"
            coinsgained = 500
            fish = "Kyogre"

        if random.randint(1, 4096) == 1:
            url = "https://i.imgur.com/0uquYEz.png"
            coinsgained = 1000
            fish = "Shiny Magikarp"

        places = ["Gotham City", "Sunnydale", "Metropolis", "Central City", "Star City", "Springfield", "Hill Valley",
                  "Duckburg", "Celadon City", "Kamina City", "Shiganshina", "Sidonia", "Ecbatana", "Alubarna",
                  "Tokyo", "New York City", "Akihabara", "R'lyeh", "Radiator Springs", "Azalea Town", "Cinnabar Island", 
                  "Dewford Town", "Fortree City", "Larvaridge Town", "Mauville City", "Mossdeep City", "Lilycove City",
                  "Littleroot Town", "Oldale Town", "Petalburg City", "Rustboro City", "Slateport City", "Sootopolis City",
                  "Verdanturf Town", "Attilan", "Atlantis", "Asgard"]

        description = f"You go fishing at {random.choice(places)} and catch a {fish}!"
        embed = discord.Embed(title="Fishing", description=description, color=0xc0d4ff)
        embed.add_field(name="Credits Gained", value=str(coinsgained), inline=True)
        embed.add_field(name="Points Gained", value=str(pointsgained), inline=True)
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


def setup(bot):
    bot.add_cog(Fishing(bot))
    print("Fishing Loaded")
