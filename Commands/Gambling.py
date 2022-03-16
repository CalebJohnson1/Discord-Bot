import asyncio
import random
import sqlite3

import discord
from discord.ext import commands

gambleColor = 0xFFFFF0

class Gambling(commands.Cog, name="Gambling.py"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='55x2', aliases=["55"],
    usage='55x2 <amount>',
    description='Roll a 100-sided dice! If the dice rolls over 55, you win.')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def __55__(self, ctx, amount):
        def check(m):
            msgchannel = ctx.message.channel
            return m.author == ctx.author and m.channel == msgchannel

        if int(amount) < 1:
            await ctx.message.reply("Please input an amount above 0.", mention_author = False)
            return

        dice = random.randint(0, 100)
        
        if dice > 55:
            description = f"You rolled a {dice} and won {int(amount):,} credits!"
        elif dice == 55:
            description = f"You rolled a {dice}! Would you like to reroll?"
        else:
            description = f"You rolled a {dice} and lost {int(amount):,} credits..."

        embed = discord.Embed(title=f"You role the dice...", description=str(description), color=gambleColor)
        embed.set_author(name="Dicing", icon_url=
        "https://i.ya-webdesign.com/images/dice-logo-png-7.png")

        db = sqlite3.connect('database.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT UserID, Balance FROM player WHERE UserID = {ctx.author.id}")
        result1 = cursor.fetchone()
        balance = int(result1[1])

        if int(balance) < int(amount):
            await ctx.message.reply("You don't have this many credits!", mention_author = False)
            return

        sql = "UPDATE player SET Balance = ? WHERE UserID = ?"
        if dice > 55:
            val = (int(balance) + int(amount), str(ctx.author.id))
        elif dice == 55:
            val = (int(balance), str(ctx.author.id))
            invalidRoll = await ctx.bot.wait_for('message', check=check, timeout=120)
            if invalidRoll.content.lower() == 'y' or 'yes' in invalidRoll.content.lower():
                # Finish this some time, not important rn
                # Just put the dice roll into a seperate function and call it here, will make it much easier
                # will need to rewrite how some of it works.
                return
            else:
                return
        else:
            val = (int(balance) - int(amount), str(ctx.author.id))
        cursor.execute(sql, val)
        db.commit()

        await ctx.message.reply(embed=embed, mention_author = False)

    @commands.command(name='dice', usage='dice <amount>',
    description='The user and bot both roll a 100-sided dice. If the user rolls higher than the bot, the user wins.')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def dice(self, ctx, amount):
        if int(amount) < 1:
            await ctx.message.reply("Please input an amount above 0.", mention_author = False)
            return

        userroll = random.randint(1, 100)
        botroll = random.randint(1, 100)

        db = sqlite3.connect('database.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT UserID, Balance FROM player WHERE UserID = {ctx.author.id}")
        result1 = cursor.fetchone()
        balance = int(result1[1])

        if int(balance) < int(amount):
            await ctx.message.reply("You don't have this many credits!")
            return

        try:
            embed = discord.Embed(title="Rolling Dice...", description=f"{ctx.author.display_name} Rolls: \n"
                                                                        "Gaia Rolls: ", color=gambleColor)
            
            newembed = discord.Embed(title="Rolling Dice...", description=f"{ctx.author.display_name} Rolls: **{userroll}** \n"
                                                                        f"Gaia Rolls: ", color=gambleColor)
            
            finalembed = discord.Embed(title="Rolling Dice...", description=f"{ctx.author.display_name} Rolls: **{userroll}** \n"
                                                       f"Gaia Rolls: **{botroll}**", color=gambleColor)
        except Exception as e:
            print(e)
            return
            
        msg = await ctx.message.reply(embed=embed, mention_author = False)
        await asyncio.sleep(1)
        await discord.Message.edit(msg, embed=newembed)
        await asyncio.sleep(1)
        await discord.Message.edit(msg, embed=finalembed)
        await asyncio.sleep(1)

        sql = "UPDATE player SET Balance = ? WHERE UserID = ?"

        try:
            if userroll > botroll:
                val = (int(balance) + int(amount), str(ctx.author.id))
                finalembed = discord.Embed(title=f"{ctx.author.display_name} wins {amount} credits!", description=f"{ctx.author.display_name} Rolls: **{userroll}** \n"
                                                                        f"Gaia Rolls: **{botroll}**\n", color=gambleColor)
                await discord.Message.edit(msg, embed=finalembed)
            elif userroll < botroll:
                val = (int(balance) - int(amount), str(ctx.author.id))
                finalembed = discord.Embed(title=f"{ctx.author.display_name} loses {amount} credits...", description=f"{ctx.author.display_name} Rolls: **{userroll}** \n"
                                                                        f"Gaia Rolls: **{botroll}**\n", color=gambleColor)
                await discord.Message.edit(msg, embed=finalembed)
            else:
                val = (int(balance), str(ctx.author.id))
                finalembed = discord.Embed(title=f"Tie!", description=f"{ctx.author.display_name} Rolls: **{userroll}** \n"
                                                                        f"Gaia Rolls: **{botroll}**\n", color=gambleColor)
                await discord.Message.edit(msg, embed=finalembed)
            
            cursor.execute(sql, val)
            db.commit()

        except Exception as e:
            print(e)
            return

def setup(bot):
    bot.add_cog(Gambling(bot))
