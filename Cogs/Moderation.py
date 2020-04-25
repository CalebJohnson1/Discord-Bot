import asyncio

import discord
from discord.ext import commands
from discord.utils import get


class ModCog(commands.Cog, name='Moderation'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["modcommands", "staffcommands"])
    @commands.has_permissions(manage_messages=True)
    async def moderation(self, ctx):
        embed = discord.Embed(title="Moderation Commands", description="Commands for Moderators.", color=0xc0d4ff)
        embed.add_field(name="m!clear <amount>",
                        value="Purges a specified amount of messages (5 if no specification).", inline=False)
        embed.add_field(name="m!ban <member id or mention>", value="Bans the specified member from the guild.",
                        inline=False)
        embed.add_field(name="m!softban <member id or mention>", value="Bans then immediately unbans the specified user from the guild.")
        embed.add_field(name="m!unban <member>", value="Unbans a member from the server.", inline=False)
        embed.add_field(name="m!giveroleall <rolename>", value="Gives all members in the guild a specified role.")
        embed.add_field(name="m!kick <member id or mention>", value="Kicks a member from the guild.",
                        inline=False)
        embed.add_field(name="m!mute <member id or mention>", value="Mutes a member from the guild.",
                        inline=False)
        embed.add_field(name="m!unmute <member name or mention>", value="Unmutes a member from the guild.", inline=False)

        await ctx.author.send(embed=embed)
        await ctx.send("Sent you a DM containing Moderation commands!")

    @moderation.error
    async def moderation_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            errormsg = await ctx.send("You are not permitted to use this command.")
            await discord.Message.delete(errormsg, delay=3)

    """@commands.command(aliases=["announce"])
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
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            errormsg = await ctx.send("You are not permitted to use this command.")
            await discord.Message.delete(errormsg, delay=3)

        if isinstance(error, commands.CommandOnCooldown):
            errormsg = await ctx.send(f"Please wait another {round(error.retry_after, 2)} seconds to send an announcement.")
            await discord.Message.delete(errormsg, delay=3)"""

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if member == self.bot.user:
            await ctx.send("I can't kick myself!")
            return

        if ctx.author.top_role <= member.top_role:
            await ctx.send("You are not permitted to use this command on this user.")
            return

        embed = discord.Embed(title=f"Kicked: {member}", description=f"**Reason:** {reason}", color=0xc0d4ff)
        embed.set_footer(text=f"ID: {member.id}")

        await member.kick(reason=reason)
        await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            errormsg = await ctx.send("You are not permitted to use this command.")
            await discord.Message.delete(errormsg, delay=3)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        if member == self.bot.user:
            await ctx.send("I can't mute myself!")
            return

        if ctx.author.top_role <= member.top_role:
            await ctx.send("You are not permitted to use this command on this user.")
            return

        if get(ctx.guild.roles, name="Muted"):
            muted = discord.utils.get(ctx.guild.roles, name="Muted")
            if muted in member.roles:
                await ctx.send(f"{member.display_name} is already muted.")
                return
        else:
            message = await ctx.send("Role 'Muted' Does not exist.")
            await asyncio.sleep(1)
            await discord.Message.edit(message, content = "\nCreating role 'Muted'")
            await asyncio.sleep(1)
            await ctx.guild.create_role(name="Muted")
            await asyncio.sleep(1)
            await discord.Message.edit(message, content = "\nFinished creating role 'Muted'")
            await asyncio.sleep(1)
            muted = discord.utils.get(ctx.guild.roles, name="Muted")

        embed = discord.Embed(title=f"Muted: {member}", description=f"**Reason:** {reason}", color=0xc0d4ff)
        embed.set_footer(text=f"ID: {member.id}")

        await member.add_roles(muted)
        await ctx.send(embed=embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            errormsg = await ctx.send("You are not permitted to use this command.")
            await discord.Message.delete(errormsg, delay=5)
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

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if member == self.bot.user:
            await ctx.send("I can't ban myself!")
            return

        if ctx.author.top_role <= member.top_role:
            await ctx.send("You are not permitted to use this command on this user.")
            return

        embed = discord.Embed(title=f"Banned: {member}", description=f"**Reason:** {reason}", color=0xc0d4ff)
        embed.set_footer(text=f"ID: {member.id}")

        await member.ban(reason=reason)

        await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            errormsg = await ctx.send("You are not permitted to use this command.")
            await discord.Message.delete(errormsg, delay=3)

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason=None):
        if member == self.bot.user:
            await ctx.send("I can't softban myself!")
            return

        if ctx.author.top_role <= member.top_role:
            await ctx.send("You are not permitted to use this command on this user.")
            return

        embed = discord.Embed(title=f"Softbanned: {member}", description=f"**Reason:** {reason}", color=0xc0d4ff)
        embed.set_footer(text=f"ID: {member.id}")

        await member.ban(reason=reason)
        await ctx.guild.unban(member)

        await ctx.send(embed=embed)

    @softban.error
    async def softban_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            errormsg = await ctx.send("You are not permitted to use this command.")
            await discord.Message.delete(errormsg, delay=3)

    @commands.command(pass_context=True)
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
    async def unban_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            errormsg = await ctx.send("You are not permitted to use this command.")
            await discord.Message.delete(errormsg, delay=3)

        print(error)

    @commands.command(aliases=["clean", "purge"], pass_context=True)
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        return

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            errormsg = await ctx.send(f"Please wait another {round(error.retry_after, 2)} seconds to purge the chat.")
            await discord.Message.delete(errormsg, delay=3)
        
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            errormsg = await ctx.send("You are not permitted to use this command.")
            await discord.Message.delete(errormsg, delay=3)

    @commands.command(aliases=["update"])
    async def reload(self, ctx, *, extension = None):
        if ctx.author.id == 154342861851197440:
            extensions = ['Cogs.Balance',
                'Cogs.Intents',
                'Cogs.Moderation',
                'Cogs.Utility',
                'Cogs.Information',
                'Cogs.Fun',
                'Cogs.Gambling',
                'Cogs.PodRacing',
                'Cogs.Fishing']

            embed = discord.Embed(title="Reloading Scripts", description=None, color=0xc0d4ff)

            if extension is not None:
                extensions = extension.lower()

                if extension == "balance":
                    extension = "Cogs.Balance"
                elif extension == "intents":
                    extension = "Cogs.Intents"
                elif extension == "moderation" or extension == "mod":
                    extension = "Cogs.Moderation"
                elif extension == "utility":
                    extension = "Cogs.Utility"
                elif extension == "information":
                    extension = "Cogs.Information"
                elif extension == "fun":
                    extension = "Cogs.Fun"
                elif extension == "gambling":
                    extension = "Cogs.Gambling"
                elif extension == "podracing" or extension == "racing":
                    extension = "Cogs.PodRacing"
                elif extension == "fishing":
                    extension = "Cogs.Fishing"

                if extensions:
                    try:
                        embed = discord.Embed(title=f"Reloaded Extension: {extension[5:]}", description=None, color=0xc0d4ff)
                        self.bot.reload_extension(extension)

                    except Exception as e:
                        if isinstance(e, discord.ext.commands.ExtensionAlreadyLoaded):
                            embed.add_field(name=extensions, value=f"**{extensions[5:]}** is already loaded.", inline=False)

                        if isinstance(e, discord.ext.commands.ExtensionNotFound):
                            embed.add_field(name=extensions, value=f"**{extensions[5:]}** not found.", inline=False)

                        embed = discord.Embed(title="Error", description=None, color=0xc0d4ff)
                        embed.add_field(name=extensions, value=e, inline=False)

            msg = await ctx.send(embed=embed)
            
            for extension in extensions:
                try:
                    self.bot.reload_extension(extension)
                    embed.add_field(name=extension[5:], value=f"Reloaded **{extension[5:]}**", inline=False)
                    await asyncio.sleep(1)
                    await discord.Message.edit(msg, embed=embed)
                    
                except Exception as e:
                    if isinstance(e, discord.ext.commands.ExtensionAlreadyLoaded):
                        embed.add_field(name=extension, value=f"**{extension[5:]}** is already loaded.", inline=False)
                        await asyncio.sleep(1)
                        await discord.Message.edit(msg, embed=embed)

                    if isinstance(e, discord.ext.commands.ExtensionNotFound):
                        embed.add_field(name=extensions, value=f"**{extensions[5:]}** not found.", inline=False)
                        await asyncio.sleep(1)
                        await discord.Message.edit(msg, embed=embed)

                    print(f"{extension[5:]} cannot be loaded. {e}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def giveroleall(self, ctx, *, rolename):
        if get(ctx.guild.roles, name=rolename):
            role = discord.utils.get(ctx.guild.roles, name=rolename)
            for member in ctx.guild.members:
                if role in member.roles or member.bot:
                        continue
                else:
                    await member.add_roles(role)
                    msg = await ctx.send(f"Added {rolename} role to {member.display_name}")
                    await discord.Message.delete(msg, delay=3)

        await ctx.send(f"Finished adding {rolename} role to members.")

    @giveroleall.error
    async def gra_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            errormsg = await ctx.send("You are not permitted to use this command.")
            await discord.Message.delete(errormsg, delay=3)

def setup(bot):
    bot.add_cog(ModCog(bot))
    print('Moderation loaded.')
