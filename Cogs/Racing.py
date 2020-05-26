import random
import sqlite3

import discord
from discord.ext import commands


class Racing(commands.Cog, name="Racing.py"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["r"])
    @commands.cooldown(1, 90, commands.BucketType.user)
    async def race(self, ctx):
        suffix = ""
        place = ""
        completedlaps = random.randint(2, 4)

        places = [place for place in range(1, 26, 1)]

        for placing in places:
            while placing < 25:
                place = random.choice(places)
                places.remove(place)
                placing += 1

            if place % 10 == 1:
                suffix = "st"
            elif place % 10 == 2:
                suffix = "nd"
            elif place % 10 == 3:
                suffix = "rd"
            else:
                suffix = "th"
            if place == 11 or place == 12 or place == 13:
                suffix = "th"

        coinsgained = round((place / 2) + completedlaps * 2)
        coinsgained = round(coinsgained / place * 50)

        pointsgained = 30

        places = ["Gotham City", "Sunnydale", "Metropolis", "Central City", "Star City", "Springfield", "Hill Valley",
                  "Duckburg", "Celadon City", "Kamina City", "Shiganshina", "Sidonia", "Ecbatana", "Alubarna",
                  "Tokyo", "New York City", "Akihabara", "R'lyeh", "Radiator Springs", "Azalea Town", "Cinnabar Island", 
                  "Dewford Town", "Fortree City", "Larvaridge Town", "Mauville City", "Mossdeep City", "Lilycove City",
                  "Littleroot Town", "Oldale Town", "Petalburg City", "Rustboro City", "Slateport City", "Sootopolis City",
                  "Verdanturf Town", "Attilan", "Atlantis", "Asgard"]

        startdesc = f"You travel through {random.choice(places)} in a race."
        description = f"{startdesc}\nYou finish in **{int(place)}{suffix}** place out of 25 racers!"

        embed = discord.Embed(title="Racing", description=description, color=0xc0d4ff)
        embed.add_field(name="Placement", value=str(place), inline=True)
        embed.add_field(name="Laps Completed", value=completedlaps, inline=False)
        embed.add_field(name="Credits Gained", value=str(coinsgained), inline=True)
        embed.add_field(name="Points Earned", value=str(pointsgained), inline=True)
        embed.set_thumbnail(url="https://i.imgur.com/189DHqc.png")

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
    bot.add_cog(Racing(bot))
    print("Racing Loaded")
