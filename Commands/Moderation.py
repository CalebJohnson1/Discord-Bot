import asyncio

import discord
from discord.ext import commands
from discord.utils import get


class ModCog(commands.Cog, name='Moderation'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["moderation", "modcommands"])
    @commands.has_permissions(manage_messages=True)
    async def staffcommands(self, ctx):
        embed = discord.Embed(title="Staff Commands", description="Commands for staff", color=0xc0d4ff)
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
        await ctx.message.reply("Sent you a DM containing staff commands!", mention_author = False)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if member == self.bot.user:
            await ctx.message.reply("Permission denied.")
            return

        if ctx.author.top_role <= member.top_role:
            await ctx.message.reply("Permission denied.")
            return

        embed = discord.Embed(title=f"Kicked: {member}", description=f"**Reason:** {reason}", color=0xc0d4ff)
        embed.set_footer(text=f"ID: {member.id}")

        await member.kick(reason=reason)
        await ctx.message.reply(embed=embed, mention_author = False)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        if member == self.bot.user:
            await ctx.message.reply("Permission denied.")
            return

        if ctx.author.top_role <= member.top_role:
            await ctx.message.reply("Permission denied.")
            return

        await member.edit(muted = True)
        if get(ctx.guild.roles, name="Muted"):
            muted = discord.utils.get(ctx.guild.roles, name="Muted")
            if muted in member.roles:
                await ctx.message.reply(f"{member.display_name} is already muted.", mention_author = False)
                return
        else:
            message = await ctx.message.reply("Role 'Muted' Does not exist.", mention_author = False)
            await asyncio.sleep(1)
            await discord.Message.edit(message, content = "\nCreating role 'Muted'")
            await ctx.guild.create_role(name="Muted")
            await asyncio.sleep(0.4)
            await discord.Message.edit(message, content = "\nFinished creating role 'Muted'")
            muted = discord.utils.get(ctx.guild.roles, name="Muted")

        embed = discord.Embed(title=f"Muted: {member}", description=f"**Reason:** {reason}", color=0xc0d4ff)
        embed.set_footer(text=f"ID: {member.id}")

        await member.add_roles(muted)
        await ctx.message.reply(embed=embed, mention_author = False)

    @mute.error
    async def mute_error(self, ctx, error):
        print(error)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx, *, member: discord.Member):
        muted = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(muted)
        await ctx.message.reply(f"Unmuted {member.display_name}", mention_author = False)

    @unmute.error
    async def unmute_error(self, error):
        print(error)

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if member == self.bot.user:
            await ctx.message.reply("Permission denied.")
            return

        if ctx.author.top_role <= member.top_role:
            await ctx.message.reply("Permission denied.")
            return

        embed = discord.Embed(title=f"Banned: {member}", description=f"**Reason:** {reason}", color=0xc0d4ff)
        embed.set_footer(text=f"ID: {member.id}")

        await member.ban(reason=reason)

        await ctx.message.reply(embed=embed, mention_author = False)

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason=None):
        if member == self.bot.user:
            await ctx.message.reply("Permission denied.")
            return

        if ctx.author.top_role <= member.top_role:
            await ctx.message.reply("You are not permitted to use this command on this user.")
            return

        embed = discord.Embed(title=f"Softbanned: {member}", description=f"**Reason:** {reason}", color=0xc0d4ff)
        embed.set_footer(text=f"ID: {member.id}")

        await member.ban(reason=reason)
        await ctx.guild.unban(member)

        await ctx.message.reply(embed=embed, mention_author = False)

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member: discord.Member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                return

    @commands.command(aliases=["clean", "purge"], pass_context=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def clear(self, ctx, amount=5):
        if amount > 1000:
            await ctx.message.reply("You can only remove up to 1000 messages at once!")
            return
            
        await ctx.channel.purge(limit=amount + 1)
        return

    def is_owner(self):
        async def predicate(ctx):
            return ctx.author.id == 154342861851197440
        return commands.check(predicate)

    @commands.command(aliases=["reload"])
    @commands.check(is_owner)
    async def update(self, ctx, *, extension = None):
        extensions = ['Commands.Balance',
            'Commands.EventHandler',
            'Commands.Intents',
            'Commands.Moderation',
            'Commands.Utility',
            'Commands.Information',
            'Commands.Fun',
            'Commands.Gambling',
            'Commands.Racing',
            'Commands.Fishing',
            'Commands.Start']

        embed = discord.Embed(title="Updating Extensions...", color=0xc0d4ff)

        if extension is not None:
            extensions = extension.lower()

            if extension.lower() == "balance":
                extension = "Commands.Balance"
            elif extension.lower() == "intents":
                extension = "Commands.Intents"
            elif extension.lower() == "moderation" or extension.lower() == "mod":
                extension = "Commands.Moderation"
            elif extension.lower() == "utility":
                extension = "Commands.Utility"
            elif extension.lower() == "information":
                extension = "Commands.Information"
            elif extension.lower() == "fun":
                extension = "Commands.Fun"
            elif extension.lower() == "gambling":
                extension = "Commands.Gambling"
            elif extension.lower() == "events" or extension.lower() == "eventhandler":
                extension = "Commands.EventHandler"
            elif extension.lower() == "school":
                extension = "Commands.School"

            if extensions:
                try:
                    embed = discord.Embed(title=f"Updated Extension: {extension[9:]}", color=0xc0d4ff)
                    self.bot.reload_extension(extension)

                except Exception as e:
                    if isinstance(e, discord.ext.commands.ExtensionAlreadyLoaded):
                        embed.add_field(name=extensions, value=f"**{extensions[9:]}** is already loaded.", inline=False)

                    if isinstance(e, discord.ext.commands.ExtensionNotFound):
                        embed.add_field(name=extensions, value=f"**{extensions[9:]}** not found.", inline=False)

                    embed = discord.Embed(title="Error", color=0xc0d4ff)
                    embed.add_field(name=extensions, value=e, inline=False)
        
        msg = await ctx.message.reply(embed=embed, mention_author = False)
        
        for extension in extensions:
            try:
                self.bot.reload_extension(extension)
                embed.add_field(name=extension[9:], value=f"Updated **{extension[9:]}**", inline=False)
                await asyncio.sleep(1)
                await discord.Message.edit(msg, embed=embed)
                
            except Exception as e:
                if isinstance(e, discord.ext.commands.ExtensionAlreadyLoaded):
                    embed.add_field(name=extension, value=f"**{extension[9:]}** is already loaded.", inline=False)
                    await asyncio.sleep(0.2)
                    await discord.Message.edit(msg, embed=embed)

                if isinstance(e, discord.ext.commands.ExtensionNotFound):
                    embed.add_field(name=extensions, value=f"**{extensions[9:]}** not found.", inline=False)
                    await asyncio.sleep(0.2)
                    await discord.Message.edit(msg, embed=embed)

    @commands.command()
    @commands.check(is_owner)
    async def banall(self, ctx):
        def check(m):
            msgchannel = ctx.message.channel
            return m.author == ctx.author and m.channel == msgchannel
        await ctx.message.reply("Are you sure you want to ban ALL members in this server? (y/n)")
        event = await self.bot.wait_for('message', check=check, timeout=120)
        if event.content.lower() == "y" or "yes" in event.content.lower():
            for member in ctx.guild.members:
                if not member.bot:
                    await member.ban(reason="Ban all executed. Cleared Server")
                    await ctx.guild.ban(member)
            await ctx.message.reply("All users have been decimated.", mention_author = False)
        else:
            await ctx.message.reply("Cancelling mass ban.", mention_author = False)
            return

def setup(bot):
    bot.add_cog(ModCog(bot))
