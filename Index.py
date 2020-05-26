import asyncio
import os
import random
import sqlite3
from sqlite3 import connect

import discord
from discord.ext import commands
from discord.utils import get

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

TOKEN = read_token()

client = commands.Bot(command_prefix=["m!"], case_insensitive=True)
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="m!help"))

    try:
        print(client.user.name)
        print(client.user.id)
        print('Discord.py Version: {}'.format(discord.__version__))

    except Exception as e:
        print(e)


extensions = ['Cogs.Balance',
              'Cogs.EventHandler',
              'Cogs.Intents',
              'Cogs.Moderation',
              'Cogs.Utility',
              'Cogs.Information',
              'Cogs.Fun',
              'Cogs.Gambling',
              'Cogs.Racing',
              'Cogs.Fishing']

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            print(f"{extension} cannot be loaded. {e}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.bot:
        return

    await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        errormsg = await ctx.send("You are not permitted to use this command.")
        await discord.Message.delete(errormsg, delay=5)

    if isinstance(error, commands.CommandOnCooldown):
        errormsg = await ctx.send(f"Please wait another {round(error.retry_after, 2)} seconds to use this command.")
        await discord.Message.delete(errormsg, delay=5)

@client.check
async def block_all_dms(ctx):
    return ctx.guild is not None

client.run(TOKEN)
