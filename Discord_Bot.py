import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import sqlite3
from sqlite3 import connect
import random
import os


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


TOKEN = read_token()

client = commands.Bot(command_prefix=["m!", "M!", "may!", "May!"], case_insensitive=True)
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="m!help"))

    try:
        print(client.user.name)
        print(client.user.id)
        print('Discord.py Version: {}'.format(discord.__version__))

    except Exception as E:
        print(E)


extensions = ['Cogs.Balance',
              'Cogs.Intents',
              'Cogs.Moderation',
              'Cogs.Utility',
              'Cogs.Information',
              'Cogs.Fun',
              'Cogs.Gambling',
              'Cogs.PodRacing',
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
        
    if isinstance(message.channel, discord.DMChannel):
        return

    await client.process_commands(message)

client.run(TOKEN)
