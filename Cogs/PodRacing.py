import discord
from discord.ext import commands
import sqlite3
import random


class PodRacing(commands.Cog, name="PodRacing.py"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["podracing", "podrace", "r", "pr"])
    @commands.cooldown(1, 90, commands.BucketType.user)
    async def race(self, ctx):
        racerone = "https://free3d.com/imgd/l35591-anakin-skywalkers-podracer-84172.png"
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

        planets = ["Tatooine", "Coruscant", "Hoth", "Naboo", "Alderaan", "Bespin", "Mustafar", "Yavin",
                   "Dagobah", "Kashyyyk", "Kamino", "Geonosis", "Corellia", "Dantooine", "Ryloth", "Moraband",
                   "Cato Neimoidia", "Byss", "Onderon", "Nal Hutta", "Polis Massa", "Malachor V", "Florrum", "Ithor",
                   "Ossus", "Taris", "Mandalore", "Haruun Kal", "Exodeen", "Malastare", "Kergans", "Theron",
                   "Cantonica"]

        startdesc = f"You travel through {random.choice(planets)} in a pod race."
        description = f"{startdesc}\nYou finish in **{int(place)}{suffix}** place out of 25 racers!"

        embed = discord.Embed(title="Pod Racing", description=description, color=0xc0d4ff)
        embed.add_field(name="Placement", value=str(place), inline=True)
        embed.add_field(name="Laps Completed", value=completedlaps, inline=False)
        embed.add_field(name="Galactic Credits Gained", value=str(coinsgained), inline=True)
        embed.add_field(name="Galactic Points Earned", value=str(pointsgained), inline=True)

        embed.set_thumbnail(url=racerone)

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

    @race.error
    async def race_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            errormsg = await ctx.send(f"Please wait **{round(error.retry_after, 2)}** seconds to complete another race.")
            await discord.Message.delete(errormsg, delay=5)

        print(error)


def setup(bot):
    bot.add_cog(PodRacing(bot))
    print("PodRacing Loaded")
