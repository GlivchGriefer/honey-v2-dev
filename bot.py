# IMPORTS
import os
import discord
from discord.ext import commands


# VARIABLES
bot = commands.Bot(command_prefix='-')


# BOT IS READY
@bot.event
async def on_ready():
    try:
        # PRINT BOT INFORMATION TO CONSOLE
        print(bot.user.name)
        print(bot.user.id)
        print('Discord.py Version: {}'.format(discord.__version__))
        print('All systems nominal....')

    except Exception as e:
        print(e)


# ADD COMMANDS ---------------------------------------------------------------------------------------------------------
@bot.command()
async def ping(ctx):
    await ctx.send('pong')
# ----------------------------------------------------------------------------------------------------------------------


# IGNORE MESSAGES FROM BOT | TRY COMMAND HANDLER
@bot.event
async def on_message(message):
    # if the message is from the bot itself ignore it
    if message.author == bot.user:
        pass


bot.run(os.environ["BOT_TOKEN"])
