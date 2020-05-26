import asyncio
import random
import sqlite3

import discord
from discord.ext import commands


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
        errormsg = await ctx.send("Please specify an amount to gamble! <m!55x2 (amount)>")
        await discord.Message.delete(errormsg, delay=5)
        print(error)

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def dice(self, ctx):
        userroll = random.randint(1, 100)
        botroll = random.randint(1, 100)

        try:
            embed = discord.Embed(title="Rolling Dice...", description=f"{ctx.author.display_name} Rolls: \n"
                                                                        "May Rolls: ", color=0xc0d4ff)
            
            newembed = discord.Embed(title="Rolling Dice...", description=f"{ctx.author.display_name} Rolls: **{userroll}** \n"
                                                                        f"May Rolls: ", color=0xc0d4ff)
            
            finalembed = discord.Embed(title="Rolling Dice...", description=f"{ctx.author.display_name} Rolls: **{userroll}** \n"
                                                       f"May Rolls: **{botroll}**", color=0xc0d4ff)
        except Exception as e:
            print(e)
            return
            
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(1)
        await discord.Message.edit(msg, embed=newembed)
        await asyncio.sleep(1)
        await discord.Message.edit(msg, embed=finalembed)
        await asyncio.sleep(1)

        try:
            if userroll > botroll:
                finalembed = discord.Embed(title=f"{ctx.author.display_name} wins!", description=f"{ctx.author.display_name} Rolls: **{userroll}** \n"
                                                                        f"May Rolls: **{botroll}**\n", color=0xc0d4ff)
                await discord.Message.edit(msg, embed=finalembed)
            elif userroll < botroll:
                finalembed = discord.Embed(title=f"{ctx.author.display_name} loses...", description=f"{ctx.author.display_name} Rolls: **{userroll}** \n"
                                                                        f"May Rolls: **{botroll}**\n", color=0xc0d4ff)
                await discord.Message.edit(msg, embed=finalembed)
            else:
                finalembed = discord.Embed(title=f"Tie!", description=f"{ctx.author.display_name} Rolls: **{userroll}** \n"
                                                                        f"May Rolls: **{botroll}**\n", color=0xc0d4ff)
                await discord.Message.edit(msg, embed=finalembed)

        except Exception as e:
            print(e)
            return

def setup(bot):
    bot.add_cog(Gambling(bot))
    print("Gambling loaded")
