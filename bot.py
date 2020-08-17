# IMPORTS
import os
import discord
from discord.ext.commands import Bot
from Commands.CommandHandler import CommandHandler


# VARIABLES
bot = Bot(command_prefix='-')
ch = CommandHandler(bot)


# BOT IS READY
@bot.event
async def on_ready():
    try:
        # PRINT BOT INFORMATION TO CONSOLE
        print(bot.user.name)
        print(bot.user.id)
        print('Discord.py Version: {}'.format(discord.__version__))
        print('All systems nominal.')

    except Exception as e:
        print(e)


# IGNORE MESSAGES FROM BOT | TRY COMMAND HANDLER
@bot.event
async def on_message(message):
    # if the message is from the bot itself ignore it
    if message.author == bot.user:
        pass
    else:

        # try to evaluate with the command handler
        try:
            await ch.command_handler(message)

        # message doesn't contain a command trigger
        except TypeError as e:
            pass

        # generic python error
        except Exception as e:
            print(e)


bot.run(os.environ["BOT_TOKEN"])
