from discord.ext import commands
import discord


class Information(commands.Cog, name="Information.py"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        if member.top_role == member.guild.default_role:
            embed = discord.Embed(color=0xc0d4ff)
        else:
            embed = discord.Embed(color=member.color)

        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.name + "#" + member.discriminator, icon_url=member.avatar_url)
        embed.add_field(name="Account Creation Date", value=member.created_at.strftime('%d-%B %Y @ %I:%M %p'),
                        inline=False)
        embed.add_field(name="Server Join Date", value=member.joined_at.strftime('%d-%B %Y @ %I:%M %p'), inline=False)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Status", value=member.status, inline=True)
        embed.add_field(name="Nickname", value=member.nick, inline=False)
        if not member.top_role == member.guild.default_role:
            embed.add_field(name=f"Top Role", value=member.top_role, inline=False)
        if member.bot:
            embed.set_footer(text="This user is a bot.")

        await ctx.send(embed=embed)

    @info.error
    async def infoerror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Please wait another {round(error.retry_after, 2)} seconds to info a user.")
        else:
            await ctx.send("Please specify a member name, ex: <m!info May>")
            print(error)

    @commands.command(aliases=["ava", "av"])
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        if member.top_role == member.guild.default_role:
            embed = discord.Embed(title=f"{member.display_name}'s Avatar", color=0xc0d4ff)
        else:
            embed = discord.Embed(title=f"{member.display_name}'s Avatar", color=member.color)
        embed.set_image(url=member.avatar_url_as(size=256))
        embed.set_author(name=member.display_name + "#" + member.discriminator, icon_url=member.avatar_url)
        if member.bot:
            embed.set_footer(text="This user is a bot.")
        await ctx.send(embed=embed)

    @avatar.error
    async def avatar_error(self, ctx, error):
        await ctx.send("Please specify a member, usage: <m!avatar <username>")
        print(error)

    @commands.command()
    async def members(self, ctx):
        bots = 0
        for member in ctx.author.guild.members:
            if member.bot:
                bots += 1

        embed = discord.Embed(title=f"{ctx.author.guild}", description=None, color=0xc0d4ff)
        embed.add_field(name="All Members", value=ctx.author.guild.member_count, inline=True)
        embed.add_field(name="Users", value=ctx.author.guild.member_count - bots, inline=True)
        embed.add_field(name="Bots", value=str(bots), inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
    print("Information Loaded")
