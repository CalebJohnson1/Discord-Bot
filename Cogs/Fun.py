from discord.ext import commands
import discord
import random


class Fun(commands.Cog, name="Fun.py"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["quotes"])
    async def quote(self, ctx):
        with open("Quotes.txt", "r") as m:
            quotes = random.choice(m.readlines())
            await ctx.send(quotes)

    @commands.command(aliases=["facts"])
    async def fact(self, ctx):
        with open("Facts.txt", "r") as f:
            facts = random.choice(f.readlines())
            await ctx.send(facts)

    @commands.command(aliases=["pfact"])
    async def pokemonfact(self, ctx):
        with open("PokemonFacts.txt", "r") as p:
            pokemonfacts = random.choice(p.readlines())
            await ctx.send(pokemonfacts)

    @commands.command(aliases=["jokes"])
    async def joke(self, ctx):
        with open("Jokes.txt", "r") as j:
            jokes = random.choice(j.readlines())
            await ctx.send(jokes)
            return

    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, question = None):
        if question is None:
            await ctx.send("Please input a question.\nUsage: **m!8ball <question>**")
            return

        member = ctx.author.display_name
        responses = [
            f"Certainly, {member}!",
            f"It is decidedly so, {member}",
            f"Without a doubt, {member}",
            f"Yes - definitely, {member}",
            f"You may rely on it, {member}",
            f"As I see it, yes, {member}",
            f"Most likely, {member}",
            f"Outlook good, {member}",
            f"Yes, {member}",
            f"No, {member}",
            f"Signs point to yes, {member}",
            f"Reply hazy, try again, {member}",
            f"Ask again later, {member}",
            f"Better not tell you now, {member}",
            f"Cannot predict now, {member}",
            f"Concentrate and ask again, {member}",
            f"Don't count on it, {member}",
            f"My reply is no, {member}",
            f"My sources say no, {member}",
            f"Outlook not so good, {member}",
            f"Very doubtful, {member}"]

        await ctx.send(f"{random.choice(responses)}")

    @commands.command(aliases=["generateusername", "randomname", "randname", "username"])
    async def generate(self, ctx):
        with open("Adjectives.txt", "r") as adjectives:
            prefix = adjectives.read().strip(' \n').split('\n')
        with open("Nouns.txt", "r") as nouns:
            suffix = nouns.read().strip(' \n').split('\n')

        firstword = random.choice(prefix)
        secondword = random.choice(suffix)

        await ctx.send(f"Generated Username: {firstword.title()}{secondword.title()}")

    @commands.command()
    async def encounter(self, ctx, amount, *, pokemon=None):
        if pokemon is None:
            pokemon = "Pokémon"

        if int(amount) < 1 or int(amount) > 1000000:
            await ctx.send("Please specify a number between 1 and 1000000.")
            return

        shinies = 0
        pokerus = 0

        for encounters in range(int(amount)):
            if random.randrange(4096) == 1:
                shinies += 1
            if random.randrange(21845) == 1:
                pokerus += 1

        embed = discord.Embed(title=f"Total {pokemon.title()} encountered: {int(amount):,}",
                              description=f"Total Shinies: {int(shinies):,}\n"
                                          f"Total Pokérus: {int(pokerus):,}\n",
                              color=0xc0d4ff)
        await ctx.send(embed=embed)

    @encounter.error
    async def encountererror(self, ctx, error):
        await ctx.send('Please specify an amount + name to encounter.\nUsage: **m!encounter <amount> <pokemon>**')
        print(error)

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def fakebal(self, ctx):
        balance = random.randint(1000000, 100000000)
        embed = discord.Embed(title=f"{ctx.author.display_name}'s balance:",
                              description=f"You currently have {balance:,} credits.",
                              color=0x00ae86)
        embed.set_thumbnail(
            url="https://images-ext-2.discordapp.net/external/xlEcYc2ErW6-vD7-nHbk3pv2u4sNwjDVx3jFEL6w9fc/https/emojipedia-us.s3.amazonaws.com/thumbs/120/emoji-one/104/money-bag_1f4b0.png")

        await ctx.send(embed=embed)

    @fakebal.error
    async def fakebal_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Please wait another {round(error.retry_after, 2)} seconds to use this command.")

    @commands.command()
    async def catch(self, ctx, *, pokemon):
        await ctx.send(
            f"Congratulations {ctx.author.mention}! You caught a level {random.randint(1, 41)} Shiny {pokemon.title()}!")

    @catch.error
    async def catch_error(self, ctx, error):
        await ctx.send("Please input the name of a pokemon to catch.")
        print(error)

    @commands.command()
    async def redeem(self, ctx, pokemon):
        await ctx.send(f"You have been given a Shiny {pokemon.title()}!")

    @commands.command()
    async def say(self, ctx, *, message=None):
        if message is None:
            await ctx.send("Please input a message.\nUsage: **m!say** <message>")
            return

        await discord.Message.delete(ctx.message, delay=None)
        await ctx.send(message.title())

    @commands.command()
    async def hug(self, ctx, *, member: discord.Member = None):
        if member is None or ctx.author == member:
            title = f"{ctx.author.display_name} hugged.. themselves?"
        else:
            title = f"{ctx.author.display_name} hugged {member.display_name} :heart:"

        hugs = ["https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif",
                "https://media.giphy.com/media/lrr9rHuoJOE0w/giphy.gif",
                "https://media.giphy.com/media/wnsgren9NtITS/giphy.gif",
                "https://i.imgur.com/r9aU2xv.gif",
                "https://media2.giphy.com/media/C4gbG94zAjyYE/source.gif",
                "https://media.giphy.com/media/l2QDM9Jnim1YVILXa/giphy.gif",
                "https://media.giphy.com/media/kvKFM3UWg2P04/giphy.gif",
                "https://66.media.tumblr.com/18fdf4adcb5ad89f5469a91e860f80ba/tumblr_oltayyHynP1sy5k7wo1_400.gif",
                "https://66.media.tumblr.com/f2a878657add13aa09a5e089378ec43d/tumblr_n5uovjOi931tp7433o1_500.gif",
                "https://i.imgur.com/gSGeZJF.gif",
                "https://66.media.tumblr.com/291c8b98b219283f9e21927e7ef6c3f2/tumblr_mzscklfLYx1tptsy9o1_400.gif",
                "https://thumbs.gfycat.com/WideSplendidDegu-size_restricted.gif",
                "https://i.imgur.com/XEs1SWQ.gif",
                "https://66.media.tumblr.com/680b69563aceba3df48b4483d007bce3/tumblr_mxre7hEX4h1sc1kfto1_500.gif",
                "https://i.imgur.com/VgP2ONn.gif",
                "https://media.giphy.com/media/13YrHUvPzUUmkM/giphy.gif",
                "https://i.pinimg.com/originals/b8/7f/8b/b87f8b1e2732c534a00937ffb24baa79.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1461001265-bd6ca0c499ca9c6065249953dfcf81c3.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1461073447-335af6bf0909c799149e1596b7170475.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1460988091-6e86cd666a30fcc1128c585c82a20cdd.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1461068547-d8d6dc7c2c74e02717c5decac5acd1c7.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1461071296-7451c05f5aae134e2cceb276b085a871.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1460993069-9ac8eaae8cd4149af4510d0fed0796bf.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1461070662-746f6d141ceabedf540dddfe9b63c162.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1461072530-67e47644a893e9f266042edc7ff6bcdd.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1461068486-646f3523d0fd8f3e6d818d96012b248e.gif",
                "https://media.tumblr.com/tumblr_m1oqhy8vrH1qfwmvy.gif",
                "https://cdn.weeb.sh/images/ryCG-OatM.gif"]
        gif = random.choice(hugs)
        embed = discord.Embed(title=title, description=None, color=0xc0d4ff)
        embed.set_image(url=gif)
        if member is None or ctx.author == member:
            embed.set_footer(text=f"Maybe {ctx.author.display_name} will have someone to hug next time.")

        await ctx.send(embed=embed)

    @hug.error
    async def hug_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.send("Please specify another user to hug.\nUsage: **m!hug <user>**")

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def kiss(self, ctx, *, member: discord.Member = None):
        if member is None or ctx.author == member:
            title = f"{ctx.author.display_name} kissed.. themselves?"
        else:
            title = f"{ctx.author.display_name} kissed {member.display_name} :heart:"

        gifs = ["https://media1.tenor.com/images/78095c007974aceb72b91aeb7ee54a71/tenor.gif?itemid=5095865",
                "https://media.giphy.com/media/bm2O3nXTcKJeU/giphy.gif",
                "https://66.media.tumblr.com/9bc0e1ca92cbad03069614eb0ed24ff3/tumblr_n0t6f5nyl51sft2bfo1_400.gif",
                "https://66.media.tumblr.com/5d51b3bbd64ccf1627dc87157a38e59f/tumblr_n5rfnvvj7H1t62gxao1_500.gif",
                "https://66.media.tumblr.com/42f96e0adb59440843c94e45650afd19/tumblr_n5mbsq844s1tzpao0o1_500.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1483589430-f951b924a6fd5f59434ad3c63fc6960c.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1483588499-c936779a4753c142eef7e4240c1a0deb.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1483588837-8380565ad290759921ae355a0bc242f5.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1483588610-757dd65fdeba2190b8c85973db6b3f96.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1483588705-b321623c459d2a7001761459d2c8707a.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1483588772-bde49b07ca18ca564d91efa7ac9703d7.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1483589322-70d5cd37d37a30f8996b85f217bce47b.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1483589646-9c8cd327454990f5da24af7d3f057627.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1483589715-78566ff0e75a4c8f004df98d994561e4.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1483589844-8d0395a7386d12026399620c087f4b97.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1483590013-b9d0df015159909c2fc2afe38651250f.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1483590131-f84dd6ab7ec5369c6ec6a2c0eb70cb64.gif",
                "https://cdn.myanimelist.net/s/common/uploaded_files/1483590257-0861880ab63699fae58af9c57e58d3b4.gif",]

        gif = random.choice(gifs)

        embed = discord.Embed(title=title, description=None, color=0xc0d4ff)
        embed.set_image(url=gif)
        if member is None or ctx.author == member:
            embed.set_footer(text=f"Maybe {ctx.author.display_name} will have someone to kiss next time.")

        await ctx.send(embed=embed)

    @kiss.error
    async def kiss_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.send("Please specify another user to kiss.\nUsage: **m!kiss <user>**")

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Please {ctx.author.display_name}, take two seconds to breathe.")

    @commands.command(aliases=["backward", "backwards"])
    async def reverse(self, ctx, *, message = None):
        if message is None:
            await ctx.send("Please input a message.\nUsage: **m!reverse** <message>")
            return

        await ctx.send(message[::-1])


def setup(bot):
    bot.add_cog(Fun(bot))
    print("FunCmds Loaded")
