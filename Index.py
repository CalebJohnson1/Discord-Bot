import discord
from discord.ext import commands

def read_token():
    with open('token.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()

TOKEN = read_token()

client = commands.Bot(command_prefix=['::'], case_insensitive=True)
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='::help'))

    try:
        print(f'\nName: {client.user.name}\nID: {client.user.id}')
        print('Discord.py Version: {}'.format(discord.__version__))

    except Exception as e:
        print(e)

extensions = [#'Commands.Balance',
              'Commands.EventHandler',
              'Commands.Utility',
              'Commands.Information',
              'Commands.Intents',
              'Commands.Fun',
              #'Commands.Gambling',
              'Commands.Moderation',
              'Commands.School'
              ]

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
            print(f'{extension[9:]} loaded')
        except (discord.ClientException, ModuleNotFoundError):
            print(f'{extension[9:]} cannot be loaded')

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
        errormsg = await ctx.message.reply("Permission denied.")
        await discord.Message.delete(errormsg, delay=5)

    if isinstance(error, commands.CommandOnCooldown):
        retry = error.retry_after
        if retry > 10:
            errormsg = await ctx.message.reply(f"Please wait another **{round(error.retry_after)}** seconds to use this command.")
            await discord.Message.delete(errormsg, delay=8)
            return
        if retry > 1 and retry < 10:
            errormsg = await ctx.message.reply(f"Please wait another **{round(error.retry_after, 1)}** seconds to use this command.")
            await discord.Message.delete(errormsg, delay=8)
            return
        else:
            errormsg = await ctx.message.reply(f"Please wait another **{round(error.retry_after, 3)}** seconds to use this command.")
            await discord.Message.delete(errormsg, delay=8)
            return

@client.check
async def block_all_dms(ctx):
    return ctx.guild is not None

client.run(TOKEN)
