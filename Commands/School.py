import discord
from discord.ext import commands
from discord.utils import get
from base64 import *
import asyncio
import sys

async def notEnoughArguments(ctx):
        if len(sys.argv) < 2:
            await ctx.send('Not enough arguments!')

class School(commands.Cog, name='School.py'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='b64', aliases=['base64'],
    description='Encode or decode bytes into base 64 format.',
    usage='encode (message) | decode (message)')
    async def b64(self, ctx, command, *, code):
        if command == 'encode':
            decodedMessage = b64encode(bytes(code, encoding='utf-8'))
            await ctx.message.reply(f'Your encoded message is: {decodedMessage}', mention_author = False)
            return
        if command == 'decode':
            decodedMessage = b64decode(bytes(code, encoding='utf-8'))
            await ctx.message.reply(f'Your decoded message is: {decodedMessage}', mention_author = False)
            return

    @commands.command(name='truthtable', aliases=['tt'],
    description='Generate a random truth table',
    usage='{truthtable} {variables}')
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def truthTable(self, ctx, variables):
        if variables < str(2):
            def check(m):
                return m.author == ctx.author and m.channel == ctx.message.channel

            await ctx.message.reply("The lowest number of variables you can use is 2. Would you like to use 2? (y/n)", mention_author = False)
            twoMessage = await self.bot.wait_for('message', check=check, timeout=120)
            if twoMessage.content.lower() == "y" or twoMessage.content.lower() == "yes":
                await ctx.send("A       B         out")
                for A in [False, True]:
                    for B in [False, True]:
                        out = A and not B or not A
                        await asyncio.sleep(1)
                        await ctx.send('%5s %5s %5s' % (A, B, out))
            elif "tt" in twoMessage.content.lower():
                return
            else:
                await ctx.send("Cancelled command.")

        if variables == str(2):
            await ctx.send("A       B         out")
            for A in [False, True]:
                for B in [False, True]:
                    out = A and not B or not A
                    await asyncio.sleep(1)
                    await ctx.send('%5s %5s %5s' %   (A, B, out))
        
        if variables == str(3):
            await ctx.send("   x        y        z          out")
            for x in [False, True]:
                for y in [False, True]:
                    for z in [False, True]:
                        out = (x or not z) and (not y or z)
                        await asyncio.sleep(1)
                        await ctx.send("%5s %5s %5s %5s" % (x, y, z, out))

        if variables == str(4):
            await ctx.send('a        b         c        d         out')
            for a in [False, True]:
                for b in [False, True]:
                    for c in [False, True]:
                        for d in [False, True]:
                            out = (a or not b or d) and (not b or not d) and (not a or b or c or not d)
                            await asyncio.sleep(1)
                            await ctx.send("%5s %5s %5s %5s %5s" % (a, b, c, d, out))

        if variables == str(5):
            await ctx.send('  m       n        p       q         r          out')
            for m in [False, True]:
                for n in [False, True]:
                    for p in [False, True]:
                        for q in [False, True]:
                            for r in [False, True]:
                                out = (p or not q) and (m or not n or q or r) and (not m or not n or p or r) and (not n or not q or not r)
                                await asyncio.sleep(1)
                                await ctx.send('%5s %5s %5s %5s %5s %5s' % (m, n, p, q, r, out))
                                return

    # Shift Cipher
    def shift(p, k):
        return (p + k) % 256

    def shiftCipher(k, plaintext):
        def shiftClosure(p):
            return (p + k) % 256
        return map(shiftClosure, plaintext)

    def linear(p, m, k):
        def linearClosure():
            return (p * m * k) % 256
        return linearClosure()

    def linearCipher(m, k, plaintext):
        def linearClosure(p):
            return (p * m * k) % 256
        return map(linearClosure, plaintext)
                 
def setup(bot):
    bot.add_cog(School(bot))