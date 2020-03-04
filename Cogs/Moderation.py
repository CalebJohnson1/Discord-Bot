import discord
from discord.ext import commands


class ModCog(commands.Cog, name='Moderation'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["modcommands", "staffcommands"])
    @commands.has_permissions(ban_members=True)
    async def moderation(self, ctx):
        embed = discord.Embed(title="Moderation Commands", description="Commands for Moderators.", color=0xc0d4ff)
        embed.add_field(name="m!clear <amount>",
                        value="Purges a specified amount of messages (5 if no specification).", inline=False)
        embed.add_field(name="m!kick <member name or mention>", value="Kicks the member from the server.",
                        inline=False)
        embed.add_field(name="m!mute <member name or mention>", value="Mutes the member from the server.",
                        inline=False)
        embed.add_field(name="m!unmute <member name or mention>", value="Unmuted the member from the server.", inline=False)
        embed.add_field(name="m!ban <member name or mention>", value="Bans the member from the server.",
                        inline=False)
        embed.add_field(name="m!unban <member>", value="Unbans the member from the server.", inline=False)

        await ctx.author.send(embed=embed)
        await ctx.send("Sent you a DM containing Moderation commands!")

    '''@commands.command(aliases=["announce"])
    @commands.cooldown(1, 300, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def announcement(self, ctx, *, message):
        guild = self.bot.get_guild(id=467019883712872459)
        embed = discord.Embed(title=f"{ctx.author.display_name.title()}'s Announcement", description=message,
                              color=0xc0d4ff)
        embed.set_author(name=f"{guild.name} Announcement",
                         icon_url=guild.icon_url)

        for member in guild.members:
            if not member.bot:
                await discord.DMChannel.send(member, embed=embed)
        await ctx.channel.purge(limit=1)

    @announcement.error
    async def announcement_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Please wait another {round(error.retry_after, 2)} seconds to send an announcement.")'''

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx, *, member: discord.Member, reason=None):
        if member.id == 634650815017254913:
            await ctx.send("I can't kick myself!")
            return
        if member.id == 154342861851197440:
            return

        else:
            await member.kick(reason=reason)
            await ctx.send(f"Kicked {member.display_name}")
            return

    @kick.error
    async def kick_error(self, error):
        print(error)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, *, member: discord.Member):
        muted = discord.utils.get(ctx.guild.roles, name="Muted")
        if member.id == 634650815017254913:
            await ctx.send("I can't mute myself!")
            return
        if member.id == 154342861851197440:
            return

        await member.add_roles(muted)
        await ctx.send(f"Muted {member.display_name}")

    @mute.error
    async def mute_error(self, error):
        print(error)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx, *, member: discord.Member):
        muted = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(muted)
        await ctx.send(f"Unmuted {member.display_name}")

    @unmute.error
    async def unmute_error(self, error):
        print(error)

    @commands.command(aliases=["banhammer"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, *, member: discord.Member, reason=None):
        if member.id == 634650815017254913:
            await ctx.send("I can't ban myself!")
            return
        if member.id == 154342861851197440:
            return

        await member.ban(reason=reason)
        await ctx.send(f"{member.display_name} has been struck by the Banhammer!")
        return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member: discord.Member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send()
                return

    @unban.error
    async def unban_error(self, error):
        print(error)

    @commands.command(aliases=["clean", "purge"])
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        return

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Please wait another {round(error.retry_after, 2)} seconds to purge the chat.")


def setup(bot):
    bot.add_cog(ModCog(bot))
    print('Moderation loaded.')
