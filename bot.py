# IMPORTS
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import nest_asyncio

# VARIABLES
load_dotenv()
token = os.environ["BOT_TOKEN"]
cid = os.environ["CLIENT_ID"]
oa2 = os.environ["CLIENT_SECRET"]
status = 'TEST STATUS'

bot = commands.Bot(command_prefix='•')


# BASE EVENTS ----------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    # PRINT BOT INFORMATION TO CONSOLE
    print(f'\npython 3.8.3')
    print(f'\nDiscord.py(Version: {discord.__version__})')
    print(f'\nBot connected as {bot.user.name}')
    print(f'\nBot ID: {bot.user.id}')
    print('\nAll events and commands loaded')
    print('\nAll systems nominal....')
    bot.remove_command('help')

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="to Speaker Honey"))
    # LOAD EXTERNAL PROGRAMS FROM OS
    for file in os.listdir('events'):
        # EVENTS
        directory = 'events.'
        if not file.startswith('__'):
            name = file.replace('.py', '')
            bot.load_extension(directory + name)
    for x in os.walk('commands', topdown=False):
        # COMMANDS
        for y in x[1]:
            if not y.startswith('__'):
                directory = 'commands.{}.'.format(y)
                for file in os.listdir('commands/{}'.format(y)):
                    if not file.startswith('__'):
                        name = file.replace('.py', '')
                        bot.load_extension(directory + name)


# INITIALIZE BOT -------- ----------------------------------------------------------------------------------------------

# ADMIN COMMANDS / EVENTS ----------------------------------------------------------------------------------------------
@bot.command()
async def test(message):
    print('\nTest successful!')
    await message.channel.send('Testing 1 2 3!')


# IGNORE MESSAGES FROM BOT | TRY COMMAND HANDLER
@bot.event
async def on_message(message):
    # if the message is from the bot itself ignore it
    if message.author == bot.user:
        pass
    await bot.process_commands(message)

# ----------------------------------------------------------------------------------------------------------------------
bot.run(os.environ["BOT_TOKEN"])
