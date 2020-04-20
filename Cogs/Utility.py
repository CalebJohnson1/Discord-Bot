import discord
from discord.ext import commands
import random

tips = ["Tip: Did you know that you can send suggestions using m!suggest <message>?",
        "Tip: Ask May how her day is going! She'll respond to messages such as: 'Hey May, hows it going?', or 'great job may!'",
        "Tip: You can also use may!<command> as a prefix instead of m!"]


class Utility(commands.Cog, name="Utility.py"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["commands"])
    async def help(self, ctx, command=None):
        if command is not None:
            command = command.lower()

        help_icon = "https://cdn.discordapp.com/emojis/678432297896116226.png?v=1"

        # Recode all this so auto detects the cmd you specify. No need to have an if for each diff cmd.

        if command == "info":
            embed = discord.Embed(title="Info Help", description="Gives information on a user.\n"
                                                                 "Usage: **m!info (user)**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "avatar":
            embed = discord.Embed(title="Avatar Help", description="Returns an embed with the users profile picture.\n"
                                                                   "Usage: **m!avatar (user)**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return
    
        if command == "members":
            embed = discord.Embed(title="Members Help", description="Displays how many members are in the server.\n"
                                                                    "Usage: **m!members**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "ping":
            embed = discord.Embed(title="Ping Help", description="Displays the latency of the bot.\n"
                                                                 "Usage: **m!ping**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "suggest" or command == "suggestion":
            embed = discord.Embed(title="Suggestion Help",
                                  description="Inputs a suggestion into the suggestions tab of May's main server\n"
                                              "Usage: **m!suggest (suggestion)**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "kick" or command == "mute" or command == "unmute" or command == "ban" or \
                command == "unban" or command == "clear" or command == "moderation":
            await ctx.send("please use **m!moderation** to view moderation commands.")
            return

        if command == "credits" or command == "balance" or command == "bal":
            embed = discord.Embed(title="Credits Help", description="Displays your Galactic Credits.\n"
                                                                    "Usage: **m!credits**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "points" or command == "galactic points":
            embed = discord.Embed(title="Points Help", description="Displays your Galactic Points.\n"
                                                                   "Usage: **m!points**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "raid" or command == "raids":
            embed = discord.Embed(title="Raid Help", description="Completes a raid and awards credits.\n"
                                                                 "Usage: **m!raid**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "55x2":
            embed = discord.Embed(title="55x2 Help", description="Rolls a dice. If the dice rolls over 55, you win.\n"
                                                                 "Usage: **m!55x2**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "hug":
            embed = discord.Embed(title="Hugging Help", description="Give someone a hug!.\n"
                                                                    "Usage: **m!hug <mention>**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "kiss" or command == "kissing":
            embed = discord.Embed(title="Kissing Help", description="Give someone a kiss!.\n"
                                                                    "Usage: **m!kiss <mention>**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "fact":
            embed = discord.Embed(title="Fact Help", description="Sends a random fact.\n"
                                                                 "Usage: **m!fact**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "quote":
            embed = discord.Embed(title="Quote Help", description="Sends a random quote from a tv show or movie.\n"
                                                                  "Usage: **m!quote**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "joke":
            embed = discord.Embed(title="Joke Help", description="Sends a random joke.\n"
                                                                 "Usage: **m!joke**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "8ball":
            embed = discord.Embed(title="8ball Help", description="Ask a question you've always wanted an answer to!\n"
                                                                  "Usage: **m!8ball (question)**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "generate":
            embed = discord.Embed(title="Generate Help", description="Generates a random username.\n"
                                                                     "Usage: **m!generate**", color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "encounter":
            embed = discord.Embed(title="Encounter Help", description="Stimulates a set number of pokemon encounters!\n"
                                                                      "Usage: **m!encounter <amount> <name>**",
                                  color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "say" or command == "speak":
            embed = discord.Embed(title="Speak Help", description="Speak as the bot!\n"
                                                                  "Usage: **m!say <message>**",
                                  color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "reverse" or command == "backwards":
            embed = discord.Embed(title="Reverse Help", description="Send a message backwards!\n"
                                                                    "Usage: **m!reverse <message>**",
                                  color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "race" or command == "podracing":
            embed = discord.Embed(title="Pod Racing", description="Stimulates a podrace!\n"
                                                                  "Usage: **m!race**\n"
                                                                  "This commands grants Galactic Credits, as well as Galactic Points.",
                                  color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "fish" or command == "fishing":
            embed = discord.Embed(title="Fishing", description="Go fishing and catch a fish! (Star Wars based)\n"
                                                               "Usage: **m!fish**\n"
                                                               "This commands grants Galactic Credits, as well as Galactic Points.",
                                  color=0xc0d4ff)
            embed.set_author(name="Help", icon_url=help_icon)
            await ctx.send(embed=embed)
            return

        if command == "guildicon" or command == "gi":
            embed = discord.Embed(title="", description="Sends an embed of the current guild icon.\n"
                                                        "Usage: **m!gi** or **m!guildicon**")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="**Commands**",
                              description="Use **m!help <command>** to get information on a command.",
                              color=0xc0d4ff)
        embed.add_field(name="Information", value="m!info, m!avatar, m!members",
                        inline=False)
        embed.add_field(name="Utility", value="m!help, m!suggest, m!ping, m!guildicon")
        embed.add_field(name="Economy", value="m!credits, m!points", inline=False)
        embed.add_field(name="Star Wars", value="m!race, m!fish", inline=False)
        embed.add_field(name="Gambling", value="Coming Soon", inline=False)
        embed.add_field(name="Interaction", value="m!hug, m!kiss", inline=False)
        embed.add_field(name="Fun", value="m!fact, m!pokemonfact, m!joke, m!quote, m!8ball, m!generate, m!encounter,"
                                          " m!say, m!reverse",
                        inline=False)
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
        await channel.send(embed=embed)
        await ctx.send("Thank you, your suggestion has been received!")

    @suggest.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            errormsg = await ctx.send(f"Please wait another {round(error.retry_after, 2)} seconds to make a suggestion.")
            await discord.Message.delete(errormsg, delay=5)
        print(error)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        ping = round(self.bot.latency * 1000)
        await ctx.send(f"Ping: **{ping}**ms")

    @commands.command(aliases=["gi"])
    async def guildicon(self, ctx):
        embed = discord.Embed(title="Server Icon", description=None, url=str(ctx.author.guild.icon_url), color=0xc0d4ff)
        embed.set_image(url=ctx.author.guild.icon_url)

        await ctx.send(embed=embed)

    @guildicon.error
    async def guildicon_error(self, ctx, error):
        errormsg = await ctx.send(error)
        await discord.Message.delete(errormsg, delay=5)


def setup(bot):
    bot.add_cog(Utility(bot))
    print("Utility Loaded")
