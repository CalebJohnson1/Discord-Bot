import discord
from discord.ext import commands
import random
import sqlite3


class Gambling(commands.Cog, name="Gambling.py"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["55x2"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def gamble(self, ctx, amount):
        if int(amount) < 1:
            await ctx.send("Please input an amount above 0.")
            return

        dice = random.randint(0, 100)
        if dice >= 55:
            description = f"You rolled a {dice} and won {int(amount):,} credits!"
        else:
            description = f"You rolled a {dice} and lost {amount:,} credits..."
        embed = discord.Embed(title=f"You role the dice...", description=str(description), color=0xFFFFF0)
        embed.set_author(name="Dicing", icon_url=
        "https://i.ya-webdesign.com/images/dice-logo-png-7.png")

        db = sqlite3.connect('database.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT UserID, Balance FROM money WHERE UserID = {ctx.author.id}")
        result1 = cursor.fetchone()
        balance = int(result1[1])
        if int(balance) < int(amount):
            await ctx.send("You don't have this many credits!")
            return

        sql = "UPDATE money SET Balance = ? WHERE UserID = ?"
        if dice >= 55:
            val = (int(balance) + int(amount) * 2, str(ctx.author.id))
        else:
            val = int(balance) - int(amount), str(ctx.author.id)
        cursor.execute(sql, val)
        db.commit()

        await ctx.send(embed=embed)

    @gamble.error
    async def gamble_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            errormsg = await ctx.send(f"Please wait another {round(error.retry_after, 2)} seconds to roll the dice.")
            await discord.Message.delete(errormsg, delay=5)
            return

        errormsg = await ctx.send("Please specify an amount to gamble! <m!55x2 (amount)>")
        await discord.Message.delete(errormsg, delay=5)
        print(error)


def setup(bot):
    bot.add_cog(Gambling(bot))
    print("Gambling loaded")
