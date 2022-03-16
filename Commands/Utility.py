import asyncio
from calendar import timegm
import random
import re
import os
from sqlite3 import Timestamp
import datetime

import discord
from discord.ext import commands
from discord.utils import get
from base64 import *

class Utility(commands.Cog, name="Utility.py"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', pass_context=True, aliases=["commands"], hidden=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def help(self, ctx, cmd = None):
        for command in self.bot.commands:
            if cmd == command.name:
                if command.hidden:
                    break

                embed = discord.Embed(title=command.name.title(), description=command.description, color=0xc0d4ff)
                embed.set_author(name="Command Help", icon_url=self.bot.user.avatar_url)
                if not command.aliases:
                    aliases = command.name

                if command.aliases:
                    aliases = (", ".join(command.aliases))

                if command.usage:
                    usages = f"**{command.usage}**"

                aliases = f"**{aliases}**"
                embed.add_field(name="*Usages*", value=usages, inline=True)
                embed.add_field(name="*Aliases*", value=aliases, inline=True)
                await ctx.message.reply(embed=embed, mention_author = False)
                return

        embed = discord.Embed(title="**Commands**",
                              description=f"Use **::help <command>** to get information on a command.",
                              color=0xc0d4ff)
        embed.add_field(name="*Information*", value="info, avatar, members",
                        inline=False)
        embed.add_field(name="*Utility*", value="help, suggest, giveroleall, removeroleall, servericon, ping, startevent")
        embed.add_field(name="*Economy*", value="**start**, credits, points, race, fish", inline=False)
        # embed.add_field(name="*Gambling*", value="Coming Soon", inline=False)
        embed.add_field(name="*Fun*", value="fact, joke, quote, marvelquote, 8ball, generate, encounter,"
                                          " say, reverse", inline=False)
        await ctx.message.reply(embed=embed, mention_author = False)

    @commands.command(name='suggest', aliases=["suggestion"],
    usage='suggest <message>',
    description='Allows you to input a suggestion to the bot.')
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def suggest(self, ctx, *, message=None):
        print(ctx.author.created_at)

        if message is None:
            await ctx.message.reply("Please input a message to suggest.\nUsage: **::suggest <message>**")
            return

        embed = discord.Embed(title="Suggestion", description=message.title(), color=0xc0d4ff)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"ID: {ctx.author.id}")

        channel = self.bot.get_channel(881778673215221791)
        msg = await channel.send(embed=embed)
        await msg.add_reaction(":greencheck:702359954740478053")
        await msg.add_reaction(":redx:702359966870405160")
        msg = await ctx.message.reply("Thank you, your suggestion has been received!", )
        await discord.Message.delete(msg, delay=3)

    @suggest.error
    async def suggestion_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(name='servericon', aliases=["gi", "guildicon"],
    usage='servericon',
    description='Displays the servers icon')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def servericon(self, ctx):
        embed = discord.Embed(title="Server Icon", url=str(ctx.author.guild.icon_url), color=0xc0d4ff)
        embed.set_image(url=ctx.author.guild.icon_url)

        await ctx.message.reply(embed=embed, mention_author = False)

    @commands.command(name='giveroleall', aliases=["gra"],
    usage='giveroleall <role>',
    description='Gives the specified role to all members in the server.\nCase sensitive')
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 300, commands.BucketType.guild)
    async def giveroleall(self, ctx, *, rolename):
        role = discord.utils.get(ctx.guild.roles, name=rolename)
        if not role in ctx.guild.roles:
            await ctx.message.reply("This role does not exist!", mention_author = False)
            return

        if role > ctx.author.top_role:
            await ctx.message.reply("Permission denied.", mention_author = False)
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

        msg = await ctx.message.reply(embed=embed, mention_author = False)

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

    @commands.command(name='removeroleall', aliases=["rra"],
    usage='removeroleall <role>',
    description='Removes the specified role from all members in the server.\nCase sensitive')
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 300, commands.BucketType.guild)
    async def removeroleall(self, ctx, *, rolename):
        role = discord.utils.get(ctx.guild.roles, name=rolename)
        if not role in ctx.guild.roles:
            await ctx.message.reply("This role does not exist!", mention_author = False)
            return

        if role > ctx.author.top_role:
            await ctx.message.reply("Permission denied. You cannot grant a role higher than your top role.", mention_author = False)
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

        msg = await ctx.message.reply(embed=embed, mention_author = False)

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

    @commands.command(name='book', aliases=["randbook", "randombook"],
    usage='book',
    description='Picks a random book for you to read!')
    async def book(self, ctx):
        verbs = ['I wish for', 'I choose', "I've picked", "I've selected"]
        randVerb = random.choice(verbs)
        books = {
            'Children of Blood and Bone': 'Tomi Adeyemi',
            'Legendborn': 'Tracy Deonn',
            '1984': 'George Orwell',
            'The Hate U Give': 'Angie Thomas',
            'Pride and Prejudice': 'Jane Austen',
            'Brave New World': 'Aldous Huxley',
            'Renegades': 'Marissa Meyer',
            'Hitchhikers Guide to the Galaxy': 'Douglas Adams',
            'Animal Farm': 'George Orwell',
            'Les Miserables': 'Victor Hugo',
            'The Da Vinci Code': 'Dan Brown',
            'Memoirs Of A Geisha': 'Arthur Golden',
            'Where The Crawdads Sing': 'Delia Owens',
            'Hunger Games': 'Suzanne Collins',
            'Percy Jackson': 'Rick Riordan'
        }
        randomBook = random.choice(list(books))
        author = books[randomBook]
        await ctx.message.reply(f"{randVerb} {randomBook} by {author} to be the next for book you to read.", mention_author = False)

    '''@commands.command(name='ping', aliases=['pingwebsite'],
    usage='ping <website>',
    description='Check to view the status of a website.')
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ping(self, ctx, website):
        response = os.system("ping -c 1 " + website)

        if response == 0:
            statusValue = 'Online'
            statusColor = 0x00ff08
        else:
            statusValue = 'Offline'
            statusColor = 0xff0015

        embed = discord.Embed(title=website.title(), color=statusColor)
        embed.add_field(name="Status", value=statusValue)
        await ctx.message.reply(embed=embed, mention_author = False)'''

def setup(bot):
    bot.add_cog(Utility(bot))
