import random, asyncio

import discord
from discord.ext import commands
from discord.utils import get

tips = ["Tip: Did you know that you can send suggestions using m!suggest <message>?",
        "Tip: Ask May how her day is going! She'll respond to messages such as: 'Hey May, hows it going?', or 'great job may!'",]


class Utility(commands.Cog, name="Utility.py"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["commands"])
    async def help(self, ctx, command=None):
        if command is not None:
            command = command.lower()

        # Recode all this so auto detects the cmd you specify. No need to have an if for each diff cmd.

        embed = discord.Embed(title="**Commands**",
                              description="Use **m!help <command>** to get information on a command.",
                              color=0xc0d4ff)
        embed.add_field(name="Information", value="m!info, m!avatar, m!members",
                        inline=False)
        embed.add_field(name="Utility", value="m!help, m!suggest, m!ping, m!giveroleall, m!removeroleall, m!guildicon")
        embed.add_field(name="Economy", value="m!credits, m!points, m!race, m!fish", inline=False)
        embed.add_field(name="Gambling", value="Coming Soon", inline=False)
        embed.add_field(name="Interaction", value="m!hug, m!kiss", inline=False)
        embed.add_field(name="Fun", value="m!fact, m!pokemonfact, m!joke, m!quote, m!8ball, m!generate, m!encounter,"
                                          " m!say, m!reverse, m!fakebal", inline=False)
        embed.set_footer(text=f"{random.choice(tips)}")

        await ctx.send(embed=embed)

    @commands.command(aliases=["suggestion"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def suggest(self, ctx, *, message=None):
        if message is None:
            await ctx.send("Please input a message to suggest.\nUsage: **m!suggest <message>**")
            return
    
        embed = discord.Embed(title="Suggestion", description=message.title(), color=0xc0d4ff)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"ID: {ctx.author.id}")

        channel = self.bot.get_channel(670470975929712640)
        msg = await channel.send(embed=embed)
        await msg.add_reaction(":greencheck:702359954740478053")
        await msg.add_reaction(":redx:702359966870405160")
        msg = await ctx.send("Thank you, your suggestion has been received!")
        await discord.Message.delete(msg, delay=3)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        ping = round(self.bot.latency * 1000)
        await ctx.send(f"Ping: **{ping}**ms")

    @commands.command(aliases=["gi"])
    async def guildicon(self, ctx):
        embed = discord.Embed(title="Server Icon", url=str(ctx.author.guild.icon_url), color=0xc0d4ff)
        embed.set_image(url=ctx.author.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=["gra"])
    @commands.has_permissions(administrator=True)
    async def giveroleall(self, ctx, *, rolename):
        role = discord.utils.get(ctx.guild.roles, name=rolename)
        if not role in ctx.guild.roles:
            await ctx.send("This role does not exist!")
            return

        if role > ctx.author.top_role:
            await ctx.send("Access denied. This role is higher than your top role!")
            return

        userswithrole = 0
        userswithoutrole = 0

        try:
            for member in ctx.guild.members:
                if not member.bot:
                    if role in member.roles:
                        userswithrole += 1
                    if not role in member.roles:
                        userswithoutrole += 1
        except Exception as e:
            print(e)

        embed = discord.Embed(title=f"Role name: {rolename}", color=0xc0d4ff)
        embed.add_field(name=f"Users with role", value=f"**{userswithrole}**", inline=True)
        embed.add_field(name=f"Users without role", value=f"**{userswithoutrole}**", inline=True)

        msg = await ctx.send(embed=embed)

        if get(ctx.guild.roles, name=rolename):
            for member in ctx.guild.members:
                if role in member.roles or member.bot:
                        continue
                else:
                    await member.add_roles(role)
                    embed.remove_field(1)
                    embed.remove_field(0)
                    userswithrole += 1
                    userswithoutrole -= 1
                    embed.add_field(name=f"Users with role", value=f"**{userswithrole}**", inline=True)
                    embed.add_field(name=f"Users without role", value=f"**{userswithoutrole}**", inline=True)
                    await discord.Message.edit(msg, embed=embed)

        embed.set_footer(text=f"Finished adding {rolename} role to members")
        await msg.edit(embed=embed)

    @commands.command(aliases=["rra"])
    @commands.has_permissions(administrator=True)
    async def removeroleall(self, ctx, *, rolename):
        role = discord.utils.get(ctx.guild.roles, name=rolename)
        if not role in ctx.guild.roles:
            await ctx.send("This role does not exist!")
            return

        if role > ctx.author.top_role:
            await ctx.send("Access denied. You cannot grant a role higher than your top role.")
            return

        userswithrole = 0
        userswithoutrole = 0

        try:
            for member in ctx.guild.members:
                if not member.bot:
                    if role in member.roles:
                        userswithrole += 1
                    if not role in member.roles:
                        userswithoutrole += 1
        except Exception as e:
            print(e)

        embed = discord.Embed(title=f"Role name: {rolename}", color=0xc0d4ff)
        embed.add_field(name=f"Users with role", value=f"**{userswithrole}**", inline=True)
        embed.add_field(name=f"Users without role", value=f"**{userswithoutrole}**", inline=True)

        msg = await ctx.send(embed=embed)

        if get(ctx.guild.roles, name=rolename):
            for member in ctx.guild.members:
                if role in member.roles:
                        await member.remove_roles(role)
                        embed.remove_field(1)
                        embed.remove_field(0)
                        userswithrole -= 1
                        userswithoutrole += 1
                        embed.add_field(name=f"Users with role", value=f"**{userswithrole}**", inline=True)
                        embed.add_field(name=f"Users without role", value=f"**{userswithoutrole}**", inline=True)
                        await discord.Message.edit(msg, embed=embed)
                else:
                    continue

        embed.set_footer(text=f"Finished removing {rolename} role from members")
        await msg.edit(embed=embed)

    @commands.command(aliases=["shop"])
    async def servershop(self, ctx, *, description):
        channel = self.bot.get_channel(703638893211418665)
        embed = discord.Embed(title="Server Shop", description=description, color=0xc0d4ff)
        embed.set_author(name=ctx.author.guild.name, icon_url=ctx.author.guild.icon_url)
        embed.set_footer(text="Prices are subject to change, and refunds are not permitted\nDM Kirie#0001 for futher information/payment")

        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))
    print("Utility Loaded")
